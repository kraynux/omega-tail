<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**TAILSCALE 管理工具，内置 FUNNEL 防火墙**

OMEGA-TAIL 是 OMEGA 套件中的一款工具：它在一台机器上管理 **Tailscale**，并在该机器通过 **Tailscale Funnel** 向互联网发布服务时为其提供**防护**。

> 由 [kraynux](https://github.com/kraynux) 为 [Omega-Server](https://kraynux.snake-mackarel.ts.net) 打造 · [官方页面](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/zh-CN/) · [截图](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 界面、文档、导出和访客页面提供 **17 种语言** —— 参见 [界面语言](#界面语言)。  
**语言：**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** 是一个基于 [Textual](https://textual.textualize.io/) 构建的 Python TUI（终端用户界面）应用程序。它让您在一个界面中以高级模式管理和调整 **Tailscale**，无需记住任何一条命令。它还为 **Funnel** 模式增加了多项防护（防火墙、资源约束、生存保障……），因为该模式会把机器上的某个服务开放给整个互联网。

每个会改变机器的操作都会先显示其命令。sudo 密码在终端中逐个操作输入，未经您同意，任何东西都不会在后台运行。

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/zh-CN/omega-tail/F.png" width="32%" />
</p>

本项目依据 **Clean Architecture（整洁架构）** 原则设计，以 `app/` 作为组合根：业务领域、编排逻辑、基础设施与界面相互分离。

## 目录

- [简介](#简介)
- [理解 Tailscale 与 Funnel](#理解-tailscale-与-funnel)
- [功能](#功能)
- [防护详解](#防护详解)
- [实测数据](#实测数据)
- [架构](#架构)
- [前置条件](#前置条件)
- [安装](#安装)
- [使用方法](#使用方法)
- [主题与终端](#主题与终端)
- [文件、服务与兼容性](#文件服务与兼容性)
- [安全性](#安全性)
- [测试与质量](#测试与质量)
- [项目状态](#项目状态)
- [卸载](#卸载)
- [许可证](#许可证)

---

## 简介

### 为什么需要 omega-tail

Tailscale Funnel 无需在路由器（光猫）上开放端口即可把机器上的服务发布到互联网：访客经由 Tailscale 的中继进入。从网络角度看，这既简单又安全，但仍存在一个弱点。

- **加密的开销。** 在默认的 Funnel 模式下，由机器上的 `tailscaled` 服务为每位访客完成 TLS 握手。在一台小型机器上实测，这大约占**一次连接开销的 80 %**。每秒几百个新连接就足以让处理器满载：一台普通电脑，配上一个简单的脚本，就能让网站和机器一起瘫痪。
- **看不见的访客。** 常用的防火墙（nftables、ufw、fail2ban）看不到这些访客：他们经由 Tailscale 隧道以加密形式到达，显示的是中继的地址。
- **分散的设置。** Tailscale 的设置（操作员、出口节点、路由、SSH、护盾……）数量众多，分散在命令和网页控制台之间，其中一些还可能中断当前会话。

### 目标

- 完全通过一个界面管理 Tailscale，每项设置都附有一句说明。
- 在任何加密**之前**拒绝滥用连接，并能看到每位访客的真实地址。
- 在遭受攻击时保持机器正常运行：管理通道和其他服务仍然可以访问。
- 绝不强加任何东西：先建议、显示命令、征求同意，并且可以回退。
- 可在任何 Linux 发行版上运行，支持 systemd、OpenRC 或 runit。

### omega-tail 能做什么

- 显示 Tailscale、机器以及已发布内容的状态，并附有可直接跳转到修正界面的警报。
- 启动、停止和重启 `tailscaled`，如果您的会话经由 Tailscale，则提供安全护栏。
- 管理连接、账户以及 `tailscale set` 的全部设置，应用前先行校验。
- 发布、撤下、暂停和测试 Serve 与 Funnel 的服务，带有备份与恢复。
- 显示 tailnet 中的设备、它们的路径（直连或中继）、网络诊断以及日志。
- 在 Funnel 与您的网站之间放置一道 HAProxy **闸门**：按地址、按前缀的规则，全局预算，信任列表和黑名单，按 JA4 指纹、来源网络（AS）和国家进行分组，自动攻击模式。
- 对 `tailscaled` 施加资源约束，暂时或彻底切断 Funnel，并可借助自动值守自行完成这些操作。
- 用一张 nftables 表保护 `tailscaled` 的 WireGuard 端口（护盾）。
- 生成一份关于机器和最近 7 天攻击情况的报告，格式为 TXT、HTML 或 JSON。

### 本项目不做什么

- 它不取代 Tailscale：它只是管理 Tailscale。
- 它无法防御让互联网线路本身（路由器、链路）饱和的流量型攻击。
- 它不管理 Tailscale 的网页管理控制台（访问策略、出口节点审批、为 tailnet 启用 Funnel）。
- 它不保护通过 Funnel 以外方式发布的服务：这些端口请交给 omega-fire。
- 它从不以 root 身份运行，未经您同意不会在后台运行任何东西。
- 它不支持 Windows 和 macOS。

[↑ 目录](#目录)

---

## 理解 Tailscale 与 Funnel

omega-tail 需要用到一些 Tailscale 的概念。本节把它们集中在一起，不需要任何其他前提知识。

### 术语

| 术语 | 含义 |
|---|---|
| **Tailnet** | 您的 Tailscale 私有网络：连接到同一账户（或同一组织）的所有机器。每台机器在其中获得一个 `100.x.y.z` 地址（范围 100.64.0.0/10）和一个位于 `fd7a:115c:a1e0::/48` 的 IPv6 地址。 |
| **`tailscaled`** | 在机器上运行的服务（守护进程）：它维护 WireGuard 加密隧道、Tailscale 的网络栈，并为 Serve 和 Funnel 充当通往您服务的中继。 |
| **`tailscale`** | 管理 `tailscaled` 的命令（`tailscale status`、`tailscale set`、`tailscale funnel`…）。omega-tail 代您使用它。 |
| **WireGuard** | 机器之间使用的加密隧道协议。为此 `tailscaled` 监听一个 UDP 端口（默认 41641），该端口通常由路由器自动打开（UPnP）。 |
| **DERP 中继（DERP relay）** | Tailscale 的服务器，在两台机器无法直接互通（NAT 难以穿透）时转发流量。「直连」路径更快。 |
| **MagicDNS** | tailnet 中机器的名称，形式为 `machine.nom-du-tailnet.ts.net`。 |
| **Serve** | **仅对 tailnet** 发布一个本地服务（网站、API……），使用 HTTPS 和有效的 `*.ts.net` 证书。 |
| **Funnel** | **对整个互联网**发布一个本地服务，地址为 `https://machine.nom-du-tailnet.ts.net`。只能开放 443、8443 和 10000 端口。 |
| **Funnel 中继（Funnel relay）** | Tailscale 的服务器，负责接收来自互联网的访客并把他们引入您的 tailnet（显示为「funnel-ingress-node」）。 |
| **操作员（operator）** | 被允许无需 sudo 即可调整 Tailscale 的 Linux 账户（`tailscale set --operator=…`）。omega-tail 会通过 sudo 提议设置一次。 |
| **出口节点（exit node）** | tailnet 中的一台机器，另一台机器让其全部互联网流量经由它通过（类似 VPN）。它必须在 Tailscale 控制台中获得批准。 |
| **通告的子网（subnet router）** | 一台机器让 tailnet 其余部分可以访问的本地网络（例如 `192.168.1.0/24`）。 |
| **护盾（shields up）** | Tailscale 的一项设置，拒绝所有来自 tailnet 的入站连接。 |
| **Tailscale SSH** | 由 Tailscale 提供、受 tailnet 策略授权的 SSH 服务器。 |
| **PROXY v2 头部** | 添加在连接开头的一小段头部，用于把访客的真实地址传给接收方。 |
| **JA4 指纹** | 某个软件建立 TLS 连接方式的特征签名：浏览器和攻击工具的指纹各不相同。 |
| **AS（自治系统）** | 一个地址的来源网络：网络接入商、托管商、云服务。 |

### 访客的路径

**默认的 Funnel，没有 omega-tail。** `tailscaled` 包揽一切：它解密 WireGuard 隧道，完成访客的 TLS 握手，然后以 HTTP 把请求转发到您的网站。机器上的任何防火墙都看不到访客，每个新连接都让 `tailscaled` 付出高昂的开销。

```text
访客 ──HTTPS──▶ Funnel 中继 ──WireGuard──▶ tailscaled (TLS + HTTP 中继) ──HTTP──▶ 您的网站
                (Tailscale)                └── 全部开销都在这里
```

**带有 omega-tail 闸门的 Funnel。** Funnel 切换到 TCP 模式：`tailscaled` 不再处理 TLS，而是把仍然加密的数据流转交给闸门，并在前面附上访客的真实地址（PROXY v2 头部）。闸门在任何加密**之前**做出决定：被拒绝的连接几乎没有开销，只有被放行的连接才会由 OpenSSL 解密，而 OpenSSL 比 `tailscaled` 的 TLS 更快。

```text
访客 ──HTTPS──▶ Funnel 中继 ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                │
                                                ▼
                                 omega-tail 闸门 (HAProxy, 127.0.0.1)
                                 ├── TLS 之前拒绝：黑名单、速率、预算、目标名称、分组
                                 └── 放行：TLS (证书 *.ts.net) ──HTTP──▶ 您的网站
```

闸门只监听机器的本地回环地址，并以您的账户运行。您 tailnet 中的机器总是先于任何规则被放行：只有 Funnel 的访客会被过滤。

### Tailscale 需要允许的内容（管理控制台）

这些设置只需在 Tailscale 的网页控制台中进行一次；omega-tail 不会更改它们。

- 为 tailnet 启用 **MagicDNS** 和 **HTTPS 证书**（Serve、Funnel 以及闸门的证书都需要它们）。
- 在 tailnet 的访问策略中为该机器**允许 Funnel**（属性 `funnel`）。
- 对于出口节点或通告的子网：在控制台中对它们进行**批准**。

[↑ 目录](#目录)

---

## 功能

主菜单分为两列，每列六项：**TAILSCALE** 用于管理，**防护** 用于防御。

### TAILSCALE

#### 1. 仪表板

- **Tailscale**：服务、连接状态、正在运行的版本和已安装的版本、机器名、地址、账户、在线设备、密钥到期时间、操作员、提供的和正在使用的出口节点、通告的子网。
- **机器**：整台机器的 CPU、每个核心的负载、温度、内存、`tailscaled` 的 CPU 和内存、资源约束，然后是各项防护的状态（Funnel、防火墙和攻击模式、黑名单、值守、护盾）。
- **发布**：每个已发布的端口，面向互联网（Funnel）还是面向 tailnet（Serve），其模式和目标。
- **警报**，按严重程度从高到低排列，并带有「修正」按钮打开相应界面。例如：服务已停止、更新已安装但未生效、密钥即将到期、Funnel 已发布但无防护、温度过高、`tailscaled` 占用过高或未受约束、黑名单持续增长。
- 数值根据阈值（CPU、负载、温度、内存、`tailscaled`）显示为绿色、橙色或红色。

#### 2. tailscaled 服务

- 初始化系统看到的状态、正在运行的版本和已安装的版本、启动命令、附加配置文件、资源约束。
- **启动**、**停止**、**重启**（例如为了应用已经安装的更新）。
- **安全护栏**：如果您的会话经由 Tailscale（通过 tailnet 的 SSH），「停止」会要求再次确认，因为停止后您将无法重新启动它。
- **修正启动**：找出在启动时执行 `tailscale up` 的附加配置文件，这种文件可能在第一次更改设置时让机器退出 tailnet；修正内容会先显示出来，原文件会被保留。

#### 3. 连接与设置

- **登录**、**登出**、**添加账户**、**切换账户**、**永久登出**（需输入机器名）。
- **`tailscale set` 的全部设置**，每项都附有一句说明：机器名和别名、路由、tailnet DNS、护盾、有状态过滤、netfilter 模式、出口节点、局域网访问、把本机提供为出口节点、通告的子网、Tailscale SSH、网页界面、更新、对等中继、操作员。
- 输入时，一个框会显示**修改前 → 修改后**以及对应命令；应用后，每个重新读取的值都会标记为 ✔（已生效）或 ✖（未生效）。
- 当某项更改可能中断经由 Tailscale 的会话时，会显示警告。
- **IP 转发**：当机器充当出口节点或通告子网时，一键启用。

#### 4. 发布

- 机器发布的全部内容：端口、公开（Funnel）或 tailnet（Serve）、模式、路径、目标、防护。
- 以 HTTPS、HTTP、TCP 或 TLS 终止方式**发布**本地服务；**撤下**；**暂停 Funnel** 和**恢复 Funnel**（与之前完全一致）。
- **端到端测试**：像访客一样发起一次真实连接（响应、耗时、证书、TLS 版本）。
- **备份**：每次更改之前的状态（最近 50 份），可以恢复。
- 每次更改都会经过校验；如有偏差，会重建发布配置，否则恢复之前的状态。

#### 5. 网络与设备

- tailnet 中的**设备**：系统、是否在线、路径（直连或经由中继）、最后一次出现时间、地址、交换的流量；Tailscale 的 Funnel 中继默认隐藏。
- **Tailscale Ping**（路径和延迟）、**这是谁？**（某个 tailnet 地址属于谁）。
- **网络诊断**：UDP、IPv4 / IPv6、NAT 类型、路由器开放端口的能力（UPnP、NAT-PMP、PCP）、最近的中继及延迟。
- **DNS**、**tailnet 锁** 和 Tailscale 的**内部计数器**。
- 只读：此界面中的任何内容都不会更改设置。

#### 6. 日志

- `tailscaled` 的日志（journalctl，或非 systemd 下服务的日志文件）和闸门的日志，可过滤、可导出。
- 每项信息都有自己的颜色，取自主题：日期、进程、消息类别（控制、网络、DNS、WireGuard 引擎）、粗体的地址、红色的错误、橙色的警告；闸门日志则为拒绝原因、分组、AS 和国家。

### 防护

#### 7. Funnel 防火墙

- 通过发行版的包管理器（pacman、apt、dnf、zypper、apk、xbps、emerge）**安装 HAProxy**。
- **启用防护**：`*.ts.net` 证书、列表、经过校验的配置、闸门服务、切换 Funnel，然后从互联网进行测试；一旦失败，立即恢复原来的发布配置。
- **停用防护**：Funnel 会被完全恢复到之前的状态，并经过校验。
- 热应用的**规则**，用于无风险地调整阈值的**观察**模式，**分组**（参见[防护详解](#防护详解)）。
- 在独立进程中**更新数据库** AS / 国家（DB-IP Lite）。

#### 8. 生存保障

- **`tailscaled` 资源约束**：CPU 上限、权重和优先级，可选择让 SSH 访问优先。
- **Funnel 断路器**：CPU 和温度阈值，切断 10 分钟（自动恢复）或彻底切断。
- **自动值守**：在无人值守时完成同样的事情。
- **WireGuard 端口护盾**：通往其专属界面的按钮（观察、生效、部署、重新部署、移除、移交）。

#### 9. 攻击与决策

- 闸门的计数器（已接收、加密前拒绝、已放行、进行中）以及最活跃的地址，每 2 秒刷新一次，附带每个地址的国家、AS 和状态。
- **封锁**、**黑名单**、**解除封锁**、**信任**：立即生效，无需重启闸门；通知会用一行说明所执行的操作以及该地址所处的位置。
- **指纹**、**AS** 和**国家**视图；攻击模式的状态以及被分组规则拒绝的连接。
- **黑名单管理**：带有添加日期和来源的完整列表，添加、删除、导入 TXT 文件（重复项、已被覆盖的网络和 tailnet 地址会被排除），带预览的清除（按时长、最早的 N 条、某个行范围、某个来源、全部），导出为 TXT（可重新导入）、HTML 和 JSON。上限为 50 000 条。

#### 10. 报告

- omega-tail 所掌握的关于机器的一切事实：Tailscale、发布、机器、防火墙、生存保障、警报，以及从闸门日志中读取的**最近 7 天的攻击**。
- **隐私**：默认不包含 Tailscale 账户，也不包含 tailnet 中设备的名称和地址，便于发送给他人。
- 导出为 **TXT**、**HTML**（主题可选）和 **JSON**；**查看导出**会在浏览器中打开导出目录。

#### 11. 设置

- 界面和导出的语言、界面和导出的主题、导出目录和截图目录，以及它们的清理。

#### 12. 帮助

- 每个界面一节，快捷键，命令行，以及**联系与支持**。

[↑ 目录](#目录)

---

## 防护详解

每项防护都针对一种明确的威胁；没有任何一项是强制的。

| 防护 | 针对什么 | 位置 |
|---|---|---|
| 闸门（规则） | 来自一个或少数几个地址的突发流量，不以本网站为目标的连接 | Funnel 防火墙 |
| 分组 | 地址分散的攻击（成千上万个地址，每个一次连接） | Funnel 防火墙 |
| 黑名单 | 已知会发动攻击的地址和网络，长期保留 | 攻击与决策 |
| 资源约束 | 遭受攻击时可能占满整台机器的 `tailscaled` | 生存保障 |
| 断路器 | 机器仍然满载：暂时切断 Funnel | 生存保障 |
| 自动值守 | 同上，在无人值守时 | 生存保障 |
| WireGuard 护盾 | 发往 `tailscaled` 端口的 UDP 洪流，无论 Funnel 是否开启 | 生存保障 |

### 闸门（Funnel 防火墙）

规则按以下顺序应用，全部在加密之前：

1. **tailnet 中的机器**（100.64.0.0/10、fd7a:115c:a1e0::/48）：始终放行。
2. **信任列表**：永不受限。**黑名单**：在移出之前一律拒绝。
3. **按地址的速率**（默认 10 秒 40 个连接）：超过后，该地址会在所选时长内被封锁（默认 60 分钟）。
4. **按前缀的速率**：IPv4 为 /24，IPv6 为 /64。
5. 每秒放行连接数的**全局预算**：处理器永远不会过载。
6. **目标名称**：未以本机名称为目标的连接会被拒绝。

闸门的 `*.ts.net` 证书向 Tailscale 申请，每天检查一次，并在到期前 30 天热更新。**观察**模式会统计一切，但不拒绝任何连接。

### 分组（指纹、AS、国家）

面对地址分散的攻击，按地址的规则对每个地址只能看到一次。因此闸门还会按客户端的 **JA4 指纹**、**AS** 和**国家**进行分类，并统计每个分组的速率。

- **自动攻击模式**：当每秒入站连接超过 80 个（可调）时，闸门会自行进入攻击模式，平静 5 分钟后退出。
- 仅在攻击模式下：激增的未知指纹、托管商或云服务的 AS（列表可修改），或您列表中的国家（默认为空），一旦超过其速率就会被拒绝。
- **常见浏览器**（Chrome、Edge、Firefox）从不受这些规则影响；**已知客户端**（最近 24 小时内被放行过的）优先于全局预算。
- **学习期**：在 7 天内，闸门会学习您网站的常见指纹（攻击期间从不学习）；在此之前，分组保持在观察模式。
- 非攻击期间，每十个连接分类一个；攻击期间，全部分类。
- AS / 国家数据库为 **DB-IP Lite**，每月下载和更新一次。

### 生存保障

- **资源约束**：一个单独的附加配置文件为 `tailscaled` 设置上限（例如在 4 线程的机器上限制为一整个核心），并降低其优先级。您自己的配置绝不会被修改。
- **断路器**：当 `tailscaled` 持续高于 CPU 阈值（默认 60 秒内占一个核心的 80 %）或温度达到 85 °C 时，omega-tail 会建议切断 Funnel 10 分钟（自动恢复，与之前完全一致，即使 omega-tail 已关闭），或彻底切断，或者等待。tailnet 永远不会被切断。
- **自动值守**（默认停用）：一个以您的账户运行的服务会在三次超限后自行切断 Funnel，第一次 15 分钟，第二次 30 分钟，之后一小时，并自行恢复。

### WireGuard 端口护盾

`tailscaled` 每秒在其 UDP 端口上接收 100 000 个数据包时，大约会消耗一个处理器核心，即使这些数据包无效。护盾是一张放在它前面、作用于网卡的 nftables 表：

- **已知对等节点**（`tailscaled` 正在与之通信的节点）永不受限；
- 握手被限制为每个来源每秒 20 次；
- 其他来源有一个预算（每个来源每秒 500 个数据包，总计 5 000 个）；
- 不是 WireGuard 的数据包会被拒绝。

它先以**观察**模式部署，再切换为**生效**。如果通过 omega-connect 关联，**omega-fire**（3.7.0 或更高版本）可以代替 omega-tail 部署和管理它：这是同一张表，管理方更换时表本身不受触动。

[↑ 目录](#目录)

---

## 实测数据

omega-tail 的各项选择来自实测，测试机器与它所保护的机器属于同一代（2010 至 2016 年的处理器，大多没有 AES 加速）。

| 测量项 | 结果 |
|---|---|
| 默认 Funnel 下 TLS 在一次连接开销中所占比例 | 约 80 % |
| 被闸门**拒绝**的连接的开销，与默认 Funnel 相比 | **低 4.6 倍** |
| 被闸门**放行**的连接的开销，与默认 Funnel 相比 | **低 2 倍** |
| 使用闸门时的吞吐量，保持连接（与 `tailscaled` 这类 Go 实现的 TLS 相比） | 请求数 **+15 %**，CPU −20 % |
| WireGuard 护盾：原本占用 `tailscaled` 一整个核心的洪流 | 一个核心的 **1 %** |
| 服务的内存占用（闸门、值守、护盾） | 约 67 MB |

因此闸门不会降低网站的吞吐量：在这些机器上，无论是否使用 omega-tail，限制因素都是加密本身；而在生产环境中，Funnel 无论如何都要经过 Tailscale 的中继和路由器。

[↑ 目录](#目录)

---

## 架构

```text
src/omega_tail/
├── app/              组合根：组装各层，入口点（界面、命令行）
├── core/             共享常量
├── domain/           纯业务逻辑：闸门规则、警报、断路器、值守、黑名单……
├── application/      用例：发布、防火墙、生存保障、报告、设置
├── ports/            应用层所需的契约（Protocol）
├── infrastructure/   Tailscale、HAProxy、nftables、systemd / OpenRC / runit、日志、导出、Lua 脚本
├── interfaces/       tui/（Textual）、cli/（命令行）、shared/（帮助、报告、展示）
└── shared/           语言（gettext）
```

### 设计原则

- `domain/` 不包含任何读写操作：其中的一切都可以在没有机器的情况下测试。
- `application/` 借助领域层和端口编排用例；界面和命令行调用的是相同的用例。
- 只有 `infrastructure.commands` 和 `infrastructure.privileged` 会执行命令；界面从不直接执行命令。这些规则会被自动检查（import-linter）。
- 界面基于 [omega-lib](https://github.com/kraynux)，即整个 OMEGA 套件共享的库（主题、终端检测、语言、联系与支持、WireGuard 护盾）。它没有发布到 PyPI：它随归档一起提供（`vendor/omega-lib/`）。
- 所有耗时的调用（Tailscale、HAProxy、磁盘、网络）都在后台任务中运行：界面永远不会卡住。

[↑ 目录](#目录)

---

## 前置条件

### 系统

- Linux，任何发行版（已在 Arch Linux 及其衍生版上测试）。
- Python 3.10 或更高版本，并带有 `venv` 模块。
- 一个初始化系统：**systemd**、**OpenRC** 或 **runit**。
- 用于改变机器的操作的 `sudo`（逐个操作请求，启动时从不请求）。
- 一个至少 80×24 的终端（参见[主题与终端](#主题与终端)）。

### Tailscale

- 已安装并已连接的 **Tailscale**（`tailscale` 客户端和 `tailscaled` 服务）；已使用 1.104 版本测试。
- 对于 Funnel：在 Tailscale 控制台中允许 MagicDNS、HTTPS 证书和 Funnel（参见 [Tailscale 需要允许的内容](#tailscale-需要允许的内容管理控制台)）。

### Python 依赖

由 `install.sh` 安装到虚拟环境中：

- `textual`：界面。
- `omega-lib`：OMEGA 套件的共享库，随归档一起提供。

### 必需组件与可选组件

omega-tail 会检测已存在的组件，只启用可用的功能。

| 组件 | 作用 | 状态 |
|---|---|---|
| Tailscale（`tailscale`、`tailscaled`） | omega-tail 所管理的一切 | **必需** |
| Python 3.10+、`textual`、`omega-lib` | 应用程序本身 | **必需** |
| systemd、OpenRC 或 runit | 闸门、值守、护盾的服务 | **必需**（三者之一） |
| HAProxy 3.x | Funnel 防火墙的闸门 | 可选（可从 omega-tail 中安装） |
| 带 Lua 的 HAProxy | 分组（指纹、AS、国家） | 可选（常见发行版的情况） |
| nftables（内核带 `nft_limit`） | WireGuard 端口护盾 | 可选 |
| 读取系统日志的权限（`systemd-journal`、`adm` 或 `wheel` 组） | 日志、攻击报告 | 推荐 |
| 浏览器和桌面环境 | 在浏览器中「查看导出」（否则在 omega-tail 中阅读） | 可选 |
| omega-connect | 登记簿、同步、套件更新 | 可选 |
| omega-fire 3.7.0+ | 从 omega-fire 管理 WireGuard 护盾 | 可选 |

[↑ 目录](#目录)

---

## 安装

官方归档以 `.tar.gz` 格式提供。安装前请使用同时发布的 `sha.txt` 文件校验其完整性：

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **以下三种方法用于首次安装。** 如果 `~/omega-tail` 已经存在，请参阅[更新](#更新)一节。切勿在已有的 `omega-tail` 目录内部重新执行这些命令：`tar` 会创建一个嵌套的 `omega-tail/omega-tail/`。

安装的任何步骤都不需要 root 权限：omega-tail 以普通用户身份运行。

### 方法一 — 安装脚本

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ 您似乎已经位于 omega-tail 目录内 —— 请参阅 README 的更新章节。" >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ 已在此解压，跳过此步骤。" || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail 已存在，跳过移动。" || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

该脚本会创建虚拟环境，安装依赖（先安装随附的 omega-lib），使启动脚本可执行，写入供 omega-connect 读取的安装令牌，并提议创建 `omega-tail` 别名。它可以安全地重复运行。

### 方法二 — 完整的可重复安装

此命令可以重复执行：它会跳过已经完成的步骤。

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ 您似乎已经位于 omega-tail 目录内 —— 请参阅 README 的更新章节。" >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail 已存在，跳过解压。" || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv 已存在，跳过此步骤。" || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail 已安装。运行 ./omega-tail.sh。"
```

### 方法三 — 详细安装

```bash
# 0. 确认没有在已存在的 omega-tail 目录内重新执行本流程
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ 您似乎已经位于 omega-tail 目录内 —— 请参阅 README 的更新章节。" >&2; exit 1; }

# 1. 解压
[ -d omega-tail ] && echo "ℹ️ 已在此解压，跳过此步骤。" || tar -xzf omega-tail-0.7.0.tar.gz

# 2. 移动到主目录
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail 已存在，跳过移动。" || mv omega-tail ~/

# 3. 进入项目目录
cd ~/omega-tail/

# 4. 创建虚拟环境
[ -f .venv/bin/activate ] && echo "ℹ️ .venv 已存在，跳过创建。" || python3 -m venv .venv

# 5. 安装依赖（先安装随附的 omega-lib）
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. 使启动脚本可执行
chmod +x omega-tail.sh install.sh

# 7. 写入安装令牌（供 omega-connect 读取；可选）
./omega-tail.sh synchro jeton

# 8. 启动
./omega-tail.sh
```

在 Debian、Ubuntu 及其衍生版上，`venv` 模块并不总是随 Python 一起安装：`sudo apt install python3-venv`。

### 更新

omega-tail 的服务（闸门、值守）使用 `~/omega-tail/var/` 中的文件。因此更新时必须**保留该目录**：归档中不包含 `var/`，并直接解压覆盖到现有安装之上。

请在存放归档的目录中操作，该目录**不能是 `~/omega-tail`**：

```bash
# 1. 备份当前安装（包括 var/）
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. 将新版本解压覆盖到原处（var/ 会被保留）
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. 重新安装（依赖、启动脚本、安装令牌）
cd ~/omega-tail
./install.sh

# 4. 重新启动 omega-tail
./omega-tail.sh
```

如果闸门处于启用状态，**Funnel 防火墙 →「应用规则」** 会用新版本热重新生成其配置。如果已启用自动值守，**生存保障 →「启用值守」** 会用新代码重新启动它。omega-connect 也可以执行更新（Updater 界面）。

### Bash 或 Zsh 别名

`install.sh` 会提议创建别名。如需手动添加：

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

别名叫 `omega-tail` 而不是 `tail`，以免遮蔽系统命令 `tail`。

[↑ 目录](#目录)

---

## 使用方法

### 启动

```bash
cd ~/omega-tail
./omega-tail.sh

# 或者，如果已创建别名，直接输入：
omega-tail
```

启动脚本不要求任何提权：omega-tail 以您的账户运行，只有需要 sudo 的操作才会在终端中请求 sudo，并事先显示命令。

### 推荐的入门步骤

要保护一个通过 Funnel 发布的网站，请按以下顺序操作：

1. **仪表板**：阅读警报；**成为操作员**（通过 sudo，仅一次），以便无需 sudo 调整 Tailscale。
2. **生存保障 → 应用资源约束**：`tailscaled` 将无法再占满整台机器。
3. **发布**：以 **HTTPS 在 443 端口**发布网站，路径为 `/`，然后进行**端到端测试**。
4. **Funnel 防火墙 → 安装 HAProxy**，然后**启用防护**，先使用**观察**模式。
5. 几天之后，查看**攻击与决策**：如果计数器只显示滥用流量，就把闸门切换到**正常**模式。
6. 让**分组**在观察模式下学习 7 天，然后把它们切换为**应用**。
7. **生存保障 → WireGuard 端口护盾**：先以观察模式部署，然后切换为生效。
8. 对于无人值守的机器：**生存保障 → 启用值守**。

### 界面语言

17 种语言：法语、英语、西班牙语、葡萄牙语（巴西）、意大利语、德语、荷兰语、波兰语、俄语、中文、越南语、泰语、印度尼西亚语、日语、韩语、印地语、阿拉伯语。

- 在设置中选择（`s` 键，「Langue / Language」，该标签从不翻译），只需重启界面即可生效。
- 临时指定：`OMEGA_TAIL_LANG=en ./omega-tail.sh`。
- 在 Linux 文本控制台（TTY）中，控制台字体不包含其文字的语言在本次会话中以英语显示；阿拉伯语从右向左显示。
- **导出语言**（报告、黑名单、日志）单独设置，默认为「与界面相同」。

### 联系与支持

帮助（`a` 键）提供 **联系与支持** 界面：

- *请我喝杯咖啡*（开发者的 PayPal 页面）；
- *联系支持*（邮箱地址和网站表单，以明文显示）；
- *登记为用户（匿名）*；
- *检查更新*。

登记是自愿的，默认关闭，并且只发送一次。它仅用于统计用户数量，以及（如您愿意）其所在的大洲或国家（封闭列表，绝无自由文本）。它发送一个随机生成的密钥、软件名称（`omega-tail`）及其版本，绝不发送姓名、机器名、设置或 tailnet 地址。可随时在同一界面中撤回（*不再登记我*）。检查更新只会读取网站上发布的版本列表，且不点击就绝不执行。

### 与其他 omega 工具的联动

- **omega-connect**：`install.sh` 会写入一个安装令牌（`var/omega-jeton.json`），描述该工具及其版本，不执行任何东西。omega-connect 将其用于登记簿、同步、修复、更新和安装。`./omega-tail.sh synchro jeton` 可手动重新写入它。
- **omega-fire**（3.7.0 或更高版本）通过 omega-connect 关联后，可以部署和管理 WireGuard 端口护盾；其规则列表会显示该护盾，并标明来源为 omega-tail。

### 命令行

所有命令的写法都是 `./omega-tail.sh …`（使用别名时为 `omega-tail …`）：

| 命令 | 作用 |
|---|---|
| `omega-tail` | 界面 |
| `omega-tail etat [--format json]` | Tailscale、机器的状态以及警报，以文本或供脚本使用的格式输出 |
| `omega-tail aide` | 文本形式的完整帮助 |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | 报告，显示或保存 |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | 切断或恢复 Funnel |
| `omega-tail veille etat` | 自动值守的状态及其最近几行日志 |
| `omega-tail porte etat` | 闸门的状态和计数器 |
| `omega-tail porte certificat [--si-besoin]` | 更新闸门的 `*.ts.net` 证书 |
| `omega-tail porte groupes` | 分组：攻击模式、指纹、AS、国家 |
| `omega-tail porte base` | 更新 AS / 国家数据库 |
| `omega-tail porte bloquer ADRESSE [--toujours]` | 封锁一个地址或网络（使用 `--toujours` 时加入黑名单） |
| `omega-tail porte debloquer ADRESSE` | 解除封锁 |
| `omega-tail porte confiance ADRESSE` | 加入信任 |
| `omega-tail synchro jeton` | 写入安装令牌（omega-connect） |
| `omega-tail --version` | 版本 |

### 总体流程

1. 启动画面，然后是分为两列（TAILSCALE 和 防护）的主菜单。
2. 在每个界面的标题下方，**状态栏**汇总一切：服务、机器和 `tailscaled` 的 CPU、温度、内存、Funnel、防火墙、值守、连接。它每 5 秒刷新一次。
3. 每个会改变机器的操作都会先显示其命令，然后请求确认；sudo 在终端中输入，之后界面会恢复。
4. 敏感操作（永久登出、彻底清空黑名单）需要输入一个词进行确认。
5. 结果以一行显示，并根据重新读取的状态进行校验。

### 导航

- 上 / 下方向键：在元素之间移动（表格的行、按钮）。
- Tab / Shift+Tab：在界面的各区域之间切换。
- Enter 或点击：激活所选按钮；在警报表格中为「修正」。
- `Esc`：返回上一个界面（在主菜单中：退出）。
- `a`：帮助，可在任意界面使用。
- `s`：设置，可在任意界面使用。
- `t`：下一个主题（会被保存）。
- `r`：重绘界面，显示终端尺寸并重新读取状态。
- `q`：退出，需确认。
- `Ctrl+P`：命令（主题、以 SVG 格式截图并保存到截图目录、退出）。

[↑ 目录](#目录)

---

## 主题与终端

十种 `omega-*` 主题与 OMEGA 套件的其余工具共享：

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- 使用 `t` 在各主题之间切换，或在设置（`s`）中选择一个主题；所选主题会被保存。
- HTML 导出有其自己的主题：`omega-base`、`omega-burn`、`omega-neon`、`light-basic`、`light-alt`。
- omega-tail 会通过一个**渲染配置**，根据检测到的终端调整视觉复杂度：完整、标准、精简或单色（仅 ASCII）。

| 最小尺寸 | 配置 | 典型终端 |
|---|---|---|
| 120×32 及以上 | 完整 | Ghostty、Alacritty、WezTerm、Kitty |
| 100×28 及以上 | 标准 | Konsole、GNOME Terminal、Terminator、xfce4-terminal |
| 80×24 及以上 | 精简 | urxvt、xterm、现代 SSH |
| 低于 80×24 | 单色（仅 ASCII） | Linux TTY、旧版 SSH |

调整窗口大小后，`r` 会重新读取终端尺寸；尺寸显示在顶部，主题旁边。

[↑ 目录](#目录)

---

## 文件、服务与兼容性

### omega-tail 目录中

omega-tail 的全部状态都位于 `~/omega-tail/var/` 中，启动时会重新创建，并且从不发布：

```text
var/
├── settings.json         设置（语言、主题、目录、阈值、闸门规则）
├── omega-jeton.json      安装令牌（omega-connect）
├── porte/                闸门配置、证书、信任列表和黑名单、AS / 国家数据库
├── veille/               自动值守日志
├── survie/               被修改文件的原件、断路器状态
├── funnel/sauvegardes/   每次更改之前的发布配置（最近 50 份）
├── exports/              导出的报告、日志和列表
└── screenshots/          截图（Ctrl+P）
```

### 系统中（仅当您启用相应防护时）

每个文件都通过 sudo 放置，事先显示命令，并可通过 omega-tail 中的相反操作移除。

| 文件或服务 | 放置者 | 移除者 |
|---|---|---|
| `omega-tail-porte` 服务（systemd、OpenRC 或 runit）和 `omega-tail-porte-certificat`（systemd 定时器，或您 crontab 中带标记的一行） | 启用防护 | 停用防护 |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf`（或非 systemd 下的控制组） | 应用资源约束 | 移除资源约束 |
| `omega-tail-retablir-*` 定时器（切断后的自动恢复） | 断路器 | 切断结束 |
| `omega-tail-veille` 服务 | 启用值守 | 停用值守 |
| `omega-bouclier-wg` 服务、nftables 表、`/etc/omega-bouclier-wg/` | 护盾：部署 | 护盾：移除 |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | 启用 IP 转发 | 删除该文件 |

`tailscaled` 的 `override.conf` 文件（如果存在）绝不会被修改。

### 初始化系统

| | systemd | OpenRC | runit |
|---|---|---|---|
| `tailscaled` 服务 | `systemctl` | `rc-service` | `sv` |
| 日志 | `journalctl` | 服务的日志文件 | `svlogd`、`socklog` |
| 资源约束 | systemd 附加配置文件 | 控制组（cgroup v2） | 控制组（cgroup v2） |
| 暂时切断 | systemd 定时器 | 以您的账户运行的分离进程 | 以您的账户运行的分离进程 |
| 闸门、值守、护盾 | systemd 服务 | OpenRC 服务 | runit 服务 |

在非 systemd 系统上，如果 `tailscaled` 重启，基于控制组的资源约束会丢失：此时会出现警报，建议重新应用。

### IPv4 与 IPv6

闸门、列表、分组和护盾都会处理这两个地址族。统计所用的前缀在 IPv4 中为 /24，在 IPv6 中为 /64；以 `::ffff:a.b.c.d` 形式出现的 IPv4 地址按 IPv4 地址处理。

[↑ 目录](#目录)

---

## 安全性

omega-tail 作用于一个暴露在互联网上的服务；它的设计原则是绝不让情况变得更糟。

- **从不使用 root**：应用程序、HAProxy 闸门和值守都以您的账户运行；只有放置或移除服务时才请求 sudo，并事先显示命令。
- **私有通道**：闸门的管理套接字权限为 600，位于权限为 700 的目录中；其表的同步通过同一目录中的一个套接字进行。
- **回退**：每次切换 Funnel 都会先备份并经过校验，一旦失败就恢复之前的状态。
- **先观察**：闸门、分组和护盾都先以观察模式部署；在您做出决定之前，不会拒绝任何连接。
- **tailnet 永远不会被切断**：闸门始终放行您的机器，断路器只切断 Funnel。
- **输入校验**：只有规范形式的地址或网络才会传给 HAProxy；tailnet 中机器所声明的名称在显示前会被清理。
- **审计**：代码已经过审计（claude-security，2026-11-25）；发现的 7 个问题（均无法被访客远程利用）已于当天全部修复。
- 请先在测试机器上或以观察模式进行测试，并在 IPv4 测试中使用 RFC 5737 规定的文档专用网段：`192.0.2.0/24`、`198.51.100.0/24`、`203.0.113.0/24`。

[↑ 目录](#目录)

---

## 测试与质量

测试套件共有 **179 个测试**：领域层、用例、基础设施（使用模拟的 Funnel）、使用真实样式表的 Textual 界面、初始化系统、安全性。代码由 `ruff`、`mypy` 和 `import-linter`（分层规则）检查。`tests/` 目录包含在归档中。

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

大多数测试既不需要 Tailscale，也不需要 HAProxy 或 root。

[↑ 目录](#目录)

---

## 项目状态

### 可用功能

- 完整管理 Tailscale：服务、连接、设置、发布、网络、日志。
- 位于 TLS 之前的 HAProxy 闸门，自 2026-11-23 起投入生产，带有规则、列表、分组和攻击模式。
- 生存保障：资源约束、断路器、自动值守。
- WireGuard 端口护盾，自 2026-11-24 起投入生产。
- 报告以及 TXT、HTML、JSON 导出。
- 与 omega-connect 和 omega-fire 兼容。

### 已知限制

- OpenRC 和 runit 下的服务已被测试覆盖，但尚未在真实机器上验证。
- 闸门保护的是以 HTTPS 发布在单个端口上、路径为 `/` 的 Funnel。
- 分组需要编译时带有 Lua 的 HAProxy；没有 Lua 时，闸门照常工作，只是没有分组功能。
- 在内核已更新但尚未重启的系统上无法部署护盾（缺少模块）：界面会提示这一点。
- 让互联网线路本身饱和的攻击，超出了安装在机器上的工具的能力范围。
- 通过 Funnel 发布的网站的吞吐量仍受 Tailscale 中继和路由器的限制。

[↑ 目录](#目录)

---

## 卸载

请先在 omega-tail 中按以下顺序移除已放置到系统中的内容：

1. **Funnel 防火墙 → 停用防护**（Funnel 会恢复到之前的状态）。
2. **生存保障 → 停用值守**。
3. **生存保障 → WireGuard 端口护盾 → 移除**。
4. **生存保障 → 移除资源约束**。

然后删除目录：

```bash
rm -rf ~/omega-tail
```

请手动删除导出到其他位置的文件、`~/.bashrc` 或 `~/.zshrc` 中的 `omega-tail` 别名，以及（如果您曾启用）`/etc/sysctl.d/99-omega-tail-forwarding.conf` 文件。Tailscale 的操作员权限可通过 `sudo tailscale set --operator=` 撤销。

[↑ 目录](#目录)

---

## 许可证

Omega-Tail 依据 **MIT** 许可证发布。完整文本请参见 [`LICENSE`](../../../LICENSE) 文件。

AS / 国家数据库使用 [DB-IP](https://db-ip.com) 提供的 IP Geolocation，采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可证。

[↑ 目录](#目录)

---

> **Omega-Tail —— 管理 Tailscale，保护 Funnel。**
>
> 一个用于 Tailscale 的 TUI 界面，以及一道在任何加密之前拒绝滥用的闸门。
