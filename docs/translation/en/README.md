<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**TAILSCALE control manager with a built-in firewall for FUNNEL**

OMEGA-TAIL is the OMEGA suite tool that controls **Tailscale** on a machine and **protects** it when it
publishes a service on the Internet through **Tailscale Funnel**.

> Developed by [kraynux](https://github.com/kraynux) for [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Official page](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/en/) · [Screenshots](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Interface, documentation, exports and visitor pages available in **17 languages** — see [Interface languages](#interface-languages).  
**Languages:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** is a Python TUI (Terminal User Interface) application built with
[Textual](https://textual.textualize.io/). It lets you manage and tune **Tailscale** in advanced mode from an
interface, without remembering a single command. It also adds protections (firewall, containment, survival…) for
**Funnel** mode, which opens a service of the machine to the whole Internet.

Every action that changes the machine shows its command first. The sudo password is typed in the terminal,
action by action, and nothing is started in the background without you.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/en/omega-tail/F.png" width="32%" />
</p>

The project is designed according to **Clean Architecture** principles, with `app/` as the composition root: the
business domain, orchestration, infrastructure and interface are kept separate.

## Contents

- [Overview](#overview)
- [Understanding Tailscale and Funnel](#understanding-tailscale-and-funnel)
- [Features](#features)
- [The protections in detail](#the-protections-in-detail)
- [Measurements](#measurements)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Themes and terminals](#themes-and-terminals)
- [Files, services and compatibility](#files-services-and-compatibility)
- [Security](#security)
- [Tests and quality](#tests-and-quality)
- [Project status](#project-status)
- [Uninstallation](#uninstallation)
- [License](#license)

---

## Overview

### Why omega-tail

Tailscale Funnel publishes a service of the machine on the Internet without opening any port on the router: visitors
go through Tailscale's relays. It is simple and safe on the network side, but one weakness remains.

- **The cost of encryption.** In default Funnel mode, it is the machine's `tailscaled` service that performs the
  TLS handshake of every visitor. Measured on a small machine, this is about **80 % of the cost of a
  connection**. A few hundred new connections per second are enough to saturate the processor: a single
  ordinary computer, with a simple script, can bring down the site and the machine.
- **Invisible visitors.** The usual firewalls (nftables, ufw, fail2ban) do not see these visitors: they
  arrive encrypted, through the Tailscale tunnel, with the address of a relay.
- **Scattered settings.** Tailscale's settings (operator, exit node, routes, SSH, shields…) are
  numerous, split between commands and the web console, and some of them can cut the current session.

### Goals

- Control Tailscale entirely from an interface, with a one-sentence explanation for every setting.
- Refuse abusive connections **before** any encryption, seeing the real address of every visitor.
- Keep the machine standing under attack: administration and the other services remain reachable.
- Never impose anything: suggest, show the command, ask, and be able to roll back.
- Work on any Linux distribution, under systemd, OpenRC or runit.

### What omega-tail does

- Shows the state of Tailscale, of the machine and of what is published, with alerts that lead to the screen that
  fixes them.
- Starts, stops and restarts `tailscaled`, with a safeguard if your session goes through Tailscale.
- Manages login, accounts and every `tailscale set` setting, checked before being applied.
- Publishes, removes, suspends and tests Serve and Funnel services, with backups and restore.
- Shows the tailnet devices, their path (direct or relayed), a network diagnostic and the logs.
- Places a HAProxy **gate** between Funnel and your site: rules per address, per prefix, global budget, trust
  list and blacklist, groupings by JA4 fingerprint, origin network (AS) and country, automatic attack mode.
- Contains `tailscaled`, cuts Funnel for a while or completely, and can do it on its own thanks to an automatic watch.
- Protects the WireGuard port of `tailscaled` with an nftables table (shield).
- Produces a report of the machine and of the attacks of the last 7 days, in TXT, HTML or JSON.

### What the project does not do

- It does not replace Tailscale: it controls it.
- It does not protect against a volumetric attack that saturates the Internet line itself (the router, the link).
- It does not manage Tailscale's web admin console (access policy, approval of exit nodes,
  enabling Funnel for the tailnet).
- It does not protect a service published other than through Funnel: for those ports, there is omega-fire.
- It never runs as root and never starts anything in the background without your consent.
- It runs neither on Windows nor on macOS.

[↑ Contents](#contents)

---

## Understanding Tailscale and Funnel

omega-tail assumes a few Tailscale notions. This part gathers them, without assuming anything else.

### The vocabulary

| Term | What it is |
|---|---|
| **Tailnet** | Your private Tailscale network: all the machines connected to the same account (or the same organization). Each machine receives an address in `100.x.y.z` (range 100.64.0.0/10) and an IPv6 address in `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | The service (daemon) running on the machine: it holds the encrypted WireGuard tunnel, Tailscale's network stack and, for Serve and Funnel, the relay to your services. |
| **`tailscale`** | The command that controls `tailscaled` (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail uses it for you. |
| **WireGuard** | The encrypted tunnel protocol used between machines. For this, `tailscaled` listens on a UDP port (41641 by default), often opened by the router (UPnP). |
| **DERP relay** | Tailscale servers that relay traffic when two machines cannot reach each other directly (difficult NAT). The "direct" path is faster. |
| **MagicDNS** | The names of the tailnet machines, in the form `machine.tailnet-name.ts.net`. |
| **Serve** | Publishing a local service (a site, an API…) **for the tailnet only**, over HTTPS with a valid `*.ts.net` certificate. |
| **Funnel** | Publishing a local service **for the whole Internet**, at the address `https://machine.tailnet-name.ts.net`. Only ports 443, 8443 and 10000 can be opened. |
| **Funnel relay** | Tailscale servers that receive visitors from the Internet and bring them into your tailnet (they appear as "funnel-ingress-node"). |
| **Operator** | A Linux account allowed to change Tailscale settings without sudo (`tailscale set --operator=…`). omega-tail offers it once, through sudo. |
| **Exit node** | A machine of the tailnet through which another one sends all its Internet traffic (like a VPN). It must be approved in the Tailscale console. |
| **Advertised subnet (subnet router)** | A local network (for example `192.168.1.0/24`) that a machine makes reachable to the rest of the tailnet. |
| **Shield (shields up)** | Tailscale setting that refuses all incoming connections coming from the tailnet. |
| **Tailscale SSH** | An SSH server provided by Tailscale, authorized by the tailnet policy. |
| **PROXY v2 header** | A short header added at the start of a connection to pass the real address of the visitor to whoever receives it. |
| **JA4 fingerprint** | A signature of the way a piece of software opens a TLS connection: a browser and an attack tool do not have the same one. |
| **AS (autonomous system)** | The origin network of an address: Internet provider, hosting company, cloud. |

### A visitor's path

**Default Funnel, without omega-tail.** `tailscaled` does everything: it decrypts the WireGuard tunnel, performs the
visitor's TLS handshake, then relays the request over HTTP to your site. No firewall on the machine sees the
visitor, and every new connection is expensive for `tailscaled`.

```text
Visitor ──HTTPS──▶ Funnel relay ──WireGuard──▶ tailscaled (TLS + HTTP relay) ──HTTP──▶ your site
                   (Tailscale)                 └── all the cost is here
```

**Funnel with the omega-tail gate.** Funnel switches to TCP mode: `tailscaled` no longer does TLS, it passes the
still-encrypted stream to the gate, preceded by the real address of the visitor (PROXY v2 header). The gate decides
**before** any encryption: a refused connection costs almost nothing, and only admitted connections are
decrypted, by OpenSSL, which is faster than `tailscaled`'s TLS.

```text
Visitor ──HTTPS──▶ Funnel relay ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                    │
                                                    ▼
                                     omega-tail gate (HAProxy, 127.0.0.1)
                                     ├── refused before TLS: blacklist, rate, budget, target name, groupings
                                     └── admitted: TLS (*.ts.net certificate) ──HTTP──▶ your site
```

The gate listens only on the machine's loopback and runs under your account. The machines of your tailnet are
always admitted, before any rule: only Funnel visitors are filtered.

### What Tailscale must allow (admin console)

These settings are made once, in Tailscale's web console; omega-tail does not change them.

- **MagicDNS** and **HTTPS certificates** enabled for the tailnet (needed for Serve, Funnel and the gate's
  certificate).
- **Funnel allowed** for the machine in the tailnet access policy (`funnel` attribute).
- For an exit node or advertised subnets: their **approval** in the console.

[↑ Contents](#contents)

---

## Features

The main menu has two columns of six: **TAILSCALE** to control, **PROTECTION** to defend.

### TAILSCALE

#### 1. Dashboard

- **Tailscale**: service, connection state, running and installed version, machine name, addresses,
  account, devices online, key expiry, operator, exit node offered and used, advertised
  subnets.
- **Machine**: CPU of the whole machine, load per core, temperature, memory, CPU and memory of `tailscaled`,
  containment, then the state of the protections (Funnel, firewall and attack mode, blacklist, watch, shield).
- **Publishing**: each published port, for the Internet (Funnel) or for the tailnet (Serve), its mode and its target.
- **Alerts**, from most to least serious, with "Fix" which opens the relevant screen. For example:
  service stopped, update installed but not applied, key expiring, Funnel published without protection,
  high temperature, `tailscaled` too greedy or not contained, growing blacklist.
- Values in green, orange or red according to thresholds (CPU, load, temperature, memory, `tailscaled`).

#### 2. tailscaled service

- State as seen by the init system, running and installed version, launch command, drop-in files,
  containment.
- **Start**, **Stop**, **Restart** (for example to apply an update that is already installed).
- **Safeguard**: if your session goes through Tailscale (SSH over the tailnet), Stop asks for a second
  confirmation, because you could no longer restart it.
- **Fix startup**: spots a drop-in file that runs `tailscale up` at startup and risks taking the machine
  out of the tailnet at the first settings change; the fix is shown and the original is kept.

#### 3. Connection and settings

- **Log in**, **Log out**, **Add an account**, **Switch account**, **Permanent logout**
  (machine name to type).
- **Every `tailscale set` setting**, each with its one-sentence explanation: machine name and nickname,
  routes, tailnet DNS, shield, stateful filtering, netfilter mode, exit node, local network access,
  offering the machine as an exit node, advertised subnets, Tailscale SSH, web interface, updates,
  peer relay, operator.
- While typing, a box shows **before → after** and the command; after applying, each value read back is
  marked ✔ (taken into account) or ✖ (not).
- A warning tells you when a change can cut a session that goes through Tailscale.
- **IP forwarding**: enabled with one button when the machine serves as an exit node or advertises subnets.

#### 4. Publishing

- Everything the machine publishes: port, public (Funnel) or tailnet (Serve), mode, path, target, protection.
- **Publish** a local service over HTTPS, HTTP, TCP or terminated TLS; **Remove**; **Suspend Funnel** and
  **Restore Funnel** (identically).
- **End-to-end test**: a real connection, like a visitor (response, time, certificate, TLS version).
- **Backups**: the state before each change (the 50 most recent), restorable.
- Every change is checked; if there is a mismatch, the publishing is rebuilt, otherwise the previous state is put back.

#### 5. Network and devices

- Tailnet **devices**: system, online or not, path (direct or through a relay), last seen, address,
  traffic exchanged; Tailscale's Funnel relays are hidden by default.
- **Tailscale ping** (path and latency), **Who is it?** (who a tailnet address belongs to).
- **Network diagnostic**: UDP, IPv4 / IPv6, NAT type, port opening by the router (UPnP, NAT-PMP, PCP), nearest
  relay and latencies.
- **DNS**, **tailnet lock** and Tailscale's **internal counters**.
- Read-only: nothing on this screen changes a setting.

#### 6. Logs

- The `tailscaled` log (journalctl, or the service's files outside systemd) and the gate's log, filterable and
  exportable.
- Each piece of information has its own color, taken from the theme: date, process, message category (control,
  network, DNS, WireGuard engine), addresses in bold, errors in red, warnings in orange; for the gate, refusal reason,
  grouping, AS and country.

### PROTECTION

#### 7. Funnel firewall

- **Install HAProxy** through the distribution's package manager (pacman, apt, dnf, zypper, apk, xbps,
  emerge).
- **Enable protection**: `*.ts.net` certificate, lists, checked configuration, gate service, Funnel
  switchover then a test from the Internet; on failure, the original publishing is put back at once.
- **Disable protection**: Funnel is put back exactly as before, checked.
- **Rules** applied live, **observation** mode to tune thresholds without risk, **groupings** (see
  [The protections in detail](#the-protections-in-detail)).
- **Update the AS / country database** (DB-IP Lite), in a separate process.

#### 8. Survival

- **Containment of `tailscaled`**: CPU cap, weight and priority, option to give priority to SSH access.
- **Funnel circuit breaker**: CPU and temperature thresholds, 10-minute cut (automatic restore) or complete cut.
- **Automatic watch**: the same thing with nobody in front of the screen.
- **WireGuard port shield**: button to its screen (observation, active, set up, set up again, remove, hand over).

#### 9. Attacks and decisions

- Gate counters (received, refused before encryption, admitted, in progress) and the most active addresses,
  read again every 2 seconds, with the country, AS and state of each address.
- **Block**, **Blacklist**, **Unblock**, **Trust**: applied immediately, without restarting the gate; the
  notification states in one line the action and where the address now stands.
- **Fingerprints**, **AS** and **Countries** views; attack mode state and connections refused by the groupings.
- **Blacklist management**: full list with date added and origin, add, delete, import of a
  TXT file (duplicates, networks already covered and tailnet addresses set aside), purges with preview (by age,
  the N oldest, a range of lines, an origin, everything), TXT exports (re-importable), HTML and JSON.
  Cap of 50,000 entries.

#### 10. Report

- Everything omega-tail knows about the machine, as facts: Tailscale, publishing, machine, firewall, survival, alerts,
  and the **attacks of the last 7 days** read from the gate's log.
- **Privacy**: by default, without the Tailscale account or the names and addresses of the tailnet devices, so that
  you can send it to someone.
- **TXT**, **HTML** (theme of your choice) and **JSON** exports; **View exports** opens the folder in the browser.

#### 11. Settings

- Language of the interface and of the exports, theme of the interface and of the exports, folders for exports and
  screenshots, and their purge.

#### 12. Help

- One section per screen, the shortcuts, the command line, and **Contact and support**.

[↑ Contents](#contents)

---

## The protections in detail

Each protection answers a specific threat; none is imposed.

| Protection | Against what | Where |
|---|---|---|
| Gate (rules) | Bursts from one or a few addresses, connections that do not target the site | Funnel firewall |
| Groupings | Attacks with scattered addresses (thousands of addresses, one connection each) | Funnel firewall |
| Blacklist | Addresses and networks known to attack, kept over time | Attacks and decisions |
| Containment | `tailscaled` taking over the whole machine under attack | Survival |
| Circuit breaker | Machine saturated despite everything: cut Funnel for a while | Survival |
| Automatic watch | Same thing, with nobody in front of the screen | Survival |
| WireGuard shield | Flood of UDP packets on the `tailscaled` port, whether Funnel is open or not | Survival |

### The gate (Funnel firewall)

The rules apply in this order, all before encryption:

1. **Tailnet machines** (100.64.0.0/10, fd7a:115c:a1e0::/48): always admitted.
2. **Trust list**: never limited. **Blacklist**: refused until removed.
3. **Rate per address** (40 connections / 10 s by default): beyond that, the address is blocked for the chosen
   duration (60 min by default).
4. **Rate per prefix**: /24 in IPv4, /64 in IPv6.
5. **Global budget** of admitted connections per second: the processor is never overwhelmed.
6. **Target name**: a connection that does not target the machine's name is refused.

The gate's `*.ts.net` certificate is requested from Tailscale, checked every day and renewed live 30 days before
it expires. **Observation** mode counts everything without refusing anything.

### The groupings (fingerprints, AS, countries)

Against an attack with scattered addresses, the per-address rules only see each address once. So the gate
also classifies each client by its **JA4 fingerprint**, its **AS** and its **country**, and counts the rate of each
group.

- **Automatic attack mode**: beyond 80 incoming connections per second (adjustable), the gate switches to
  attack mode on its own, and leaves it after 5 minutes of calm.
- In attack mode only: an unknown fingerprint that explodes, a hosting or cloud AS (editable list)
  or a country from your list (empty by default) that exceeds its rate is refused.
- **Common browsers** (Chrome, Edge, Firefox) are never affected by these rules; **known clients**
  (admitted in the last 24 h) go ahead of the global budget.
- **Learning**: for 7 days, the gate learns the usual fingerprints of your site (never during an
  attack); the groupings stay in observation until then.
- Outside an attack, one connection in ten is classified; during an attack, all of them.
- The AS / country database is **DB-IP Lite**, downloaded and updated once a month.

### Survival

- **Containment**: a separate drop-in file caps `tailscaled` (for example one full core on a machine with
  4 threads) and lowers its priority. Your own configuration is never modified.
- **Circuit breaker**: when `tailscaled` stays above the CPU threshold (80 % of one core for 60 s by default) or
  the temperature reaches 85 °C, omega-tail offers to cut Funnel for 10 minutes (automatic restore,
  identically, even with omega-tail closed), to cut it completely, or to wait. The tailnet is never cut.
- **Automatic watch** (disabled by default): a service under your account cuts Funnel on its own after three
  overruns, 15 minutes the first time, 30 the second, then one hour, and restores it on its own.

### The WireGuard port shield

`tailscaled` spends about one processor core per 100,000 packets per second received on its UDP port, even
invalid ones. The shield is an nftables table placed in front of it, on the network cards:

- **known peers** (those `tailscaled` writes to) are never limited;
- handshakes are limited to 20 per second and per source;
- the other sources have a budget (500 packets per second each, 5,000 in total);
- packets that are not WireGuard are refused.

It is first set up in **observation**, then in **active** mode. If it is linked through omega-connect, **omega-fire** (3.7.0 or
newer) can set it up and manage it instead of omega-tail: it is the same table, which changes hands without being
touched.

[↑ Contents](#contents)

---

## Measurements

omega-tail's choices come from measurements, on machines of the same generation as the ones it protects
(processors from 2010 to 2016, mostly without AES acceleration).

| Measurement | Result |
|---|---|
| Share of TLS in the cost of a default Funnel connection | about 80 % |
| Cost of a connection **refused** by the gate, compared with default Funnel | **4.6 times less** |
| Cost of a connection **admitted** by the gate, compared with default Funnel | **2 times less** |
| Throughput with the gate, connections kept open (compared with a Go TLS like `tailscaled`'s) | **+15 %** requests, −20 % CPU |
| WireGuard shield: flood that took a full core from `tailscaled` | **1 %** of a core |
| Memory of the services (gate, watch, shield) | about 67 MB |

So the gate does not degrade a site's throughput: on these machines, it is encryption itself that limits, with
or without omega-tail, and in production Funnel goes through Tailscale's relays and the router anyway.

[↑ Contents](#contents)

---

## Architecture

```text
src/omega_tail/
├── app/              Composition root: assembles the layers, entry point (interface, command line)
├── core/             Shared constants
├── domain/           Pure business logic: gate rules, alerts, circuit breaker, watch, blacklist…
├── application/      Use cases: publishing, firewall, survival, report, settings
├── ports/            Contracts (Protocol) expected by the application
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, logs, exports, Lua scripts
├── interfaces/       tui/ (Textual), cli/ (command line), shared/ (help, report, presentation)
└── shared/           Languages (gettext)
```

### Design principles

- `domain/` contains no reads or writes: everything in it can be tested without a machine.
- `application/` orchestrates the use cases through the domain and the ports; the interface and the command line
  call the same use cases.
- Only `infrastructure.commands` and `infrastructure.privileged` run commands; the interface never runs any
  directly. These rules are checked automatically (import-linter).
- The interface relies on [omega-lib](https://github.com/kraynux), the library shared by the whole OMEGA
  suite (themes, terminal detection, languages, contact and support, WireGuard shield). It is not published on
  PyPI: it is bundled in the archive (`vendor/omega-lib/`).
- Every slow call (Tailscale, HAProxy, disk, network) runs as a background task: the interface never freezes.

[↑ Contents](#contents)

---

## Requirements

### System

- Linux, any distribution (tested on Arch Linux and derivatives).
- Python 3.10 or higher, with the `venv` module.
- An init system: **systemd**, **OpenRC** or **runit**.
- `sudo` for the actions that change the machine (requested action by action, never at launch).
- A terminal of at least 80×24 (see [Themes and terminals](#themes-and-terminals)).

### Tailscale

- **Tailscale** installed and connected (`tailscale` client and `tailscaled` service); tested with version 1.104.
- For Funnel: MagicDNS, HTTPS certificates and Funnel allowed in the Tailscale console (see
  [What Tailscale must allow](#what-tailscale-must-allow-admin-console)).

### Python dependencies

Installed by `install.sh` in a virtual environment:

- `textual`: the interface.
- `omega-lib`: shared library of the OMEGA suite, bundled in the archive.

### Mandatory and optional components

omega-tail detects what is present and only enables what can be used.

| Component | Role | Status |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Everything omega-tail controls | **Mandatory** |
| Python 3.10+, `textual`, `omega-lib` | The application | **Mandatory** |
| systemd, OpenRC or runit | Services for the gate, the watch, the shield | **Mandatory** (one of the three) |
| HAProxy 3.x | The gate of the Funnel firewall | Optional (can be installed from omega-tail) |
| HAProxy with Lua | The groupings (fingerprints, AS, countries) | Optional (the case for common distributions) |
| nftables (kernel with `nft_limit`) | The WireGuard port shield | Optional |
| Reading the system journal (`systemd-journal`, `adm` or `wheel` group) | Logs, attack report | Recommended |
| Browser and desktop | "View exports" in the browser (otherwise, reading inside omega-tail) | Optional |
| omega-connect | Registry, synchronization, suite updates | Optional |
| omega-fire 3.7.0+ | Managing the WireGuard shield from omega-fire | Optional |

[↑ Contents](#contents)

---

## Installation

The official archive is provided in `.tar.gz` format. Check its integrity before installing, with the
`sha.txt` file published next to it:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **These three methods are for a first installation.** If `~/omega-tail` already exists, use the
> [Update](#update) section. Never re-run these commands from inside an existing
> `omega-tail` folder: `tar` would create a nested `omega-tail/omega-tail/`.

No installation step requires root privileges: omega-tail runs as a normal user.

### Method 1 — installation script

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ You appear to already be inside an omega-tail folder — see the Update section of the README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Already extracted here, step skipped." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail already exists, move skipped." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

The script creates the virtual environment, installs the dependencies (bundled omega-lib first), makes the launchers
executable, writes the installation token read by omega-connect and offers the `omega-tail` alias. It can be
re-run safely.

### Method 2 — resilient full installation

This command can be re-run: it skips the steps already done.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ You appear to already be inside an omega-tail folder — see the Update section of the README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail already exists, extraction skipped." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv already exists, step skipped." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail installed. Run ./omega-tail.sh."
```

### Method 3 — detailed installation

```bash
# 0. Make sure we're not re-running this from inside an existing omega-tail
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ You appear to already be inside an omega-tail folder — see the Update section of the README." >&2; exit 1; }

# 1. Extract
[ -d omega-tail ] && echo "ℹ️ Already extracted here, step skipped." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Move into the home directory
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail already exists, move skipped." || mv omega-tail ~/

# 3. Enter the project
cd ~/omega-tail/

# 4. Create the virtual environment
[ -f .venv/bin/activate ] && echo "ℹ️ .venv already exists, creation skipped." || python3 -m venv .venv

# 5. Install the dependencies (bundled omega-lib first)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Make the launchers executable
chmod +x omega-tail.sh install.sh

# 7. Write the installation token (read by omega-connect; optional)
./omega-tail.sh synchro jeton

# 8. Launch
./omega-tail.sh
```

On Debian, Ubuntu and derivatives, the `venv` module is not always installed with Python:
`sudo apt install python3-venv`.

### Update

omega-tail's services (gate, watch) use the files in `~/omega-tail/var/`. An update must therefore
**keep this folder in place**: the archive contains no `var/`, and is extracted over the existing
installation.

From the folder that contains the archive, **other than `~/omega-tail`**:

```bash
# 1. Back up the current installation (var/ included)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Extract the new version on top (var/ is kept)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Reinstall (dependencies, launchers, installation token)
cd ~/omega-tail
./install.sh

# 4. Relaunch omega-tail
./omega-tail.sh
```

If the gate is active, **Funnel firewall → "Apply rules"** regenerates its configuration with the new
version, live. If the automatic watch is enabled, **Survival → "Enable watch"** restarts it with the
new code. omega-connect can also perform the update (Updater screen).

### Bash or Zsh alias

`install.sh` offers the alias. To add it by hand:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

The alias is called `omega-tail`, and not `tail`, so as not to hide the system `tail` command.

[↑ Contents](#contents)

---

## Usage

### Launch

```bash
cd ~/omega-tail
./omega-tail.sh

# or simply, if the alias was created:
omega-tail
```

The launcher asks for no elevation: omega-tail runs under your account, and sudo is only requested by the
actions that need it, in the terminal, with the command shown beforehand.

### Recommended first steps

To protect a site published through Funnel, in this order:

1. **Dashboard**: read the alerts; **Become operator** (once, through sudo) to change Tailscale settings without sudo.
2. **Survival → Apply containment**: `tailscaled` will no longer be able to take over the whole machine.
3. **Publishing**: publish the site over **HTTPS on port 443**, path `/`, then run the **end-to-end test**.
4. **Funnel firewall → Install HAProxy**, then **Enable protection**, first in **observation** mode.
5. A few days later, **Attacks and decisions**: if the counters only show abuse, switch the gate to
   **normal** mode.
6. Let the **groupings** learn for 7 days in observation, then switch them to **enforced**.
7. **Survival → WireGuard port shield**: set it up in observation, then switch to active.
8. For a machine with nobody in front of the screen: **Survival → Enable watch**.

### Interface languages

17 languages: French, English, Spanish, Portuguese (Brazil), Italian, German, Dutch, Polish, Russian,
Chinese, Vietnamese, Thai, Indonesian, Japanese, Korean, Hindi, Arabic.

- Chosen in the settings (`s` key, "Langue / Language", a label that is never translated), applied by restarting
  only the interface.
- For a single run: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- In the Linux text console (TTY), languages whose script does not exist in the console fonts
  are shown in English for the session; Arabic is displayed right to left.
- The **export language** (report, blacklist, logs) is set separately, "Same as interface" by default.

### Contact and support

Help (`a` key) offers a **Contact and support** screen:

- *Buy me a coffee* (the developer's PayPal page);
- *Contact support* (email address and the site's form, shown in plain text);
- *Declare myself as a user (anonymous)*;
- *Check for updates*.

The declaration is voluntary, off by default and sent only once. It is used only to count
users and, if you wish, their continent or country (closed lists, never free text). It sends
a randomly drawn key, the software name (`omega-tail`) and its version; never a name, a machine name, a
setting or a tailnet address. You can withdraw at any time from the same screen (*Stop declaring me*). The update
check only reads the list of versions published on the site, and never without a click.

### Links with the other omega tools

- **omega-connect**: `install.sh` writes an installation token (`var/omega-jeton.json`) that describes the tool and its
  version, without running anything. omega-connect uses it for the Registry, synchronization, repair,
  updates and installation. `./omega-tail.sh synchro jeton` rewrites it by hand.
- **omega-fire** (3.7.0 or newer), linked through omega-connect, can set up and manage the WireGuard port shield;
  its list of rules shows it with omega-tail as the origin.

### Command line

All commands are written `./omega-tail.sh …` (or `omega-tail …` with the alias):

| Command | Role |
|---|---|
| `omega-tail` | The interface |
| `omega-tail etat [--format json]` | State of Tailscale, of the machine and alerts, as text or for a script |
| `omega-tail aide` | The full help as text |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | The report, displayed or saved |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Cut or restore Funnel |
| `omega-tail veille etat` | State of the automatic watch and its last lines |
| `omega-tail porte etat` | State of the gate and counters |
| `omega-tail porte certificat [--si-besoin]` | Renew the gate's `*.ts.net` certificate |
| `omega-tail porte groupes` | Groupings: attack mode, fingerprints, AS, countries |
| `omega-tail porte base` | Update the AS / country database |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Block an address or a network (blacklist with `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Unblock |
| `omega-tail porte confiance ADRESSE` | Add to the trust list |
| `omega-tail synchro jeton` | Write the installation token (omega-connect) |
| `omega-tail --version` | The version |

### General flow

1. Startup screen, then the main menu in two columns (TAILSCALE and PROTECTION).
2. Under the title of each screen, the **status bar** sums everything up: service, CPU of the machine and of `tailscaled`,
   temperature, memory, Funnel, firewall, watch, connection. It is read again every 5 seconds.
3. Every action that changes the machine shows its command, then asks for confirmation; sudo is typed in the
   terminal and the interface comes back afterwards.
4. Sensitive actions (permanent logout, complete purge of the blacklist) ask you to type a word.
5. The result is shown in one line, checked against the state read back.

### Navigation

- Up / down arrows: move from one item to another (table rows, buttons).
- Tab / Shift+Tab: move from one area of the screen to another.
- Enter or click: activate the selected button; in the alerts table, "Fix".
- `Esc`: go back to the previous screen (in the menu: quit).
- `a`: help, from any screen.
- `s`: settings, from any screen.
- `t`: next theme (saved).
- `r`: redraw the screen, show the terminal size and read the state again.
- `q`: quit, with confirmation.
- `Ctrl+P`: commands (theme, SVG screenshot into the screenshots folder, quit).

[↑ Contents](#contents)

---

## Themes and terminals

Ten `omega-*` themes are shared with the rest of the OMEGA suite:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Switch between themes with `t`, or pick one in the settings (`s`); the choice is kept.
- HTML exports have their own themes: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail adapts visual complexity to the detected terminal through a **rendering profile**: Complete, Standard,
  Reduced or Mono (ASCII only).

| Minimum size | Profile | Typical terminals |
|---|---|---|
| 120×32 or more | Complete | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 or more | Standard | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 or more | Reduced | urxvt, xterm, modern SSH |
| below 80×24 | Mono (ASCII only) | Linux TTY, legacy SSH |

After a resize, `r` reads the terminal size again; it is shown at the top, next to the theme.

[↑ Contents](#contents)

---

## Files, services and compatibility

### In the omega-tail folder

All of omega-tail's state is in `~/omega-tail/var/`, recreated at startup and never published:

```text
var/
├── settings.json         settings (language, themes, folders, thresholds, gate rules)
├── omega-jeton.json      installation token (omega-connect)
├── porte/                gate configuration, certificate, trust list and blacklist, AS / country database
├── veille/               automatic watch log
├── survie/               originals of the modified files, circuit breaker state
├── funnel/sauvegardes/   publishing before each change (the 50 most recent)
├── exports/              exported reports, logs and lists
└── screenshots/          screenshots (Ctrl+P)
```

### On the system (only if you enable the relevant protection)

Each file is put in place through sudo, with the command shown, and removed by the reverse action in omega-tail.

| File or service | Put in place by | Removed by |
|---|---|---|
| `omega-tail-porte` service (systemd, OpenRC or runit) and `omega-tail-porte-certificat` (systemd timer, or a marked line in your crontab) | Enable protection | Disable protection |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (or a control group outside systemd) | Apply containment | Remove containment |
| `omega-tail-retablir-*` timers (restore after a cut) | Circuit breaker | End of the cut |
| `omega-tail-veille` service | Enable watch | Disable watch |
| `omega-bouclier-wg` service, nftables table, `/etc/omega-bouclier-wg/` | Shield: Set up | Shield: Remove |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | Enable IP forwarding | Deleting the file |

The `override.conf` file of `tailscaled`, if it exists, is never modified.

### Init systems

| | systemd | OpenRC | runit |
|---|---|---|---|
| `tailscaled` service | `systemctl` | `rc-service` | `sv` |
| Logs | `journalctl` | service files | `svlogd`, `socklog` |
| Containment | systemd drop-in file | control group (cgroup v2) | control group (cgroup v2) |
| Temporary cut | systemd timer | detached process under your account | detached process under your account |
| Gate, watch, shield | systemd services | OpenRC services | runit services |

Outside systemd, containment by control group is lost if `tailscaled` restarts: an alert then offers
to put it back.

### IPv4 and IPv6

The gate, the lists, the groupings and the shield handle both families. The prefixes counted are /24 in
IPv4 and /64 in IPv6; an IPv4 address seen in the form `::ffff:a.b.c.d` is treated as the IPv4 address.

[↑ Contents](#contents)

---

## Security

omega-tail acts on a service exposed to the Internet; it was designed never to make the situation worse.

- **Never root**: the application, the HAProxy gate and the watch run under your account; sudo is only requested
  to set up or remove a service, with the command shown beforehand.
- **Private channels**: the gate's administration sockets are in mode 600 inside a 700 folder; the
  synchronization of its tables goes through a socket in the same folder.
- **Rollback**: every Funnel switchover is backed up, checked, and the previous state is put back on
  failure.
- **Observation first**: the gate, the groupings and the shield are set up in observation; nothing is refused
  before you have decided so.
- **The tailnet is never cut**: the gate always admits your machines, and the circuit breaker only cuts Funnel.
- **Checked inputs**: only addresses or networks in canonical form reach HAProxy; the names declared
  by tailnet machines are cleaned before being displayed.
- **Audit**: the code was audited (claude-security, 2026-11-25); the 7 issues found, none of which could be exploited
  remotely by a visitor, were fixed the same day.
- Test first on a test machine or in observation mode, and use the RFC 5737 documentation networks
  for IPv4 tests: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Contents](#contents)

---

## Tests and quality

The suite has **179 tests**: domain, use cases, infrastructure (with a simulated Funnel), Textual screens with the
real stylesheets, init systems, security. The code is checked by `ruff`, `mypy` and `import-linter`
(layer rules). The `tests/` folder is included in the archive.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

Most tests need neither Tailscale, nor HAProxy, nor root.

[↑ Contents](#contents)

---

## Project status

### Operational points

- Full control of Tailscale: service, connection, settings, publishing, network, logs.
- HAProxy gate before TLS, in production since 2026-11-23, with rules, lists, groupings and attack mode.
- Survival: containment, circuit breaker, automatic watch.
- WireGuard port shield, in production since 2026-11-24.
- Report and TXT, HTML, JSON exports.
- Compatible with omega-connect and omega-fire.

### Known limitations

- Services under OpenRC and runit are covered by the tests, but not yet validated on a real machine.
- The gate protects a Funnel published over HTTPS on a single port, with the path `/`.
- The groupings require HAProxy compiled with Lua; without Lua, the gate works without them.
- The shield cannot be set up on a kernel updated without a reboot (missing modules): the screen says so.
- An attack that saturates the Internet line itself remains out of reach of a tool installed on the machine.
- The throughput of a site published through Funnel remains limited by Tailscale's relays and by the router.

[↑ Contents](#contents)

---

## Uninstallation

First remove, from omega-tail, what was put in place on the system, in this order:

1. **Funnel firewall → Disable protection** (Funnel is put back as before).
2. **Survival → Disable watch**.
3. **Survival → WireGuard port shield → Remove**.
4. **Survival → Remove containment**.

Then delete the folder:

```bash
rm -rf ~/omega-tail
```

Delete by hand the exports placed elsewhere, the `omega-tail` alias from `~/.bashrc` or `~/.zshrc`, and, if you
had enabled it, the `/etc/sysctl.d/99-omega-tail-forwarding.conf` file. Tailscale's operator right is removed
with `sudo tailscale set --operator=`.

[↑ Contents](#contents)

---

## License

Omega-Tail is distributed under the **MIT** license. See the [`LICENSE`](../../../LICENSE) file for the full text.

The AS / country database uses IP Geolocation by [DB-IP](https://db-ip.com), under the
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.

[↑ Contents](#contents)

---

> **Omega-Tail — Control Tailscale, protect Funnel.**
>
> A TUI interface for Tailscale, and a gate that refuses abuse before any encryption.
