-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE)
-- omega-tail : empreinte JA4 du ClientHello, calculee par HAProxy AVANT tout chiffrement (lot 6).
-- Ecrit d'apres la specification publique de FoxIO (JA4, licence BSD 3-Clause). Meme calcul que
-- omega_tail/domain/ja4.py (reference des tests). Action « lua.omega_ja4 » : pose sess.ja4 ; ne refuse jamais rien
-- elle-meme, et une donnee mal formee laisse simplement sess.ja4 vide.
-- A appeler APRES une regle qui attend le ClientHello complet (req.ssl_hello_type 1).

local VERSIONS = {[0x0304] = "13", [0x0303] = "12", [0x0302] = "11", [0x0301] = "10", [0x0300] = "s3",
                  [0x0002] = "s2", [0xfeff] = "d1", [0xfefd] = "d2", [0xfefc] = "d3"}
local EMPTY = "000000000000"

local function grease(v)
  return (v & 0x0f0f) == 0x0a0a and (v >> 8) == (v & 0xff)
end

local function u16(s, i)
  local a, b = s:byte(i, i + 1)
  return a * 256 + b
end

-- valeurs de 16 bits entre les octets first et last (inclus)
local function list16(s, first, last, out)
  local k = first
  while k + 1 <= last do
    out[#out + 1] = u16(s, k)
    k = k + 2
  end
  return out
end

local function clean(values)
  local out = {}
  for _, v in ipairs(values) do
    if not grease(v) then out[#out + 1] = v end
  end
  return out
end

local function hex4(values, skip)
  local out = {}
  for _, v in ipairs(values) do
    if not (skip and skip[v]) then out[#out + 1] = string.format("%04x", v) end
  end
  return out
end

local function sorted(values)
  local copy = {}
  for i, v in ipairs(values) do copy[i] = v end
  table.sort(copy)
  return copy
end

local function alnum(c)
  return (c >= 0x30 and c <= 0x39) or (c >= 0x41 and c <= 0x5a) or (c >= 0x61 and c <= 0x7a)
end

-- SHA-256 deja calcules (memes listes pour les memes clients : navigateurs, outil d'une attaque) ; vide au-dela
-- de 4096 entrees. Mesure du 2026-11-23 : les deux appels a sha2 etaient la moitie du cout de l'empreinte.
local cache, cached = {}, 0

local function h12(txn, text)
  if text == "" then return EMPTY end
  local found = cache[text]
  if found then return found end
  found = string.lower(txn.c:hex(txn.c:sha2(text, 256))):sub(1, 12)
  if cached >= 4096 then cache, cached = {}, 0 end
  cache[text] = found
  cached = cached + 1
  return found
end

local function compute(txn, d)
  if #d < 9 or d:byte(1) ~= 0x16 or d:byte(6) ~= 0x01 then return nil end
  local length = d:byte(7) * 65536 + d:byte(8) * 256 + d:byte(9)
  if length < 38 or #d < 9 + length then return nil end
  local stop = 9 + length                      -- dernier octet du ClientHello
  local version = u16(d, 10)
  local at = 10 + 34
  at = at + 1 + d:byte(at)                     -- session
  local count = u16(d, at)
  local ciphers = list16(d, at + 2, math.min(stop, at + 1 + count), {})
  at = at + 2 + count
  at = at + 1 + d:byte(at)                     -- compression
  local exts, sig, vers, alpn = {}, {}, {}, nil
  if at + 1 <= stop then
    local last = math.min(stop, at + 1 + u16(d, at))
    at = at + 2
    while at + 3 <= last do
      local kind, size = u16(d, at), u16(d, at + 2)
      local first, final = at + 4, math.min(stop, at + 3 + size)
      exts[#exts + 1] = kind
      if kind == 0x000d and size >= 2 then
        list16(d, first + 2, math.min(final, first + 1 + u16(d, first)), sig)
      elseif kind == 0x002b and size >= 1 then
        list16(d, first + 1, math.min(final, first + d:byte(first)), vers)
      elseif kind == 0x0010 and size >= 3 and alpn == nil then
        alpn = d:sub(first + 3, math.min(final, first + 2 + d:byte(first + 2)))
      end
      at = at + 4 + size
    end
  end
  ciphers, exts, vers, sig = clean(ciphers), clean(exts), clean(vers), clean(sig)
  local top = version
  if #vers > 0 then
    top = 0
    for _, v in ipairs(vers) do if v > top then top = v end end
  end
  local sni = "i"
  for _, v in ipairs(exts) do if v == 0 then sni = "d" end end
  local code = "00"
  if alpn and #alpn > 0 then
    local f, l = alpn:byte(1), alpn:byte(#alpn)
    if alnum(f) and alnum(l) then
      code = string.char(f) .. string.char(l)
    else
      code = string.format("%02x", f):sub(1, 1) .. string.format("%02x", l):sub(2, 2)
    end
  end
  local part_b = h12(txn, table.concat(hex4(sorted(ciphers)), ","))
  local kept = table.concat(hex4(sorted(exts), {[0x0000] = true, [0x0010] = true}), ",")
  local signatures = table.concat(hex4(sig), ",")
  local part_c = EMPTY
  if kept ~= "" then
    if signatures ~= "" then part_c = h12(txn, kept .. "_" .. signatures) else part_c = h12(txn, kept) end
  end
  return string.format("t%s%s%02d%02d%s_%s_%s", VERSIONS[top] or "00", sni, math.min(#ciphers, 99),
                       math.min(#exts, 99), code, part_b, part_c)
end

-- Lecture du seul enregistrement TLS (en-tete, puis sa longueur exacte) : lire tout le tampon coutait
-- +0,1 ms par connexion (mesure du 2026-11-23).
local function record(txn)
  local head = txn.f:req_payload(0, 9)
  if not head or #head < 9 then return "" end
  return txn.f:req_payload(0, 9 + head:byte(7) * 65536 + head:byte(8) * 256 + head:byte(9)) or ""
end

local function tag_ja4(txn)
  local ok, value = pcall(function() return compute(txn, record(txn)) end)
  if ok and value then txn:set_var("sess.ja4", value) end
end

core.register_action("omega_ja4", {"tcp-req"}, tag_ja4, 0)

-- Action de la porte : empreinte, puis pays et AS (omega_geo.lua) - un seul appel Lua par connexion.
core.register_action("omega_groupes", {"tcp-req"}, function(txn)
  tag_ja4(txn)
  if omega_geo_tag then omega_geo_tag(txn) end
end, 0)
