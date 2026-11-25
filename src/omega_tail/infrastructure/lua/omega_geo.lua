-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
-- omega-tail : pays et AS de l'adresse reelle (lot 6). Lit geo.bin (format dans omega_tail/domain/geo.py, base
-- DB-IP Lite, CC BY 4.0) une fois au chargement, puis cherche par dichotomie : une quinzaine de Mo en memoire au
-- lieu de +630 Mo pour des plages CIDR dans HAProxy (mesure du 2026-11-23).
-- Chargement : lua-load omega_geo.lua <chemin de geo.bin>. Echantillons : lua.omega_pays (« FR »), lua.omega_as
-- (« AS13335 ») ; « -- » et « AS0 » si l'adresse est inconnue ou la base absente.

local args = table.pack(...)
local data = nil
local sections = {}

do
  local handle = args[1] and io.open(args[1], "rb")
  if handle then
    data = handle:read("a")
    handle:close()
  end
  if data and data:sub(1, 8) == "OMGEO001" then
    local at = 9
    for _, spec in ipairs({{4, 2}, {16, 2}, {4, 4}, {16, 4}}) do
      local count = string.unpack(">I4", data, at)
      at = at + 4
      sections[#sections + 1] = {first = at, count = count, size = spec[1], step = spec[1] + spec[2]}
      at = at + count * (spec[1] + spec[2])
    end
  end
end

local function v4(text)
  local a, b, c, d = text:match("^(%d+)%.(%d+)%.(%d+)%.(%d+)$")
  if not a then return nil end
  a, b, c, d = tonumber(a), tonumber(b), tonumber(c), tonumber(d)
  if a > 255 or b > 255 or c > 255 or d > 255 then return nil end
  return ((a * 256 + b) * 256 + c) * 256 + d
end

-- adresse IPv6 en deux entiers de 64 bits (hi, lo)
local function v6(text)
  local head, tail = text:match("^(.-)::(.*)$")
  local left, right = {}, {}
  local function groups(part, out)
    for group in part:gmatch("[^:]+") do
      local value = tonumber(group, 16)
      if value == nil or value > 0xffff or #group > 4 then return false end
      out[#out + 1] = value
    end
    return true
  end
  if head then
    if not groups(head, left) or not groups(tail, right) then return nil end
  elseif not groups(text, left) then
    return nil
  end
  local all = {}
  for _, value in ipairs(left) do all[#all + 1] = value end
  if head then
    for _ = 1, 8 - #left - #right do all[#all + 1] = 0 end
  end
  for _, value in ipairs(right) do all[#all + 1] = value end
  if #all ~= 8 then return nil end
  return (all[1] << 48) | (all[2] << 32) | (all[3] << 16) | all[4],
         (all[5] << 48) | (all[6] << 32) | (all[7] << 16) | all[8]
end

-- position de la valeur de la derniere plage qui commence avant la cle, ou nil
local function search(section, hi, lo)
  local low, high, found = 0, section.count - 1, nil
  while low <= high do
    local middle = (low + high) // 2
    local at = section.first + middle * section.step
    local before
    if section.size == 4 then
      before = string.unpack(">I4", data, at) <= hi
    else
      local start_hi, start_lo = string.unpack(">I8I8", data, at)
      before = math.ult(start_hi, hi) or (start_hi == hi and (start_lo == lo or math.ult(start_lo, lo)))
    end
    if before then
      found = at + section.size
      low = middle + 1
    else
      high = middle - 1
    end
  end
  return found
end

-- (section, hi, lo) de l'adresse source ; offset 0 = pays, 2 = AS
local function locate(txn, offset)
  if #sections ~= 4 then return nil end
  local text = txn.f:src()
  if not text then return nil end
  text = tostring(text)
  if text:find(".", 1, true) then
    local value = v4(text:match("([%d%.]+)$") or "")
    if value == nil then return nil end
    return search(sections[1 + offset], value, 0)
  end
  local hi, lo = v6(text)
  if hi == nil then return nil end
  return search(sections[2 + offset], hi, lo)
end

-- Pays et AS en un seul passage (l'adresse n'est lue qu'une fois) ; appelee par l'action « omega_groupes » du
-- script des empreintes : un seul appel Lua par connexion.
function omega_geo_tag(txn)
  local country, number = "--", 0
  local ok, at = pcall(locate, txn, 0)
  if ok and at then country = data:sub(at, at + 1) end
  ok, at = pcall(locate, txn, 2)
  if ok and at then number = string.unpack(">I4", data, at) end
  txn:set_var("sess.pays", country)
  txn:set_var("sess.as", "AS" .. number)
end

-- Inconnu : « -- » et « AS0 » (un nil de Lua deviendrait « 0 » dans HAProxy).
core.register_fetches("omega_pays", function(txn)
  local ok, at = pcall(locate, txn, 0)
  if not ok or not at then return "--" end
  return data:sub(at, at + 1)
end)

core.register_fetches("omega_as", function(txn)
  local ok, at = pcall(locate, txn, 2)
  if not ok or not at then return "AS0" end
  return "AS" .. string.unpack(">I4", data, at)
end)
