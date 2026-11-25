<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**FUNNEL용 방화벽을 통합한 TAILSCALE 제어 관리자**

OMEGA-TAIL은 OMEGA 도구 모음 가운데 한 머신의 **Tailscale**을 제어하고, 그 머신이 **Tailscale Funnel**로 인터넷에
서비스를 게시할 때 머신을 **보호**하는 도구입니다.

> [kraynux](https://github.com/kraynux)가 [Omega-Server](https://kraynux.snake-mackarel.ts.net)를 위해 개발 · [공식 페이지](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/ko/) · [스크린샷](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 인터페이스, 문서, 내보내기, 방문자 페이지를 **17개 언어**로 제공합니다 — [인터페이스 언어](#인터페이스-언어)를 참조하십시오.  
**언어:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL**은 [Textual](https://textual.textualize.io/)로 만든 Python 기반 TUI(Terminal User Interface)
애플리케이션입니다. 명령을 하나도 외우지 않고 인터페이스에서 **Tailscale**을 고급 모드로 관리하고 설정할 수
있습니다. 또한 머신의 서비스를 인터넷 전체에 여는 **Funnel** 모드를 위해 보호 기능(방화벽, 자원 제한, 생존…)을
더합니다.

머신을 바꾸는 모든 작업은 먼저 그 명령을 보여 줍니다. sudo 비밀번호는 작업마다 터미널에서 입력하며, 여러분 모르게
백그라운드에서 실행되는 것은 없습니다.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ko/omega-tail/F.png" width="32%" />
</p>

이 프로젝트는 **Clean Architecture** 원칙에 따라 설계되었으며, `app/`이 구성 루트입니다: 비즈니스 도메인,
오케스트레이션, 인프라, 인터페이스가 분리되어 있습니다.

## 목차

- [소개](#소개)
- [Tailscale과 Funnel 이해하기](#tailscale과-funnel-이해하기)
- [기능](#기능)
- [보호 기능 상세](#보호-기능-상세)
- [측정](#측정)
- [아키텍처](#아키텍처)
- [사전 요구 사항](#사전-요구-사항)
- [설치](#설치)
- [사용법](#사용법)
- [테마와 터미널](#테마와-터미널)
- [파일, 서비스, 호환성](#파일-서비스-호환성)
- [보안](#보안)
- [테스트와 품질](#테스트와-품질)
- [프로젝트 상태](#프로젝트-상태)
- [제거](#제거)
- [라이선스](#라이선스)

---

## 소개

### omega-tail이 필요한 이유

Tailscale Funnel은 공유기의 포트를 열지 않고도 머신의 서비스를 인터넷에 게시합니다: 방문자는 Tailscale의 릴레이를
거쳐 들어옵니다. 네트워크 측면에서는 간단하고 안전하지만, 약점이 하나 남아 있습니다.

- **암호화 비용.** 기본 Funnel 모드에서는 머신의 `tailscaled` 서비스가 방문자마다 TLS 핸드셰이크를 수행합니다.
  작은 머신에서 측정하면 이것이 **연결 비용의 약 80 %** 입니다. 초당 수백 개의 새 연결만으로도 프로세서가
  포화됩니다: 평범한 컴퓨터 한 대가 간단한 스크립트 하나로 사이트와 머신을 쓰러뜨릴 수 있습니다.
- **보이지 않는 방문자.** 일반적인 방화벽(nftables, ufw, fail2ban)은 이 방문자들을 보지 못합니다: 이들은 암호화된
  상태로, Tailscale 터널을 통해, 릴레이의 주소를 달고 도착합니다.
- **흩어진 설정.** Tailscale의 설정(운영자, 출구 노드, 경로, SSH, 방패…)은 많고, 명령과 웹 콘솔에 나뉘어 있으며,
  일부는 진행 중인 세션을 끊을 수 있습니다.

### 목표

- 설정마다 한 문장의 설명을 붙여, 인터페이스에서 Tailscale을 완전히 제어합니다.
- 각 방문자의 실제 주소를 보고, 남용하는 연결을 모든 암호화 **이전에** 거부합니다.
- 공격 중에도 머신이 버티게 합니다: 관리 접속과 다른 서비스는 계속 접근할 수 있습니다.
- 아무것도 강요하지 않습니다: 제안하고, 명령을 보여 주고, 묻고, 되돌릴 수 있습니다.
- systemd, OpenRC, runit 아래에서 모든 Linux 배포판에서 동작합니다.

### omega-tail이 하는 일

- Tailscale, 머신, 게시된 항목의 상태를 보여 주며, 경고에서 바로 문제를 고치는 화면으로 이동할 수 있습니다.
- `tailscaled`를 시작, 중지, 다시 시작하며, 세션이 Tailscale을 거치는 경우를 위한 안전장치가 있습니다.
- 연결, 계정, `tailscale set`의 모든 설정을 관리하며, 적용하기 전에 검사합니다.
- Serve와 Funnel 서비스를 게시, 제거, 일시 중지, 테스트하며, 백업과 복원을 제공합니다.
- tailnet의 장치, 그 경로(직접 또는 릴레이 경유), 네트워크 진단, 로그를 보여 줍니다.
- Funnel과 사이트 사이에 HAProxy **게이트**를 둡니다: 주소별·접두사별 규칙, 전체 예산, 신뢰 목록과 블랙리스트,
  JA4 지문·출발 네트워크(AS)·국가별 그룹화, 자동 공격 모드.
- `tailscaled`의 자원을 제한하고, Funnel을 잠시 또는 완전히 끊으며, 자동 감시 덕분에 이를 스스로 할 수도 있습니다.
- nftables 테이블(방패)로 `tailscaled`의 WireGuard 포트를 보호합니다.
- 머신과 최근 7일간의 공격에 대한 보고서를 TXT, HTML, JSON으로 만듭니다.

### 이 프로젝트가 하지 않는 일

- Tailscale을 대체하지 않습니다: 제어할 뿐입니다.
- 인터넷 회선 자체(공유기, 링크)를 포화시키는 대용량 공격은 막지 못합니다.
- Tailscale의 웹 관리 콘솔(접근 정책, 출구 노드 승인, tailnet의 Funnel 활성화)은 관리하지 않습니다.
- Funnel이 아닌 다른 방식으로 게시한 서비스는 보호하지 않습니다: 그런 포트에는 omega-fire가 있습니다.
- 결코 root로 실행되지 않으며, 여러분의 동의 없이 백그라운드에서 아무것도 실행하지 않습니다.
- Windows와 macOS에서는 동작하지 않습니다.

[↑ 목차](#목차)

---

## Tailscale과 Funnel 이해하기

omega-tail은 Tailscale에 관한 몇 가지 개념을 전제로 합니다. 이 절은 그 개념들을 모아 두었으며, 그 밖의 지식은
전제하지 않습니다.

### 용어

| 용어 | 설명 |
|---|---|
| **Tailnet** | 여러분의 Tailscale 사설 네트워크: 같은 계정(또는 같은 조직)에 연결된 모든 머신. 각 머신은 그 안에서 `100.x.y.z` 주소(범위 100.64.0.0/10)와 `fd7a:115c:a1e0::/48` 안의 IPv6 주소를 받습니다. |
| **`tailscaled`** | 머신에서 실행되는 서비스(데몬): WireGuard 암호화 터널, Tailscale의 네트워크 스택, 그리고 Serve와 Funnel의 경우 여러분의 서비스로 가는 릴레이를 맡습니다. |
| **`tailscale`** | `tailscaled`를 제어하는 명령(`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail이 여러분 대신 이 명령을 사용합니다. |
| **WireGuard** | 머신 사이에 쓰이는 암호화 터널 프로토콜. 이를 위해 `tailscaled`는 UDP 포트(기본값 41641)에서 대기하며, 이 포트는 흔히 공유기가 열어 줍니다(UPnP). |
| **DERP 릴레이** | 두 머신이 서로 직접 닿을 수 없을 때(까다로운 NAT) 트래픽을 중계하는 Tailscale 서버. 「직접」 경로가 더 빠릅니다. |
| **MagicDNS** | tailnet 머신의 이름으로, `machine.nom-du-tailnet.ts.net` 형식입니다. |
| **Serve** | 로컬 서비스(사이트, API…)를 **tailnet에만** 유효한 `*.ts.net` 인증서와 함께 HTTPS로 게시합니다. |
| **Funnel** | 로컬 서비스를 **인터넷 전체에** `https://machine.nom-du-tailnet.ts.net` 주소로 게시합니다. 443, 8443, 10000 포트만 열 수 있습니다. |
| **Funnel 릴레이** | 인터넷의 방문자를 받아 여러분의 tailnet으로 들여보내는 Tailscale 서버(「funnel-ingress-node」로 표시됨). |
| **운영자 (operator)** | sudo 없이 Tailscale을 설정할 수 있도록 허가된 Linux 계정(`tailscale set --operator=…`). omega-tail은 sudo를 통해 한 번 이를 제안합니다. |
| **출구 노드 (exit node)** | 다른 머신이 모든 인터넷 트래픽을 통과시키는 tailnet의 머신(VPN처럼). Tailscale 콘솔에서 승인되어야 합니다. |
| **광고된 서브넷 (subnet router)** | 한 머신이 tailnet의 나머지에서 접근할 수 있게 해 주는 로컬 네트워크(예: `192.168.1.0/24`). |
| **방패 (shields up)** | tailnet에서 들어오는 모든 연결을 거부하는 Tailscale 설정. |
| **Tailscale SSH** | Tailscale이 제공하고 tailnet 정책으로 허가되는 SSH 서버. |
| **PROXY v2 헤더** | 방문자의 실제 주소를 받는 쪽에 전달하기 위해 연결의 맨 앞에 붙이는 짧은 헤더. |
| **JA4 지문** | 소프트웨어가 TLS 연결을 여는 방식의 서명: 브라우저와 공격 도구는 서로 다른 서명을 가집니다. |
| **AS (자율 시스템)** | 주소의 출발 네트워크: 인터넷 서비스 제공자, 호스팅 업체, 클라우드. |

### 방문자의 경로

**omega-tail 없이 기본 Funnel.** `tailscaled`가 모든 것을 합니다: WireGuard 터널을 복호화하고, 방문자와 TLS
핸드셰이크를 한 뒤, 요청을 HTTP로 사이트에 중계합니다. 머신의 어떤 방화벽도 방문자를 보지 못하며, 새 연결마다
`tailscaled`에 큰 비용이 듭니다.

```text
방문자 ──HTTPS──▶ Funnel 릴레이 ──WireGuard──▶ tailscaled (TLS + HTTP 릴레이) ──HTTP──▶ 여러분의 사이트
                  (Tailscale)                  └── 모든 비용이 여기서 발생
```

**omega-tail 게이트를 둔 Funnel.** Funnel이 TCP 모드로 바뀝니다: `tailscaled`는 더 이상 TLS를 처리하지 않고, 아직
암호화된 흐름을 방문자의 실제 주소(PROXY v2 헤더)를 앞에 붙여 게이트로 넘깁니다. 게이트는 모든 암호화 **이전에**
결정합니다: 거부된 연결에는 비용이 거의 들지 않으며, 허용된 연결만 `tailscaled`의 TLS보다 빠른 OpenSSL로
복호화됩니다.

```text
방문자 ──HTTPS──▶ Funnel 릴레이 ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                    │
                                                    ▼
                                     omega-tail 게이트 (HAProxy, 127.0.0.1)
                                     ├── TLS 전에 거부: 블랙리스트, 속도, 예산, 대상 이름, 그룹화
                                     └── 허용: TLS (*.ts.net 인증서) ──HTTP──▶ 여러분의 사이트
```

게이트는 머신의 루프백에서만 대기하며 여러분의 계정으로 실행됩니다. tailnet의 머신은 어떤 규칙보다도 먼저 항상
허용됩니다: Funnel 방문자만 걸러집니다.

### Tailscale에서 허용해야 하는 것 (관리 콘솔)

이 설정은 Tailscale 웹 콘솔에서 한 번만 합니다. omega-tail은 이를 바꾸지 않습니다.

- tailnet에서 **MagicDNS**와 **HTTPS 인증서** 활성화(Serve, Funnel, 게이트 인증서에 필요).
- tailnet 접근 정책에서 해당 머신에 **Funnel 허용**(`funnel` 속성).
- 출구 노드나 광고된 서브넷의 경우: 콘솔에서의 **승인**.

[↑ 목차](#목차)

---

## 기능

메인 메뉴는 여섯 개씩 두 열로 되어 있습니다: 제어하는 **TAILSCALE**, 방어하는 **보호**.

### TAILSCALE

#### 1. 대시보드

- **Tailscale**: 서비스, 연결 상태, 실행 중인 버전과 설치된 버전, 머신 이름, 주소, 계정, 온라인 장치, 키 만료,
  운영자, 제공 중인 출구 노드와 사용 중인 출구 노드, 광고된 서브넷.
- **머신**: 머신 전체 CPU, 코어별 부하, 온도, 메모리, `tailscaled`의 CPU와 메모리, 자원 제한, 그리고 보호 기능의
  상태(Funnel, 방화벽과 공격 모드, 블랙리스트, 감시, 방패).
- **게시**: 게시된 각 포트, 인터넷용(Funnel)인지 tailnet용(Serve)인지, 그 모드와 대상.
- **경고**: 가장 심각한 것부터 가벼운 것까지, 해당 화면을 여는 「수정」과 함께. 예: 서비스 중지, 업데이트가
  설치되었지만 적용되지 않음, 키 만료 임박, 보호 없이 게시된 Funnel, 높은 온도, 자원을 너무 많이 쓰거나 제한되지
  않은 `tailscaled`, 계속 커지는 블랙리스트.
- 임곗값(CPU, 부하, 온도, 메모리, `tailscaled`)에 따라 녹색, 주황색, 빨간색으로 표시되는 값.

#### 2. tailscaled 서비스

- init 시스템이 보는 상태, 실행 중인 버전과 설치된 버전, 실행 명령, 추가 설정 파일(drop-in), 자원 제한.
- **시작**, **중지**, **다시 시작**(예: 이미 설치된 업데이트를 적용할 때).
- **안전장치**: 세션이 Tailscale을 거치는 경우(tailnet을 통한 SSH), 중지는 두 번째 확인을 요구합니다. 다시 시작할
  수 없게 되기 때문입니다.
- **시작 설정 수정**: 부팅 시 `tailscale up`을 실행하여 설정을 처음 바꿀 때 머신이 tailnet에서 빠질 위험이 있는
  추가 설정 파일을 찾아냅니다. 수정 내용을 보여 주며 원본은 보관합니다.

#### 3. 연결 및 설정

- **연결**, **연결 해제**, **계정 추가**, **계정 전환**, **영구 로그아웃**(머신 이름 입력 필요).
- **`tailscale set`의 모든 설정**, 각각 설명 한 문장과 함께: 머신 이름과 별칭, 경로, tailnet DNS, 방패, 상태 기반
  필터링, netfilter 모드, 출구 노드, 로컬 네트워크 접근, 이 머신을 출구 노드로 제공, 광고된 서브넷, Tailscale SSH,
  웹 인터페이스, 업데이트, 피어 릴레이, 운영자.
- 입력하는 동안 틀 안에 **이전 → 이후**와 명령을 보여 주며, 적용한 뒤에는 다시 읽은 각 값을 ✔(반영됨) 또는
  ✖(반영 안 됨)으로 표시합니다.
- 변경이 Tailscale을 거치는 세션을 끊을 수 있으면 경고합니다.
- **IP 포워딩**: 머신이 출구 노드 역할을 하거나 서브넷을 광고할 때 버튼 하나로 활성화.

#### 4. 게시

- 머신이 게시하는 모든 것: 포트, 공개(Funnel) 또는 tailnet(Serve), 모드, 경로, 대상, 보호.
- 로컬 서비스를 HTTPS, HTTP, TCP, 종료된 TLS로 **게시**; **제거**; **Funnel 일시 중지**와 **Funnel 복원**(원래와
  똑같이).
- **종단 간 테스트**: 방문자처럼 실제로 연결합니다(응답, 시간, 인증서, TLS 버전).
- **백업**: 각 변경 전의 상태(최근 50개), 복원 가능.
- 모든 변경은 검사되며, 차이가 있으면 게시를 다시 구성하고, 그렇지 않으면 이전 상태로 되돌립니다.

#### 5. 네트워크와 장치

- tailnet의 **장치**: 시스템, 온라인 여부, 경로(직접 또는 릴레이 경유), 마지막 확인 시각, 주소, 주고받은 트래픽.
  Tailscale의 Funnel 릴레이는 기본적으로 숨겨집니다.
- **Tailscale 핑**(경로와 지연 시간), **누구인가요?**(tailnet 주소의 소유자).
- **네트워크 진단**: UDP, IPv4 / IPv6, NAT 유형, 공유기의 포트 열기(UPnP, NAT-PMP, PCP), 가장 가까운 릴레이와 지연
  시간.
- Tailscale의 **DNS**, **tailnet 잠금**, **내부 카운터**.
- 읽기 전용: 이 화면의 어떤 것도 설정을 바꾸지 않습니다.

#### 6. 로그

- `tailscaled`의 로그(journalctl, 또는 systemd가 아닌 경우 서비스 파일)와 게이트의 로그: 필터링 및 내보내기 가능.
- 각 정보에는 테마에서 가져온 고유한 색이 있습니다: 날짜, 프로세스, 메시지 범주(제어, 네트워크, DNS, WireGuard 엔진), 굵은 주소, 빨간색 오류, 주황색 경고. 게이트의 경우 거부 사유,
  그룹화, AS, 국가.

### 보호

#### 7. Funnel 방화벽

- 배포판의 패키지 관리자(pacman, apt, dnf, zypper, apk, xbps, emerge)로 **HAProxy 설치**.
- **보호 활성화**: `*.ts.net` 인증서, 목록, 검사된 설정, 게이트 서비스, Funnel 전환 후 인터넷에서 테스트. 실패하면
  원래 게시를 즉시 되돌립니다.
- **보호 비활성화**: Funnel을 이전과 정확히 같게 되돌리고 검사합니다.
- 재시작 없이 적용되는 **규칙**, 위험 없이 임곗값을 조정하는 **관찰** 모드, **그룹화**([보호 기능 상세](#보호-기능-상세)
  참조).
- 별도 프로세스에서 AS / 국가 **데이터베이스 업데이트**(DB-IP Lite).

#### 8. 생존

- **`tailscaled` 자원 제한**: CPU 상한, 가중치와 우선순위, SSH 접근 우선 옵션.
- **Funnel 서킷 브레이커**: CPU와 온도 임곗값, 10분 차단(자동 재개) 또는 완전 차단.
- **자동 감시**: 화면 앞에 아무도 없을 때 같은 일을 합니다.
- **WireGuard 포트 방패**: 해당 화면으로 가는 버튼(관찰, 활성, 설치, 재설치, 제거, 위임).

#### 9. 공격과 결정

- 게이트의 카운터(수신, 암호화 전 거부, 허용, 진행 중)와 가장 활발한 주소를 2초마다 다시 읽어, 각 주소의 국가,
  AS, 상태와 함께 보여 줍니다.
- **차단**, **블랙리스트**, **차단 해제**, **신뢰**: 게이트를 다시 시작하지 않고 즉시 적용되며, 알림이 작업과
  주소의 위치를 한 줄로 알려 줍니다.
- **지문**, **AS**, **국가** 보기; 공격 모드 상태와 그룹화로 거부된 연결.
- **블랙리스트 관리**: 추가 날짜와 출처가 있는 전체 목록, 추가, 삭제, TXT 파일 가져오기(중복, 이미 포함된
  네트워크, tailnet 주소는 제외), 미리 보기가 있는 정리(기간별, 가장 오래된 N개, 줄 범위, 출처 하나, 전체),
  TXT(다시 가져오기 가능), HTML, JSON 내보내기. 최대 50,000개 항목.

#### 10. 보고서

- omega-tail이 머신에 대해 아는 모든 것을 사실로: Tailscale, 게시, 머신, 방화벽, 생존, 경고, 그리고 게이트 로그에서
  읽은 **최근 7일간의 공격**.
- **개인정보 보호**: 기본적으로 Tailscale 계정과 tailnet 장치의 이름·주소를 빼므로, 다른 사람에게 보낼 수 있습니다.
- **TXT**, **HTML**(테마 선택), **JSON** 내보내기; **내보내기 보기**는 브라우저에서 폴더를 엽니다.

#### 11. 설정

- 인터페이스와 내보내기의 언어, 인터페이스와 내보내기의 테마, 내보내기 폴더와 스크린샷 폴더, 그리고 그 정리.

#### 12. 도움말

- 화면마다 한 절, 단축키, 명령줄, 그리고 **문의 및 지원**.

[↑ 목차](#목차)

---

## 보호 기능 상세

각 보호 기능은 특정 위협에 대응하며, 어느 것도 강요되지 않습니다.

| 보호 기능 | 무엇에 대응하는가 | 위치 |
|---|---|---|
| 게이트(규칙) | 하나 또는 몇 개의 주소에서 오는 폭주, 사이트를 대상으로 하지 않는 연결 | Funnel 방화벽 |
| 그룹화 | 주소가 흩어진 공격(수천 개의 주소, 각각 연결 하나) | Funnel 방화벽 |
| 블랙리스트 | 공격하는 것으로 알려진 주소와 네트워크, 오래 보관 | 공격과 결정 |
| 자원 제한 | 공격 중에 머신 전체를 차지할 수 있는 `tailscaled` | 생존 |
| 서킷 브레이커 | 그래도 포화된 머신: Funnel을 잠시 끊기 | 생존 |
| 자동 감시 | 같은 일을, 화면 앞에 아무도 없을 때 | 생존 |
| WireGuard 방패 | `tailscaled` 포트로 쏟아지는 UDP 패킷, Funnel이 열려 있든 아니든 | 생존 |

### 게이트 (Funnel 방화벽)

규칙은 이 순서로, 모두 암호화 전에 적용됩니다:

1. **tailnet 머신**(100.64.0.0/10, fd7a:115c:a1e0::/48): 항상 허용.
2. **신뢰 목록**: 결코 제한되지 않음. **블랙리스트**: 목록에서 뺄 때까지 거부.
3. **주소별 속도**(기본값 10초에 연결 40개): 넘으면 그 주소는 선택한 기간(기본값 60분) 동안 차단됩니다.
4. **접두사별 속도**: IPv4는 /24, IPv6는 /64.
5. 초당 허용 연결의 **전체 예산**: 프로세서가 결코 넘치지 않습니다.
6. **대상 이름**: 머신 이름을 대상으로 하지 않는 연결은 거부됩니다.

게이트의 `*.ts.net` 인증서는 Tailscale에 요청하며, 매일 확인하고, 만료 30일 전에 재시작 없이 갱신합니다.
**관찰** 모드는 아무것도 거부하지 않고 모든 것을 셉니다.

### 그룹화 (지문, AS, 국가)

주소가 흩어진 공격에서는 주소별 규칙이 각 주소를 한 번만 봅니다. 그래서 게이트는 각 클라이언트를 **JA4 지문**,
**AS**, **국가**로도 분류하고 그룹마다 속도를 셉니다.

- **자동 공격 모드**: 초당 들어오는 연결이 80개(조정 가능)를 넘으면 게이트가 스스로 공격 모드로 바뀌고, 5분간
  잠잠하면 빠져나옵니다.
- 공격 모드에서만: 폭증하는 알 수 없는 지문, 호스팅 업체나 클라우드의 AS(목록 수정 가능), 또는 여러분의 목록에 있는
  국가(기본값은 비어 있음)가 속도를 넘으면 거부됩니다.
- **일반 브라우저**(Chrome, Edge, Firefox)는 이 규칙의 영향을 결코 받지 않으며, **알려진 클라이언트**(최근 24시간
  안에 허용됨)는 전체 예산보다 먼저 통과합니다.
- **학습**: 7일 동안 게이트는 사이트에서 평소 보이는 지문을 학습합니다(공격 중에는 결코 학습하지 않음). 그때까지
  그룹화는 관찰 모드로 남습니다.
- 공격이 없을 때는 연결 열 개 중 하나를 분류하고, 공격 중에는 모두 분류합니다.
- AS / 국가 데이터베이스는 **DB-IP Lite**이며, 한 달에 한 번 내려받아 업데이트합니다.

### 생존

- **자원 제한**: 별도의 추가 설정 파일이 `tailscaled`에 상한을 두고(예: 스레드 4개 머신에서 코어 하나 전체)
  우선순위를 낮춥니다. 여러분의 설정은 결코 수정되지 않습니다.
- **서킷 브레이커**: `tailscaled`가 CPU 임곗값(기본값 60초 동안 코어 하나의 80 %)을 계속 넘거나 온도가 85 °C에
  이르면, omega-tail은 Funnel을 10분간 끊기(자동 재개, 원래와 똑같이, omega-tail을 닫아도 동작), 완전히 끊기, 또는
  기다리기를 제안합니다. tailnet은 결코 끊기지 않습니다.
- **자동 감시**(기본값 비활성): 여러분의 계정으로 실행되는 서비스가 임곗값 초과가 세 번 일어나면 Funnel을 스스로
  끊습니다. 처음에는 15분, 두 번째는 30분, 그다음은 한 시간이며, 스스로 다시 켭니다.

### WireGuard 포트 방패

`tailscaled`는 UDP 포트로 들어오는 초당 100,000개의 패킷마다, 유효하지 않은 패킷이라도, 프로세서 코어 하나 정도를
씁니다. 방패는 네트워크 카드 위에서 그 앞에 놓이는 nftables 테이블입니다:

- **알려진 피어**(`tailscaled`가 데이터를 보내는 상대)는 결코 제한되지 않습니다.
- 핸드셰이크는 출발지마다 초당 20개로 제한됩니다.
- 그 밖의 출발지에는 예산이 있습니다(각각 초당 패킷 500개, 전체 5,000개).
- WireGuard가 아닌 패킷은 거부됩니다.

방패는 먼저 **관찰**로 설치한 뒤 **활성**으로 바꿉니다. omega-connect로 연결되어 있으면 **omega-fire**(3.7.0 이상)가
omega-tail 대신 이를 설치하고 관리할 수 있습니다: 같은 테이블이며, 건드리지 않은 채 관리 주체만 바뀝니다.

[↑ 목차](#목차)

---

## 측정

omega-tail의 선택은 보호 대상과 같은 세대의 머신(2010~2016년 프로세서, 대부분 AES 가속 없음)에서 한 측정에서
나왔습니다.

| 측정 항목 | 결과 |
|---|---|
| 기본 Funnel 연결 비용 가운데 TLS의 비중 | 약 80 % |
| 게이트가 **거부한** 연결의 비용, 기본 Funnel과 비교 | **4.6배 적음** |
| 게이트가 **허용한** 연결의 비용, 기본 Funnel과 비교 | **2배 적음** |
| 게이트를 둔 처리량, 연결 유지(`tailscaled`처럼 Go로 구현된 TLS와 비교) | 요청 **+15 %**, CPU −20 % |
| WireGuard 방패: `tailscaled`의 코어 하나를 다 쓰던 패킷 폭주 | 코어 하나의 **1 %** |
| 서비스(게이트, 감시, 방패)의 메모리 | 약 67 MB |

따라서 게이트는 사이트의 처리량을 떨어뜨리지 않습니다: 이런 머신에서는 omega-tail이 있든 없든 암호화 자체가
한계이며, 운영 환경에서 Funnel은 어차피 Tailscale의 릴레이와 공유기를 거칩니다.

[↑ 목차](#목차)

---

## 아키텍처

```text
src/omega_tail/
├── app/              구성 루트: 계층을 조립, 진입점(인터페이스, 명령줄)
├── core/             공유 상수
├── domain/           순수 비즈니스 로직: 게이트 규칙, 경고, 서킷 브레이커, 감시, 블랙리스트…
├── application/      유스 케이스: 게시, 방화벽, 생존, 보고서, 설정
├── ports/            애플리케이션이 기대하는 계약(Protocol)
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, 로그, 내보내기, Lua 스크립트
├── interfaces/       tui/ (Textual), cli/ (명령줄), shared/ (도움말, 보고서, 표시)
└── shared/           언어(gettext)
```

### 설계 원칙

- `domain/`에는 읽기도 쓰기도 없습니다: 모든 것을 머신 없이 테스트할 수 있습니다.
- `application/`은 도메인과 포트를 통해 유스 케이스를 조율합니다. 인터페이스와 명령줄은 같은 유스 케이스를
  호출합니다.
- 명령을 실행하는 것은 `infrastructure.commands`와 `infrastructure.privileged`뿐이며, 인터페이스는 결코 직접
  실행하지 않습니다. 이 규칙은 자동으로 검사됩니다(import-linter).
- 인터페이스는 OMEGA 도구 모음 전체가 공유하는 라이브러리 [omega-lib](https://github.com/kraynux)(테마, 터미널
  감지, 언어, 문의 및 지원, WireGuard 방패)에 기반합니다. PyPI에는 공개되지 않으며, 아카이브에 포함되어
  있습니다(`vendor/omega-lib/`).
- 느린 호출(Tailscale, HAProxy, 디스크, 네트워크)은 모두 백그라운드 작업으로 실행됩니다: 인터페이스는 결코 멈추지
  않습니다.

[↑ 목차](#목차)

---

## 사전 요구 사항

### 시스템

- Linux, 모든 배포판(Arch Linux와 그 파생 배포판에서 테스트).
- Python 3.10 이상, `venv` 모듈 포함.
- init 시스템: **systemd**, **OpenRC**, **runit** 중 하나.
- 머신을 바꾸는 작업을 위한 `sudo`(작업마다 요청하며, 실행할 때는 결코 요청하지 않음).
- 최소 80×24의 터미널([테마와 터미널](#테마와-터미널) 참조).

### Tailscale

- 설치되어 연결된 **Tailscale**(`tailscale` 클라이언트와 `tailscaled` 서비스). 버전 1.104로 테스트했습니다.
- Funnel의 경우: Tailscale 콘솔에서 MagicDNS, HTTPS 인증서, Funnel 허용
  ([Tailscale에서 허용해야 하는 것](#tailscale에서-허용해야-하는-것-관리-콘솔) 참조).

### Python 의존성

`install.sh`가 가상 환경 안에 설치합니다:

- `textual`: 인터페이스.
- `omega-lib`: OMEGA 도구 모음의 공유 라이브러리, 아카이브에 포함.

### 필수 및 선택 구성 요소

omega-tail은 있는 것을 감지하고, 쓸 수 있는 것만 활성화합니다.

| 구성 요소 | 역할 | 상태 |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | omega-tail이 제어하는 모든 것 | **필수** |
| Python 3.10+, `textual`, `omega-lib` | 애플리케이션 | **필수** |
| systemd, OpenRC 또는 runit | 게이트, 감시, 방패 서비스 | **필수**(셋 중 하나) |
| HAProxy 3.x | Funnel 방화벽의 게이트 | 선택(omega-tail에서 설치 가능) |
| Lua를 포함한 HAProxy | 그룹화(지문, AS, 국가) | 선택(일반적인 배포판의 경우) |
| nftables(`nft_limit`이 있는 커널) | WireGuard 포트 방패 | 선택 |
| 시스템 로그 읽기(`systemd-journal`, `adm` 또는 `wheel` 그룹) | 로그, 공격 보고서 | 권장 |
| 브라우저와 데스크톱 | 브라우저에서 「내보내기 보기」(없으면 omega-tail 안에서 읽기) | 선택 |
| omega-connect | 도구 모음의 레지스트리, 동기화, 업데이트 | 선택 |
| omega-fire 3.7.0+ | omega-fire에서 WireGuard 방패 관리 | 선택 |

[↑ 목차](#목차)

---

## 설치

공식 아카이브는 `.tar.gz` 형식으로 제공됩니다. 설치 전에, 옆에 게시된 `sha.txt` 파일로 무결성을 확인하십시오:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **이 세 가지 방법은 첫 설치용입니다.** `~/omega-tail`이 이미 있다면 [업데이트](#업데이트) 절을 사용하십시오.
> 기존 `omega-tail` 폴더 안에서 이 명령을 다시 실행하지 마십시오: `tar`가 중첩된 `omega-tail/omega-tail/`을
> 만들게 됩니다.

설치의 어떤 단계도 root 권한을 요구하지 않습니다: omega-tail은 일반 사용자로 실행됩니다.

### 방법 1 — 설치 스크립트

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ 이미 omega-tail 폴더 안에 있는 것 같습니다 — README의 업데이트 절을 참조하십시오." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ 이미 여기에 압축이 풀려 있어 이 단계를 건너뜁니다." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail이 이미 있어 이동을 건너뜁니다." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

스크립트는 가상 환경을 만들고, 의존성을 설치하며(포함된 omega-lib 먼저), 실행기에 실행 권한을 주고, omega-connect가
읽는 설치 토큰을 쓰고, `omega-tail` 별칭을 제안합니다. 다시 실행해도 안전합니다.

### 방법 2 — 견고한 전체 설치

이 명령은 다시 실행할 수 있습니다: 이미 끝난 단계는 건너뜁니다.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ 이미 omega-tail 폴더 안에 있는 것 같습니다 — README의 업데이트 절을 참조하십시오." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail이 이미 있어 압축 해제를 건너뜁니다." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv가 이미 있어 이 단계를 건너뜁니다." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail을 설치했습니다. ./omega-tail.sh를 실행하십시오."
```

### 방법 3 — 상세 설치

```bash
# 0. 기존 omega-tail 안에서 다시 실행하는 것이 아닌지 확인
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ 이미 omega-tail 폴더 안에 있는 것 같습니다 — README의 업데이트 절을 참조하십시오." >&2; exit 1; }

# 1. 압축 해제
[ -d omega-tail ] && echo "ℹ️ 이미 여기에 압축이 풀려 있어 이 단계를 건너뜁니다." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. 홈으로 이동
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail이 이미 있어 이동을 건너뜁니다." || mv omega-tail ~/

# 3. 프로젝트로 들어가기
cd ~/omega-tail/

# 4. 가상 환경 만들기
[ -f .venv/bin/activate ] && echo "ℹ️ .venv가 이미 있어 생성을 건너뜁니다." || python3 -m venv .venv

# 5. 의존성 설치(포함된 omega-lib 먼저)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. 실행기에 실행 권한 부여
chmod +x omega-tail.sh install.sh

# 7. 설치 토큰 쓰기(omega-connect가 읽음, 선택 사항)
./omega-tail.sh synchro jeton

# 8. 실행
./omega-tail.sh
```

Debian, Ubuntu와 그 파생 배포판에서는 `venv` 모듈이 Python과 함께 설치되지 않는 경우가 있습니다:
`sudo apt install python3-venv`.

### 업데이트

omega-tail의 서비스(게이트, 감시)는 `~/omega-tail/var/`의 파일을 사용합니다. 따라서 업데이트는 **이 폴더를 그대로
두어야** 합니다: 아카이브에는 `var/`가 없으며, 기존 설치 위에 덮어써서 압축을 풉니다.

**`~/omega-tail`이 아닌**, 아카이브가 있는 폴더에서:

```bash
# 1. 현재 설치 백업(var/ 포함)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. 새 버전을 그 위에 압축 해제(var/는 유지됨)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. 다시 설치(의존성, 실행기, 설치 토큰)
cd ~/omega-tail
./install.sh

# 4. omega-tail 다시 실행
./omega-tail.sh
```

게이트가 활성 상태라면 **Funnel 방화벽 → 「규칙 적용」** 작업이 새 버전으로 재시작 없이 설정을 다시 만듭니다. 자동 감시가
켜져 있다면 **생존 → 「감시 활성화」** 작업이 새 코드로 감시를 다시 시작합니다. omega-connect도 업데이트를 할 수
있습니다(Updater 화면).

### Bash 또는 Zsh 별칭

`install.sh`가 별칭을 제안합니다. 직접 추가하려면:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

별칭 이름은 시스템 명령 `tail`을 가리지 않도록 `tail`이 아니라 `omega-tail`입니다.

[↑ 목차](#목차)

---

## 사용법

### 실행

```bash
cd ~/omega-tail
./omega-tail.sh

# 또는 별칭을 만들었다면 간단히:
omega-tail
```

실행기는 권한 상승을 요구하지 않습니다: omega-tail은 여러분의 계정으로 실행되며, sudo는 그것이 필요한 작업에서만,
터미널에서, 명령을 먼저 보여 준 뒤 요청합니다.

### 권장 첫 단계

Funnel로 게시한 사이트를 보호하려면, 이 순서로:

1. **대시보드**: 경고를 읽고, **운영자 되기**(sudo로 한 번)를 하여 sudo 없이 Tailscale을 설정합니다.
2. **생존 → 자원 제한 적용**: `tailscaled`가 더 이상 머신 전체를 차지하지 못합니다.
3. **게시**: 사이트를 **443 포트에서 HTTPS**로, 경로 `/`로 게시한 뒤 **종단 간 테스트**를 합니다.
4. **Funnel 방화벽 → HAProxy 설치**, 이어서 **보호 활성화**, 처음에는 **관찰** 모드로.
5. 며칠 뒤 **공격과 결정**: 카운터에 남용만 보이면 게이트를 **일반** 모드로 바꿉니다.
6. **그룹화**가 관찰 모드에서 7일 동안 학습하게 둔 뒤 **적용**으로 바꿉니다.
7. **생존 → WireGuard 포트 방패**: 관찰로 설치한 뒤 활성으로 바꿉니다.
8. 화면 앞에 아무도 없는 머신이라면: **생존 → 감시 활성화**.

### 인터페이스 언어

17개 언어: 프랑스어, 영어, 스페인어, 포르투갈어(브라질), 이탈리아어, 독일어, 네덜란드어, 폴란드어, 러시아어,
중국어, 베트남어, 태국어, 인도네시아어, 일본어, 한국어, 힌디어, 아랍어.

- 설정에서 선택하며(`s` 키, 번역되지 않는 레이블 「Langue / Language」), 인터페이스만 다시 시작하여 적용합니다.
- 한 번만 쓰려면: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- Linux 텍스트 콘솔(TTY)에서는 콘솔 글꼴에 문자가 없는 언어가 해당 세션 동안 영어로 표시되며, 아랍어는 오른쪽에서
  왼쪽으로 표시됩니다.
- **내보내기 언어**(보고서, 블랙리스트, 로그)는 따로 설정하며, 기본값은 「인터페이스와 같음」입니다.

### 문의 및 지원

도움말(`a` 키)에는 **문의 및 지원** 화면이 있습니다:

- *커피 한 잔 사기*(개발자의 PayPal 페이지);
- *지원팀에 문의*(이메일 주소와 사이트의 양식을 그대로 표시);
- *사용자로 등록(익명)*;
- *업데이트 확인*.

등록은 자발적이며 기본적으로 꺼져 있고 한 번만 전송됩니다. 사용자 수와, 원하면 사용자의 대륙 또는 국가(닫힌 목록,
자유 입력 없음)를 세는 데에만 쓰입니다. 무작위로 생성한 키, 소프트웨어 이름(`omega-tail`)과 버전만 보내며, 이름,
머신 이름, 설정, tailnet 주소는 절대 보내지 않습니다. 같은 화면에서 언제든지 철회할 수 있습니다(*등록 취소*).
업데이트 확인은 사이트에 게시된 버전 목록만 읽으며, 클릭하지 않으면 절대 실행되지 않습니다.

### 다른 omega 도구와의 연동

- **omega-connect**: `install.sh`는 아무것도 실행하지 않고 도구와 그 버전을 설명하는 설치 토큰
  (`var/omega-jeton.json`)을 씁니다. omega-connect는 이를 레지스트리, 동기화, 복구, 업데이트, 설치에 사용합니다.
  `./omega-tail.sh synchro jeton`으로 직접 다시 쓸 수 있습니다.
- omega-connect로 연결된 **omega-fire**(3.7.0 이상)는 WireGuard 포트 방패를 설치하고 관리할 수 있으며, 그 규칙
  목록에 출처를 omega-tail로 표시합니다.

### 명령줄

모든 명령은 `./omega-tail.sh …`(별칭이 있으면 `omega-tail …`) 형식으로 씁니다:

| 명령 | 역할 |
|---|---|
| `omega-tail` | 인터페이스 |
| `omega-tail etat [--format json]` | Tailscale과 머신의 상태 및 경고, 텍스트 또는 스크립트용 |
| `omega-tail aide` | 텍스트로 된 전체 도움말 |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | 보고서, 표시 또는 저장 |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Funnel 끊기 또는 다시 켜기 |
| `omega-tail veille etat` | 자동 감시의 상태와 마지막 줄들 |
| `omega-tail porte etat` | 게이트 상태와 카운터 |
| `omega-tail porte certificat [--si-besoin]` | 게이트의 `*.ts.net` 인증서 갱신 |
| `omega-tail porte groupes` | 그룹화: 공격 모드, 지문, AS, 국가 |
| `omega-tail porte base` | AS / 국가 데이터베이스 업데이트 |
| `omega-tail porte bloquer ADRESSE [--toujours]` | 주소나 네트워크 차단(`--toujours`이면 블랙리스트) |
| `omega-tail porte debloquer ADRESSE` | 차단 해제 |
| `omega-tail porte confiance ADRESSE` | 신뢰로 지정 |
| `omega-tail synchro jeton` | 설치 토큰 쓰기(omega-connect) |
| `omega-tail --version` | 버전 |

### 전체 흐름

1. 시작 화면, 이어서 두 열(TAILSCALE과 보호)로 된 메인 메뉴.
2. 각 화면 제목 아래의 **상태 표시줄**이 모든 것을 요약합니다: 서비스, 머신과 `tailscaled`의 CPU, 온도, 메모리,
   Funnel, 방화벽, 감시, 연결. 5초마다 다시 읽습니다.
3. 머신을 바꾸는 모든 작업은 명령을 보여 준 뒤 확인을 요청합니다. sudo는 터미널에서 입력하며, 그다음 인터페이스로
   돌아옵니다.
4. 민감한 작업(영구 로그아웃, 블랙리스트 전체 정리)은 단어 하나를 입력하도록 요구합니다.
5. 결과는 다시 읽은 상태로 검증되어 한 줄로 표시됩니다.

### 탐색

- 위 / 아래 화살표: 항목 사이 이동(표의 행, 버튼).
- Tab / Shift+Tab: 화면의 영역 사이 이동.
- Enter 또는 클릭: 선택한 버튼 실행. 경고 표에서는 「수정」.
- `Esc`: 이전 화면으로 돌아가기(메뉴에서는 종료).
- `a`: 어느 화면에서나 도움말.
- `s`: 어느 화면에서나 설정.
- `t`: 다음 테마(저장됨).
- `r`: 화면을 다시 그리고, 터미널 크기를 표시하고, 상태를 다시 읽기.
- `q`: 확인 후 종료.
- `Ctrl+P`: 명령(테마, 스크린샷 폴더에 SVG 스크린샷 저장, 종료).

[↑ 목차](#목차)

---

## 테마와 터미널

열 가지 `omega-*` 테마가 OMEGA 도구 모음의 나머지와 공유됩니다:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- `t`로 테마를 바꾸거나 설정(`s`)에서 하나를 고르십시오. 선택은 저장됩니다.
- HTML 내보내기에는 자체 테마가 있습니다: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail은 감지된 터미널에 맞춰 **렌더링 프로필**로 시각적 복잡도를 조정합니다: 완전, 표준, 축소,
  Mono(ASCII 전용).

| 최소 크기 | 프로필 | 대표 터미널 |
|---|---|---|
| 120×32 이상 | 완전 | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 이상 | 표준 | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 이상 | 축소 | urxvt, xterm, 최신 SSH |
| 80×24 미만 | Mono(ASCII 전용) | Linux TTY, 오래된 SSH |

창 크기를 바꾼 뒤에는 `r`로 터미널 크기를 다시 읽습니다. 크기는 위쪽, 테마 옆에 표시됩니다.

[↑ 목차](#목차)

---

## 파일, 서비스, 호환성

### omega-tail 폴더 안

omega-tail의 모든 상태는 `~/omega-tail/var/`에 있으며, 시작할 때 다시 만들어지고 결코 게시되지 않습니다:

```text
var/
├── settings.json         설정(언어, 테마, 폴더, 임곗값, 게이트 규칙)
├── omega-jeton.json      설치 토큰(omega-connect)
├── porte/                게이트 설정, 인증서, 신뢰 목록과 블랙리스트, AS / 국가 데이터베이스
├── veille/               자동 감시 로그
├── survie/               수정된 파일의 원본, 서킷 브레이커 상태
├── funnel/sauvegardes/   각 변경 전의 게시 상태(최근 50개)
├── exports/              내보낸 보고서, 로그, 목록
└── screenshots/          스크린샷(Ctrl+P)
```

### 시스템 (해당 보호를 활성화한 경우에만)

각 파일은 명령을 보여 준 뒤 sudo로 설치되며, omega-tail의 반대 작업으로 제거됩니다.

| 파일 또는 서비스 | 설치하는 작업 | 제거하는 작업 |
|---|---|---|
| `omega-tail-porte` 서비스(systemd, OpenRC 또는 runit)와 `omega-tail-porte-certificat`(systemd 타이머, 또는 crontab의 표시된 한 줄) | 보호 활성화 | 보호 비활성화 |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf`(systemd가 아니면 제어 그룹) | 자원 제한 적용 | 자원 제한 해제 |
| `omega-tail-retablir-*` 타이머(차단 후 재개) | 서킷 브레이커 | 차단 종료 |
| `omega-tail-veille` 서비스 | 감시 활성화 | 감시 비활성화 |
| `omega-bouclier-wg` 서비스, nftables 테이블, `/etc/omega-bouclier-wg/` | 방패: 설치 | 방패: 제거 |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | IP 포워딩 활성화 | 파일 삭제 |

`tailscaled`의 `override.conf` 파일은 있더라도 결코 수정되지 않습니다.

### init 시스템

| | systemd | OpenRC | runit |
|---|---|---|---|
| `tailscaled` 서비스 | `systemctl` | `rc-service` | `sv` |
| 로그 | `journalctl` | 서비스 파일 | `svlogd`, `socklog` |
| 자원 제한 | systemd 추가 설정 파일 | 제어 그룹(cgroup v2) | 제어 그룹(cgroup v2) |
| 일시 차단 | systemd 타이머 | 여러분의 계정으로 분리 실행되는 프로세스 | 여러분의 계정으로 분리 실행되는 프로세스 |
| 게이트, 감시, 방패 | systemd 서비스 | OpenRC 서비스 | runit 서비스 |

systemd가 아닌 경우 `tailscaled`가 다시 시작되면 제어 그룹을 통한 자원 제한이 사라집니다: 그러면 경고가 다시
적용하도록 제안합니다.

### IPv4와 IPv6

게이트, 목록, 그룹화, 방패는 두 주소 체계를 모두 처리합니다. 집계하는 접두사는 IPv4에서 /24, IPv6에서 /64이며,
`::ffff:a.b.c.d` 형태로 보이는 IPv4 주소는 IPv4 주소로 처리합니다.

[↑ 목차](#목차)

---

## 보안

omega-tail은 인터넷에 노출된 서비스에 작용합니다. 결코 상황을 악화시키지 않도록 설계되었습니다.

- **결코 root가 아님**: 애플리케이션, HAProxy 게이트, 감시는 여러분의 계정으로 실행됩니다. sudo는 서비스를 설치하거나
  제거할 때만, 명령을 먼저 보여 준 뒤 요청합니다.
- **비공개 채널**: 게이트의 관리 소켓은 700 폴더 안에서 600 모드입니다. 테이블 동기화는 같은 폴더의 소켓을
  거칩니다.
- **되돌리기**: Funnel의 모든 전환은 백업되고 검사되며, 실패하면 이전 상태로 되돌립니다.
- **관찰 먼저**: 게이트, 그룹화, 방패는 관찰 모드로 설치됩니다. 여러분이 결정하기 전에는 아무것도 거부되지 않습니다.
- **tailnet은 결코 끊기지 않음**: 게이트는 여러분의 머신을 항상 허용하며, 서킷 브레이커는 Funnel만 끊습니다.
- **검증된 입력**: 정규 형식의 주소나 네트워크만 HAProxy에 도달합니다. tailnet 머신이 알린 이름은 표시하기 전에
  정리됩니다.
- **감사**: 코드는 감사를 받았습니다(claude-security, 2026-11-25). 지적된 7개 항목은, 그중 어느 것도 방문자가
  원격으로 악용할 수 없었으며, 같은 날 수정되었습니다.
- 먼저 테스트 머신이나 관찰 모드에서 시험하고, IPv4 테스트에는 RFC 5737 문서용 네트워크를 사용하십시오:
  `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ 목차](#목차)

---

## 테스트와 품질

테스트 모음은 **179개의 테스트**로 구성됩니다: 도메인, 유스 케이스, 인프라(시뮬레이션된 Funnel 사용), 실제
스타일시트를 쓰는 Textual 화면, init 시스템, 보안. 코드는 `ruff`, `mypy`, `import-linter`(계층 규칙)로
검사합니다. `tests/` 폴더는 아카이브에 포함되어 있습니다.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

대부분의 테스트에는 Tailscale도, HAProxy도, root도 필요하지 않습니다.

[↑ 목차](#목차)

---

## 프로젝트 상태

### 작동 중인 부분

- Tailscale의 완전한 제어: 서비스, 연결, 설정, 게시, 네트워크, 로그.
- TLS 이전의 HAProxy 게이트, 2026-11-23부터 운영 중, 규칙, 목록, 그룹화, 공격 모드 포함.
- 생존: 자원 제한, 서킷 브레이커, 자동 감시.
- WireGuard 포트 방패, 2026-11-24부터 운영 중.
- 보고서와 TXT, HTML, JSON 내보내기.
- omega-connect 및 omega-fire와 호환.

### 알려진 한계

- OpenRC와 runit의 서비스는 테스트로 다루지만, 아직 실제 머신에서 검증되지 않았습니다.
- 게이트는 한 포트에서 HTTPS로, 경로 `/`로 게시된 Funnel을 보호합니다.
- 그룹화에는 Lua와 함께 컴파일된 HAProxy가 필요합니다. Lua가 없으면 게이트는 그룹화 없이 동작합니다.
- 재부팅 없이 업데이트된 커널에는 방패를 설치할 수 없습니다(모듈 없음): 화면이 이를 알려 줍니다.
- 인터넷 회선 자체를 포화시키는 공격은 머신에 설치된 도구가 막을 수 있는 범위 밖입니다.
- Funnel로 게시한 사이트의 처리량은 여전히 Tailscale의 릴레이와 공유기에 의해 제한됩니다.

[↑ 목차](#목차)

---

## 제거

먼저 omega-tail에서, 시스템에 설치한 것을 이 순서로 제거하십시오:

1. **Funnel 방화벽 → 보호 비활성화**(Funnel이 이전처럼 되돌아갑니다).
2. **생존 → 감시 비활성화**.
3. **생존 → WireGuard 포트 방패 → 제거**.
4. **생존 → 자원 제한 해제**.

그런 다음 폴더를 삭제합니다:

```bash
rm -rf ~/omega-tail
```

다른 곳에 둔 내보내기, `~/.bashrc`나 `~/.zshrc`의 `omega-tail` 별칭, 그리고 활성화했었다면
`/etc/sysctl.d/99-omega-tail-forwarding.conf` 파일은 직접 삭제하십시오. Tailscale 운영자 권한은
`sudo tailscale set --operator=`로 회수합니다.

[↑ 목차](#목차)

---

## 라이선스

Omega-Tail은 **MIT** 라이선스로 배포됩니다. 전체 내용은 [`LICENSE`](../../../LICENSE) 파일을 참조하십시오.

AS / 국가 데이터베이스는 IP Geolocation by [DB-IP](https://db-ip.com)를
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 라이선스로 사용합니다.

[↑ 목차](#목차)

---

> **Omega-Tail — Tailscale을 제어하고, Funnel을 보호합니다.**
>
> Tailscale을 위한 TUI 인터페이스, 그리고 모든 암호화 이전에 남용을 거부하는 게이트.
