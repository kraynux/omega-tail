<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**FUNNEL 用ファイアウォールを内蔵した TAILSCALE 管理ツール**

OMEGA-TAIL は OMEGA スイートのツールの 1 つで、マシン上の **Tailscale** を操作し、そのマシンが **Tailscale Funnel** でインターネットにサービスを公開するときにマシンを**保護**します。

> [kraynux](https://github.com/kraynux) が [Omega-Server](https://kraynux.snake-mackarel.ts.net) のために開発 · [公式ページ](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/ja/) · [スクリーンショット](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 インターフェース・ドキュメント・エクスポート・訪問者向けページは **17 言語** に対応しています — [インターフェースの言語](#インターフェースの言語) を参照してください。  
**言語：**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** は [Textual](https://textual.textualize.io/) で構築された Python の TUI（ターミナルユーザーインターフェース）アプリケーションです。コマンドを 1 つも覚えることなく、1 つのインターフェースから **Tailscale** を高度なモードで管理・調整できます。さらに、マシンのサービスをインターネット全体に開放する **Funnel** モードのために、保護機能（ファイアウォール、封じ込め、サバイバル…）を追加します。

マシンを変更する操作はすべて、最初にそのコマンドを表示します。sudo のパスワードは操作ごとにターミナルで入力し、あなたの知らないうちにバックグラウンドで何かが実行されることはありません。

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ja/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ja/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ja/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ja/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ja/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/ja/omega-tail/F.png" width="32%" />
</p>

本プロジェクトは **Clean Architecture（クリーンアーキテクチャ）** の原則に従って設計されており、`app/` をコンポジションルートとして、ビジネスドメイン、オーケストレーション、インフラストラクチャ、インターフェースが分離されています。

## 目次

- [概要](#概要)
- [Tailscale と Funnel を理解する](#tailscale-と-funnel-を理解する)
- [機能](#機能)
- [保護機能の詳細](#保護機能の詳細)
- [測定結果](#測定結果)
- [アーキテクチャ](#アーキテクチャ)
- [前提条件](#前提条件)
- [インストール](#インストール)
- [使い方](#使い方)
- [テーマとターミナル](#テーマとターミナル)
- [ファイル、サービス、互換性](#ファイルサービス互換性)
- [セキュリティ](#セキュリティ)
- [テストと品質](#テストと品質)
- [プロジェクトの状況](#プロジェクトの状況)
- [アンインストール](#アンインストール)
- [ライセンス](#ライセンス)

---

## 概要

### なぜ omega-tail なのか

Tailscale Funnel は、ルーターのポートを開けることなく、マシンのサービスをインターネットに公開します。訪問者は Tailscale のリレーを経由してやって来ます。ネットワークの面では簡単で安全ですが、弱点が 1 つ残ります。

- **暗号化のコスト。** 既定の Funnel モードでは、訪問者ごとの TLS ハンドシェイクを行うのはマシン上の `tailscaled` サービスです。小さなマシンで測定すると、これは**接続コストの約 80 %** を占めます。毎秒数百の新規接続があればプロセッサーは飽和します。ごく普通のパソコン 1 台と簡単なスクリプトだけで、サイトとマシンを落とせてしまいます。
- **見えない訪問者。** 通常のファイアウォール（nftables、ufw、fail2ban）にはこれらの訪問者が見えません。訪問者は Tailscale のトンネルを通って暗号化されたまま、リレーのアドレスで到着するからです。
- **散らばった設定。** Tailscale の設定（オペレーター、出口ノード、ルート、SSH、シールド…）は数が多く、コマンドと Web コンソールに分かれており、中には現在のセッションを切断しうるものもあります。

### 目的

- 1 つのインターフェースから Tailscale を完全に操作し、各設定には 1 文の説明を付ける。
- あらゆる暗号化の**前に**、各訪問者の実アドレスを見たうえで、悪用的な接続を拒否する。
- 攻撃を受けてもマシンを稼働させ続ける。管理用のアクセスとほかのサービスには引き続き到達できる。
- 何も押し付けない。提案し、コマンドを示し、確認を求め、元に戻せるようにする。
- systemd、OpenRC、runit のいずれでも、あらゆる Linux ディストリビューションで動作する。

### omega-tail ができること

- Tailscale、マシン、公開中のものの状態を表示し、修正する画面へ移動できるアラートを出します。
- `tailscaled` を起動・停止・再起動します。セッションが Tailscale 経由の場合はセーフガードが働きます。
- 接続、アカウント、`tailscale set` のすべての設定を管理し、適用前に検証します。
- Serve と Funnel のサービスを公開・撤去・一時停止・テストし、バックアップと復元も行います。
- tailnet のデバイス、その経路（直接またはリレー経由）、ネットワーク診断、ログを表示します。
- Funnel とあなたのサイトの間に HAProxy の**ゲート**を置きます。アドレス単位・プレフィックス単位のルール、全体予算、信頼リストとブラックリスト、JA4 フィンガープリント・接続元ネットワーク（AS）・国によるグループ化、自動攻撃モードを備えます。
- `tailscaled` を封じ込め、Funnel を一時的または完全に遮断し、自動監視によってそれを自動で行うこともできます。
- `tailscaled` の WireGuard ポートを nftables テーブル（シールド）で保護します。
- マシンと直近 7 日間の攻撃についてのレポートを TXT、HTML、JSON で作成します。

### 本プロジェクトが行わないこと

- Tailscale を置き換えるものではありません。Tailscale を操作するものです。
- インターネット回線そのもの（ルーター、回線）を飽和させるボリューム型攻撃からは守れません。
- Tailscale の Web 管理コンソール（アクセスポリシー、出口ノードの承認、tailnet での Funnel の有効化）は扱いません。
- Funnel 以外の方法で公開されたサービスは保護しません。そうしたポートには omega-fire があります。
- root では決して動作せず、あなたの同意なしにバックグラウンドで何かを実行することもありません。
- Windows と macOS では動作しません。

[↑ 目次](#目次)

---

## Tailscale と Funnel を理解する

omega-tail はいくつかの Tailscale の概念を前提としています。この節ではそれらをまとめており、ほかの前提知識は必要ありません。

### 用語

| 用語 | 意味 |
|---|---|
| **Tailnet** | あなたの Tailscale プライベートネットワーク。同じアカウント（または同じ組織）に接続されたすべてのマシンです。各マシンは `100.x.y.z` のアドレス（範囲 100.64.0.0/10）と `fd7a:115c:a1e0::/48` の IPv6 アドレスを受け取ります。 |
| **`tailscaled`** | マシン上で動作するサービス（デーモン）。WireGuard の暗号化トンネルと Tailscale のネットワークスタックを保持し、Serve と Funnel ではあなたのサービスへの中継を担います。 |
| **`tailscale`** | `tailscaled` を操作するコマンド（`tailscale status`、`tailscale set`、`tailscale funnel`…）。omega-tail があなたの代わりに使います。 |
| **WireGuard** | マシン間で使われる暗号化トンネルのプロトコル。そのために `tailscaled` は UDP ポート（既定は 41641）で待ち受けます。このポートはルーターによって開かれることがよくあります（UPnP）。 |
| **DERP リレー（DERP relay）** | 2 台のマシンが直接つながれないとき（難しい NAT）にトラフィックを中継する Tailscale のサーバー。「直接」経路のほうが高速です。 |
| **MagicDNS** | tailnet のマシン名。`machine.nom-du-tailnet.ts.net` の形式です。 |
| **Serve** | ローカルのサービス（サイト、API…）を **tailnet のみに**、有効な `*.ts.net` 証明書付きの HTTPS で公開すること。 |
| **Funnel** | ローカルのサービスを **インターネット全体に**、`https://machine.nom-du-tailnet.ts.net` というアドレスで公開すること。開けられるのは 443、8443、10000 番ポートのみです。 |
| **Funnel リレー（Funnel relay）** | インターネットからの訪問者を受け取り、あなたの tailnet に入れる Tailscale のサーバー（「funnel-ingress-node」として表示されます）。 |
| **オペレーター（operator）** | sudo なしで Tailscale を設定できる Linux アカウント（`tailscale set --operator=…`）。omega-tail は sudo で一度だけ設定を提案します。 |
| **出口ノード（exit node）** | tailnet 内のマシンで、別のマシンがインターネットへのトラフィックをすべてそこ経由で流すもの（VPN のように）。Tailscale のコンソールで承認される必要があります。 |
| **アドバタイズするサブネット（subnet router）** | あるマシンが tailnet の残りから到達できるようにするローカルネットワーク（例：`192.168.1.0/24`）。 |
| **シールド（shields up）** | tailnet から来るすべての着信接続を拒否する Tailscale の設定。 |
| **Tailscale SSH** | Tailscale が提供し、tailnet のポリシーで許可される SSH サーバー。 |
| **PROXY v2 ヘッダー** | 接続の先頭に付け加える短いヘッダーで、訪問者の実アドレスを受け手に伝えます。 |
| **JA4 フィンガープリント** | ソフトウェアが TLS 接続を開く方法の特徴を表すシグネチャ。ブラウザーと攻撃ツールでは異なります。 |
| **AS（自律システム）** | アドレスの接続元ネットワーク。プロバイダー、ホスティング事業者、クラウド。 |

### 訪問者の経路

**omega-tail なしの既定の Funnel。** `tailscaled` がすべてを行います。WireGuard トンネルを復号し、訪問者との TLS ハンドシェイクを行い、リクエストを HTTP であなたのサイトへ中継します。マシンのファイアウォールには訪問者がまったく見えず、新しい接続のたびに `tailscaled` に大きなコストがかかります。

```text
訪問者 ──HTTPS──▶ Funnel リレー ──WireGuard──▶ tailscaled (TLS + HTTP 中継) ──HTTP──▶ あなたのサイト
                  (Tailscale)                  └── コストはすべてここ
```

**omega-tail のゲートを使った Funnel。** Funnel は TCP モードに切り替わります。`tailscaled` はもう TLS を処理せず、まだ暗号化されたままのストリームを、訪問者の実アドレス（PROXY v2 ヘッダー）を先頭に付けてゲートへ渡します。ゲートはあらゆる暗号化の**前に**判断します。拒否された接続にはほとんどコストがかからず、許可された接続だけが OpenSSL で復号されます。OpenSSL は `tailscaled` の TLS より高速です。

```text
訪問者 ──HTTPS──▶ Funnel リレー ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                    │
                                                    ▼
                                     omega-tail ゲート (HAProxy, 127.0.0.1)
                                     ├── TLS 前に拒否：ブラックリスト、レート、予算、宛先名、グループ化
                                     └── 許可：TLS (証明書 *.ts.net) ──HTTP──▶ あなたのサイト
```

ゲートはマシンのループバックでのみ待ち受け、あなたのアカウントで動作します。あなたの tailnet のマシンは、どのルールよりも先に常に許可されます。フィルタリングされるのは Funnel の訪問者だけです。

### Tailscale で許可しておくこと（管理コンソール）

これらの設定は Tailscale の Web コンソールで一度だけ行います。omega-tail はこれらを変更しません。

- tailnet で **MagicDNS** と **HTTPS 証明書** を有効にする（Serve、Funnel、ゲートの証明書に必要）。
- tailnet のアクセスポリシーで、そのマシンに **Funnel を許可** する（属性 `funnel`）。
- 出口ノードやアドバタイズするサブネットの場合：コンソールでそれらを **承認** する。

[↑ 目次](#目次)

---

## 機能

メインメニューは 6 項目ずつの 2 列です。操作するための **TAILSCALE** と、守るための **保護** です。

### TAILSCALE

#### 1. ダッシュボード

- **Tailscale**：サービス、接続状態、実行中とインストール済みのバージョン、マシン名、アドレス、アカウント、オンラインのデバイス、キーの有効期限、オペレーター、提供している出口ノードと使用中の出口ノード、アドバタイズするサブネット。
- **マシン**：マシン全体の CPU、コアごとの負荷、温度、メモリー、`tailscaled` の CPU とメモリー、封じ込め、続いて各保護機能の状態（Funnel、ファイアウォールと攻撃モード、ブラックリスト、監視、シールド）。
- **公開**：公開中の各ポート、インターネット向け（Funnel）か tailnet 向け（Serve）か、そのモードと転送先。
- **アラート**：重大なものから順に並び、「修正」で該当する画面が開きます。例：サービスの停止、インストール済みだが未適用の更新、期限切れが近いキー、保護なしで公開された Funnel、高温、リソースを使いすぎている・または封じ込められていない `tailscaled`、増え続けるブラックリスト。
- しきい値（CPU、負荷、温度、メモリー、`tailscaled`）に応じて、値は緑、オレンジ、赤で表示されます。

#### 2. tailscaled サービス

- init システムから見た状態、実行中とインストール済みのバージョン、起動コマンド、追加設定ファイル、封じ込め。
- **起動**、**停止**、**再起動**（たとえばインストール済みの更新を適用するため）。
- **セーフガード**：セッションが Tailscale 経由（tailnet 経由の SSH）の場合、停止すると再起動できなくなるため、「停止」は 2 回目の確認を求めます。
- **起動を修正**：起動時に `tailscale up` を実行する追加設定ファイルを見つけます。このファイルは、最初に設定を変更した時点でマシンを tailnet から外してしまうおそれがあります。修正内容は表示され、元のファイルは保存されます。

#### 3. 接続と設定

- **ログイン**、**ログアウト**、**アカウントを追加**、**アカウントを切り替え**、**完全ログアウト**（マシン名の入力が必要）。
- **`tailscale set` のすべての設定**、それぞれに 1 文の説明付き：マシン名と別名、ルート、tailnet の DNS、シールド、ステートフルフィルタリング、netfilter モード、出口ノード、ローカルネットワークへのアクセス、このマシンを出口ノードとして提供、アドバタイズするサブネット、Tailscale SSH、Web インターフェース、更新、ピアリレー、オペレーター。
- 入力中は、枠の中に **変更前 → 変更後** とコマンドが表示されます。適用後は、読み直した各値に ✔（反映済み）または ✖（未反映）の印が付きます。
- 変更によって Tailscale 経由のセッションが切断されるおそれがある場合は、警告が表示されます。
- **IP 転送**：マシンが出口ノードとして動作する場合やサブネットをアドバタイズする場合に、ボタン 1 つで有効にできます。

#### 4. 公開

- マシンが公開しているすべて：ポート、公開（Funnel）か tailnet（Serve）か、モード、パス、転送先、保護。
- ローカルのサービスを HTTPS、HTTP、TCP、または TLS 終端で **公開**、**撤去**、**Funnel を一時停止** と **Funnel を復旧**（まったく同じ状態に）。
- **エンドツーエンドテスト**：訪問者と同じように実際に接続します（応答、時間、証明書、TLS のバージョン）。
- **バックアップ**：各変更前の状態（最新 50 件）で、復元できます。
- 変更はすべて検証されます。差異があれば公開設定を作り直し、それができなければ変更前の状態に戻します。

#### 5. ネットワークとデバイス

- tailnet の **デバイス**：システム、オンラインかどうか、経路（直接またはリレー経由）、最終確認時刻、アドレス、やり取りしたトラフィック。Tailscale の Funnel リレーは既定で非表示です。
- **Tailscale Ping**（経路と遅延）、**これは誰？**（tailnet のアドレスが誰のものか）。
- **ネットワーク診断**：UDP、IPv4 / IPv6、NAT の種類、ルーターによるポート開放（UPnP、NAT-PMP、PCP）、最寄りのリレーと遅延。
- **DNS**、**tailnet ロック**、Tailscale の **内部カウンター**。
- 読み取り専用：この画面で設定が変わることはありません。

#### 6. ログ

- `tailscaled` のログ（journalctl、または systemd 以外ではサービスのログファイル）とゲートのログ。絞り込みとエクスポートが可能です。
- 各情報にはテーマから取った固有の色が付きます：日付、プロセス、メッセージのカテゴリー（制御、ネットワーク、DNS、WireGuard エンジン）、太字のアドレス、赤のエラー、オレンジの警告。ゲートのログでは拒否理由、グループ化、AS、国。

### 保護

#### 7. Funnel ファイアウォール

- ディストリビューションのパッケージマネージャー（pacman、apt、dnf、zypper、apk、xbps、emerge）で **HAProxy をインストール**。
- **保護を有効化**：`*.ts.net` 証明書、リスト、検証済みの設定、ゲートのサービス、Funnel の切り替え、続いてインターネットからのテスト。失敗した場合は、元の公開設定がただちに戻されます。
- **保護を無効化**：Funnel は以前とまったく同じ状態に戻され、検証されます。
- ホット適用される **ルール**、リスクなしでしきい値を調整するための **観察** モード、**グループ化**（[保護機能の詳細](#保護機能の詳細) を参照）。
- AS / 国の **データベースを更新**（DB-IP Lite）。別プロセスで実行されます。

#### 8. サバイバル

- **`tailscaled` の封じ込め**：CPU の上限、重みと優先度、SSH アクセスを優先するオプション。
- **Funnel ブレーカー**：CPU と温度のしきい値、10 分間の遮断（自動で再開）または完全遮断。
- **自動監視**：画面の前に誰もいなくても同じことを行います。
- **WireGuard ポートのシールド**：専用画面へのボタン（観察、有効、設置、再設置、撤去、委任）。

#### 9. 攻撃と判断

- ゲートのカウンター（受信、暗号化前に拒否、許可、処理中）と最も活発なアドレス。2 秒ごとに読み直され、各アドレスの国、AS、状態が表示されます。
- **ブロック**、**ブラックリスト**、**ブロック解除**、**信頼**：ゲートを再起動せずにただちに適用されます。通知は、行った操作とそのアドレスの位置付けを 1 行で伝えます。
- **フィンガープリント**、**AS**、**国** の表示。攻撃モードの状態と、グループ化によって拒否された接続。
- **ブラックリストの管理**：追加日時と追加元付きの完全な一覧、追加、削除、TXT ファイルのインポート（重複、すでに含まれるネットワーク、tailnet のアドレスは除外）、プレビュー付きのパージ（経過期間ごと、古い順に N 件、行の範囲、追加元、すべて）、TXT（再インポート可能）、HTML、JSON でのエクスポート。上限は 50 000 件です。

#### 10. レポート

- omega-tail がマシンについて把握しているすべての事実：Tailscale、公開、マシン、ファイアウォール、サバイバル、アラート、そしてゲートのログから読み取った **直近 7 日間の攻撃**。
- **プライバシー**：既定では Tailscale のアカウントも、tailnet のデバイス名やアドレスも含まないので、そのまま誰かに送れます。
- **TXT**、**HTML**（テーマを選択可能）、**JSON** でエクスポート。**エクスポートを見る** でフォルダーをブラウザーで開きます。

#### 11. 設定

- インターフェースとエクスポートの言語、インターフェースとエクスポートのテーマ、エクスポートとスクリーンショットのフォルダー、およびそのパージ。

#### 12. ヘルプ

- 画面ごとの節、キーボードショートカット、コマンドライン、そして **お問い合わせとサポート**。

[↑ 目次](#目次)

---

## 保護機能の詳細

それぞれの保護機能は特定の脅威に対応しており、どれも強制ではありません。

| 保護機能 | 何に対して | 場所 |
|---|---|---|
| ゲート（ルール） | 1 つまたは少数のアドレスからの集中的な接続、サイトを宛先としない接続 | Funnel ファイアウォール |
| グループ化 | アドレスが分散した攻撃（数千のアドレスがそれぞれ 1 接続） | Funnel ファイアウォール |
| ブラックリスト | 攻撃元として知られ、長期間保持されるアドレスとネットワーク | 攻撃と判断 |
| 封じ込め | 攻撃を受けてマシン全体を占有しかねない `tailscaled` | サバイバル |
| ブレーカー | それでもマシンが飽和している：Funnel を一時的に遮断 | サバイバル |
| 自動監視 | 同じことを、画面の前に誰もいなくても | サバイバル |
| WireGuard シールド | `tailscaled` のポートへの UDP パケットの洪水（Funnel が開いているかどうかにかかわらず） | サバイバル |

### ゲート（Funnel ファイアウォール）

ルールは次の順序で、すべて暗号化の前に適用されます。

1. **tailnet のマシン**（100.64.0.0/10、fd7a:115c:a1e0::/48）：常に許可。
2. **信頼リスト**：決して制限されません。**ブラックリスト**：削除されるまで拒否されます。
3. **アドレスごとのレート**（既定は 10 秒あたり 40 接続）：これを超えると、そのアドレスは選んだ時間（既定は 60 分）ブロックされます。
4. **プレフィックスごとのレート**：IPv4 は /24、IPv6 は /64。
5. 1 秒あたりに許可する接続の **全体予算**：プロセッサーが溢れることはありません。
6. **宛先名**：マシンの名前を宛先としない接続は拒否されます。

ゲートの `*.ts.net` 証明書は Tailscale に要求し、毎日確認し、有効期限の 30 日前にホットで更新します。**観察** モードはすべてを数えますが、何も拒否しません。

### グループ化（フィンガープリント、AS、国）

アドレスが分散した攻撃では、アドレスごとのルールには各アドレスが 1 回しか見えません。そこでゲートは、各クライアントを **JA4 フィンガープリント**、**AS**、**国** でも分類し、グループごとのレートを数えます。

- **自動攻撃モード**：着信接続が毎秒 80 件（調整可能）を超えると、ゲートは自動的に攻撃モードに入り、5 分間落ち着いた状態が続くと抜けます。
- 攻撃モードのときのみ：急増する未知のフィンガープリント、ホスティング事業者やクラウドの AS（リストは変更可能）、あなたのリストにある国（既定は空）がそのレートを超えると拒否されます。
- **一般的なブラウザー**（Chrome、Edge、Firefox）はこれらのルールの影響を決して受けません。**既知のクライアント**（直近 24 時間以内に許可されたもの）は全体予算より優先されます。
- **学習**：7 日間、ゲートはあなたのサイトでよく見られるフィンガープリントを学習します（攻撃中は学習しません）。それまでグループ化は観察モードのままです。
- 攻撃時以外は 10 接続に 1 つを分類し、攻撃中はすべてを分類します。
- AS / 国のデータベースは **DB-IP Lite** で、月に 1 回ダウンロード・更新されます。

### サバイバル

- **封じ込め**：別の追加設定ファイルで `tailscaled` に上限を設け（たとえば 4 スレッドのマシンで 1 コア分）、優先度を下げます。あなた自身の設定は決して変更されません。
- **ブレーカー**：`tailscaled` が CPU しきい値（既定は 60 秒間 1 コアの 80 %）を超え続けたとき、または温度が 85 °C に達したとき、omega-tail は Funnel を 10 分間遮断する（自動で再開、まったく同じ状態に、omega-tail を閉じていても）、完全に遮断する、または待つ、のいずれかを提案します。tailnet が遮断されることはありません。
- **自動監視**（既定は無効）：あなたのアカウントで動作するサービスが、しきい値超過が 3 回続くと自動で Funnel を遮断します。1 回目は 15 分、2 回目は 30 分、その後は 1 時間で、自動で再開します。

### WireGuard ポートのシールド

`tailscaled` は、UDP ポートで受信するパケットが毎秒 100 000 個あると、たとえ無効なパケットでもプロセッサーの約 1 コアを消費します。シールドは、ネットワークカード上で `tailscaled` の手前に置かれる nftables テーブルです。

- **既知のピア**（`tailscaled` が送信している相手）は決して制限されません。
- ハンドシェイクは送信元ごとに毎秒 20 回までに制限されます。
- それ以外の送信元には予算があります（それぞれ毎秒 500 パケット、合計 5 000）。
- WireGuard ではないパケットは拒否されます。

まず **観察** で設置し、その後 **有効** に切り替えます。omega-connect で連携していれば、**omega-fire**（3.7.0 以降）が omega-tail の代わりにシールドを設置・管理できます。同じテーブルのまま、テーブル自体に手を触れずに管理者だけが替わります。

[↑ 目次](#目次)

---

## 測定結果

omega-tail の選択は測定に基づいています。測定には、保護対象と同じ世代のマシン（2010 年から 2016 年のプロセッサー、ほとんどは AES アクセラレーションなし）を使いました。

| 測定項目 | 結果 |
|---|---|
| 既定の Funnel で接続コストに占める TLS の割合 | 約 80 % |
| ゲートで **拒否** された接続のコスト（既定の Funnel との比較） | **4.6 分の 1** |
| ゲートで **許可** された接続のコスト（既定の Funnel との比較） | **2 分の 1** |
| ゲート使用時のスループット、接続を開いたまま（`tailscaled` のような Go 実装の TLS との比較） | リクエスト **+15 %**、CPU −20 % |
| WireGuard シールド：`tailscaled` の 1 コアを丸ごと占有していた洪水 | 1 コアの **1 %** |
| サービス（ゲート、監視、シールド）のメモリー | 約 67 MB |

つまり、ゲートがサイトのスループットを落とすことはありません。これらのマシンでは、omega-tail の有無にかかわらず、制約となるのは暗号化そのものです。また本番環境では、いずれにせよ Funnel は Tailscale のリレーとルーターを経由します。

[↑ 目次](#目次)

---

## アーキテクチャ

```text
src/omega_tail/
├── app/              コンポジションルート：各層を組み立てる、エントリーポイント（インターフェース、コマンドライン）
├── core/             共有定数
├── domain/           純粋なビジネスロジック：ゲートのルール、アラート、ブレーカー、監視、ブラックリスト…
├── application/      ユースケース：公開、ファイアウォール、サバイバル、レポート、設定
├── ports/            アプリケーションが期待する契約（Protocol）
├── infrastructure/   Tailscale、HAProxy、nftables、systemd / OpenRC / runit、ログ、エクスポート、Lua スクリプト
├── interfaces/       tui/（Textual）、cli/（コマンドライン）、shared/（ヘルプ、レポート、表示）
└── shared/           言語（gettext）
```

### 設計原則

- `domain/` には読み書きが一切含まれません。すべてマシンなしでテストできます。
- `application/` はドメインとポートを通じてユースケースを調整します。インターフェースとコマンドラインは同じユースケースを呼び出します。
- コマンドを実行するのは `infrastructure.commands` と `infrastructure.privileged` だけです。インターフェースが直接コマンドを実行することはありません。これらのルールは自動的に検証されます（import-linter）。
- インターフェースは、OMEGA スイート全体で共有されるライブラリ [omega-lib](https://github.com/kraynux)（テーマ、ターミナル検出、言語、お問い合わせとサポート、WireGuard シールド）に基づいています。PyPI には公開されておらず、アーカイブに同梱されています（`vendor/omega-lib/`）。
- 時間のかかる呼び出し（Tailscale、HAProxy、ディスク、ネットワーク）はすべてバックグラウンドタスクで実行されるため、インターフェースが固まることはありません。

[↑ 目次](#目次)

---

## 前提条件

### システム

- Linux、あらゆるディストリビューション（Arch Linux とその派生でテスト済み）。
- Python 3.10 以上と `venv` モジュール。
- init システム：**systemd**、**OpenRC**、または **runit**。
- マシンを変更する操作のための `sudo`（操作ごとに求められ、起動時には求められません）。
- 80×24 以上のターミナル（[テーマとターミナル](#テーマとターミナル) を参照）。

### Tailscale

- インストール済みで接続済みの **Tailscale**（`tailscale` クライアントと `tailscaled` サービス）。バージョン 1.104 でテスト済み。
- Funnel の場合：Tailscale のコンソールで MagicDNS、HTTPS 証明書、Funnel が許可されていること（[Tailscale で許可しておくこと](#tailscale-で許可しておくこと管理コンソール) を参照）。

### Python の依存関係

`install.sh` が仮想環境にインストールします。

- `textual`：インターフェース。
- `omega-lib`：OMEGA スイートの共有ライブラリ。アーカイブに同梱されています。

### 必須コンポーネントとオプションのコンポーネント

omega-tail は存在するものを検出し、使えるものだけを有効にします。

| コンポーネント | 役割 | 区分 |
|---|---|---|
| Tailscale（`tailscale`、`tailscaled`） | omega-tail が操作するすべて | **必須** |
| Python 3.10+、`textual`、`omega-lib` | アプリケーション本体 | **必須** |
| systemd、OpenRC、または runit | ゲート、監視、シールドのサービス | **必須**（いずれか 1 つ） |
| HAProxy 3.x | Funnel ファイアウォールのゲート | オプション（omega-tail からインストール可能） |
| Lua 対応の HAProxy | グループ化（フィンガープリント、AS、国） | オプション（一般的なディストリビューションでは対応済み） |
| nftables（`nft_limit` を含むカーネル） | WireGuard ポートのシールド | オプション |
| システムジャーナルの読み取り（`systemd-journal`、`adm`、または `wheel` グループ） | ログ、攻撃レポート | 推奨 |
| ブラウザーとデスクトップ | ブラウザーでの「エクスポートを見る」（なければ omega-tail 内で閲覧） | オプション |
| omega-connect | レジストリ、同期、スイートの更新 | オプション |
| omega-fire 3.7.0+ | omega-fire からの WireGuard シールドの管理 | オプション |

[↑ 目次](#目次)

---

## インストール

公式アーカイブは `.tar.gz` 形式で提供されます。インストール前に、一緒に公開されている `sha.txt` ファイルで整合性を確認してください。

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **以下の 3 つの方法は初回インストール用です。** `~/omega-tail` がすでに存在する場合は、[更新](#更新) の節を参照してください。既存の `omega-tail` フォルダーの中からこれらのコマンドを再実行しないでください。`tar` が入れ子の `omega-tail/omega-tail/` を作ってしまいます。

インストールのどの手順でも root 権限は必要ありません。omega-tail は通常のユーザーとして起動します。

### 方法 1 — インストールスクリプト

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ すでに omega-tail フォルダーの中にいるようです — README の更新セクションを参照してください。" >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ ここにはすでに展開済みのため、この手順を省略します。" || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail はすでに存在するため、移動を省略します。" || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

このスクリプトは仮想環境を作成し、依存関係をインストールし（同梱の omega-lib を先に）、ランチャーを実行可能にし、omega-connect が読み取るインストールトークンを書き込み、`omega-tail` エイリアスの作成を提案します。何度実行しても問題ありません。

### 方法 2 — 堅牢な完全インストール

このコマンドは再実行できます。すでに完了した手順は省略されます。

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ すでに omega-tail フォルダーの中にいるようです — README の更新セクションを参照してください。" >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail はすでに存在するため、展開を省略します。" || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv はすでに存在するため、この手順を省略します。" || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail をインストールしました。./omega-tail.sh を実行してください。"
```

### 方法 3 — 詳細なインストール

```bash
# 0. 既存の omega-tail の中から再実行していないことを確認する
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ すでに omega-tail フォルダーの中にいるようです — README の更新セクションを参照してください。" >&2; exit 1; }

# 1. 展開する
[ -d omega-tail ] && echo "ℹ️ ここにはすでに展開済みのため、この手順を省略します。" || tar -xzf omega-tail-0.7.0.tar.gz

# 2. ホームに移動する
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail はすでに存在するため、移動を省略します。" || mv omega-tail ~/

# 3. プロジェクトに入る
cd ~/omega-tail/

# 4. 仮想環境を作成する
[ -f .venv/bin/activate ] && echo "ℹ️ .venv はすでに存在するため、作成を省略します。" || python3 -m venv .venv

# 5. 依存関係をインストールする（同梱の omega-lib を先に）
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. ランチャーを実行可能にする
chmod +x omega-tail.sh install.sh

# 7. インストールトークンを書き込む（omega-connect が読み取る。任意）
./omega-tail.sh synchro jeton

# 8. 起動する
./omega-tail.sh
```

Debian、Ubuntu とその派生では、`venv` モジュールが Python と一緒にインストールされているとは限りません：`sudo apt install python3-venv`。

### 更新

omega-tail のサービス（ゲート、監視）は `~/omega-tail/var/` のファイルを使います。そのため更新では **このフォルダーをそのまま残す** 必要があります。アーカイブには `var/` が含まれておらず、既存のインストールの上に展開されます。

アーカイブがあるフォルダー（**`~/omega-tail` 以外**）から実行します。

```bash
# 1. 現在のインストールをバックアップする（var/ を含む）
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. 新しいバージョンを上書きで展開する（var/ は保持される）
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. 再インストールする（依存関係、ランチャー、インストールトークン）
cd ~/omega-tail
./install.sh

# 4. omega-tail を再起動する
./omega-tail.sh
```

ゲートが有効な場合は、**Funnel ファイアウォール →「ルールを適用」** で新しいバージョンの設定をホットで再生成します。自動監視が有効な場合は、**サバイバル →「監視を有効化」** で新しいコードを使って再起動します。omega-connect で更新することもできます（Updater 画面）。

### Bash または Zsh のエイリアス

`install.sh` がエイリアスの作成を提案します。手動で追加するには：

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

エイリアスの名前は `tail` ではなく `omega-tail` です。システムの `tail` コマンドを隠さないためです。

[↑ 目次](#目次)

---

## 使い方

### 起動

```bash
cd ~/omega-tail
./omega-tail.sh

# またはエイリアスを作成済みなら単に：
omega-tail
```

ランチャーは権限昇格を一切求めません。omega-tail はあなたのアカウントで動作し、sudo は必要な操作のときだけ、コマンドを先に表示したうえで、ターミナルで求められます。

### おすすめの最初の手順

Funnel で公開したサイトを保護するには、次の順序で進めます。

1. **ダッシュボード**：アラートを読む。sudo なしで Tailscale を設定できるよう **オペレーターになる**（sudo で一度だけ）。
2. **サバイバル → 封じ込めを適用**：`tailscaled` がマシン全体を占有できなくなります。
3. **公開**：サイトを **ポート 443 の HTTPS**、パス `/` で公開し、**エンドツーエンドテスト** を行う。
4. **Funnel ファイアウォール → HAProxy をインストール**、続いて **保護を有効化**。まずは **観察** モードで。
5. 数日後、**攻撃と判断**：カウンターに悪用的な接続しか表れていなければ、ゲートを **通常** モードに切り替える。
6. **グループ化** に観察モードで 7 日間学習させ、その後 **適用** に切り替える。
7. **サバイバル → WireGuard ポートのシールド**：観察で設置し、その後有効に切り替える。
8. 画面の前に誰もいないマシンの場合：**サバイバル → 監視を有効化**。

### インターフェースの言語

17 言語：フランス語、英語、スペイン語、ポルトガル語（ブラジル）、イタリア語、ドイツ語、オランダ語、ポーランド語、ロシア語、中国語、ベトナム語、タイ語、インドネシア語、日本語、韓国語、ヒンディー語、アラビア語。

- 設定で選択します（`s` キー、「Langue / Language」、このラベルは翻訳されません）。インターフェースを再起動するだけで適用されます。
- 一時的に指定する場合：`OMEGA_TAIL_LANG=en ./omega-tail.sh`。
- Linux のテキストコンソール（TTY）では、コンソールのフォントにその文字がない言語は、そのセッションの間は英語で表示されます。アラビア語は右から左に表示されます。
- **エクスポートの言語**（レポート、ブラックリスト、ログ）は別に設定し、既定は「インターフェースと同じ」です。

### お問い合わせとサポート

ヘルプ（`a` キー）には **お問い合わせとサポート** 画面があります。

- *コーヒーをおごる*（開発者の PayPal ページ）
- *サポートに連絡*（メールアドレスとサイトのフォームをそのまま表示）
- *ユーザーとして登録（匿名）*
- *更新を確認*

登録は任意で、既定では無効、送信は一度だけです。利用者の数と、希望すればその大陸または国（選択式のリストのみ、自由入力なし）を数えるためだけに使われます。送信されるのは、ランダムに生成したキー、ソフトウェア名（`omega-tail`）とそのバージョンだけで、名前、マシン名、設定、tailnet のアドレスは決して送信されません。同じ画面からいつでも取り消せます（*登録を取り消す*）。更新の確認は、サイトで公開されているバージョンの一覧を読むだけで、クリックしない限り行われません。

### ほかの omega ツールとの連携

- **omega-connect**：`install.sh` は、ツールとそのバージョンを記述するインストールトークン（`var/omega-jeton.json`）を書き込みます。何も実行しません。omega-connect はこれをレジストリ、同期、修復、更新、インストールに使います。`./omega-tail.sh synchro jeton` で手動で書き直せます。
- **omega-fire**（3.7.0 以降）は、omega-connect で連携していれば WireGuard ポートのシールドを設置・管理できます。omega-fire のルール一覧には、追加元 omega-tail として表示されます。

### コマンドライン

すべてのコマンドは `./omega-tail.sh …`（エイリアスがあれば `omega-tail …`）の形で入力します。

| コマンド | 役割 |
|---|---|
| `omega-tail` | インターフェース |
| `omega-tail etat [--format json]` | Tailscale とマシンの状態、およびアラート。テキストまたはスクリプト向け |
| `omega-tail aide` | テキスト形式の完全なヘルプ |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | レポートを表示または保存 |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Funnel を遮断または再開 |
| `omega-tail veille etat` | 自動監視の状態と直近の数行 |
| `omega-tail porte etat` | ゲートの状態とカウンター |
| `omega-tail porte certificat [--si-besoin]` | ゲートの `*.ts.net` 証明書を更新 |
| `omega-tail porte groupes` | グループ化：攻撃モード、フィンガープリント、AS、国 |
| `omega-tail porte base` | AS / 国のデータベースを更新 |
| `omega-tail porte bloquer ADRESSE [--toujours]` | アドレスまたはネットワークをブロック（`--toujours` を付けるとブラックリストへ） |
| `omega-tail porte debloquer ADRESSE` | ブロック解除 |
| `omega-tail porte confiance ADRESSE` | 信頼する |
| `omega-tail synchro jeton` | インストールトークンを書き込む（omega-connect） |
| `omega-tail --version` | バージョン |

### 全体の流れ

1. 起動画面、続いて 2 列（TAILSCALE と保護）のメインメニュー。
2. 各画面のタイトルの下にある **ステータスバー** がすべてをまとめて表示します：サービス、マシンと `tailscaled` の CPU、温度、メモリー、Funnel、ファイアウォール、監視、接続。5 秒ごとに読み直されます。
3. マシンを変更する操作はすべてコマンドを表示してから確認を求めます。sudo はターミナルで入力し、その後インターフェースに戻ります。
4. 重要な操作（完全ログアウト、ブラックリストの全パージ）では、単語の入力が求められます。
5. 結果は、読み直した状態で検証したうえで 1 行で表示されます。

### ナビゲーション

- 上下の矢印キー：要素（表の行、ボタン）の間を移動。
- Tab / Shift+Tab：画面の領域の間を移動。
- Enter またはクリック：選択したボタンを実行。アラートの表では「修正」。
- `Esc`：前の画面に戻る（メニューでは終了）。
- `a`：どの画面からでもヘルプ。
- `s`：どの画面からでも設定。
- `t`：次のテーマ（保存されます）。
- `r`：画面を再描画し、ターミナルのサイズを表示し、状態を読み直す。
- `q`：確認のうえ終了。
- `Ctrl+P`：コマンド（テーマ、スクリーンショットフォルダーへの SVG 形式のスクリーンショット、終了）。

[↑ 目次](#目次)

---

## テーマとターミナル

10 種類の `omega-*` テーマが OMEGA スイートの他のツールと共通です：

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- `t` でテーマを切り替えるか、設定（`s`）から選択します。選択は保存されます。
- HTML エクスポートには独自のテーマがあります：`omega-base`、`omega-burn`、`omega-neon`、`light-basic`、`light-alt`。
- omega-tail は検出したターミナルに合わせて、**描画プロファイル** により視覚的な複雑さを調整します：完全、標準、縮小、Mono（ASCII のみ）。

| 最小サイズ | プロファイル | 代表的なターミナル |
|---|---|---|
| 120×32 以上 | 完全 | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 以上 | 標準 | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 以上 | 縮小 | urxvt, xterm, 最新の SSH |
| 80×24 未満 | Mono（ASCII のみ） | Linux TTY, 古い SSH |

ウィンドウのサイズを変えたあとは、`r` でターミナルのサイズを読み直します。サイズは上部、テーマの横に表示されます。

[↑ 目次](#目次)

---

## ファイル、サービス、互換性

### omega-tail のフォルダー内

omega-tail の状態はすべて `~/omega-tail/var/` にあり、起動時に作り直され、決して公開されません。

```text
var/
├── settings.json         設定（言語、テーマ、フォルダー、しきい値、ゲートのルール）
├── omega-jeton.json      インストールトークン（omega-connect）
├── porte/                ゲートの設定、証明書、信頼リストとブラックリスト、AS / 国のデータベース
├── veille/               自動監視のログ
├── survie/               変更したファイルの元のファイル、ブレーカーの状態
├── funnel/sauvegardes/   各変更前の公開設定（最新 50 件）
├── exports/              エクスポートしたレポート、ログ、リスト
└── screenshots/          スクリーンショット（Ctrl+P）
```

### システム上（該当する保護機能を有効にした場合のみ）

各ファイルはコマンドを表示したうえで sudo で設置され、omega-tail の逆の操作で撤去されます。

| ファイルまたはサービス | 設置する操作 | 撤去する操作 |
|---|---|---|
| `omega-tail-porte` サービス（systemd、OpenRC、または runit）と `omega-tail-porte-certificat`（systemd タイマー、または crontab の印付きの 1 行） | 保護を有効化 | 保護を無効化 |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf`（systemd 以外ではコントロールグループ） | 封じ込めを適用 | 封じ込めを撤去 |
| `omega-tail-retablir-*` タイマー（遮断後の自動再開） | ブレーカー | 遮断の終了 |
| `omega-tail-veille` サービス | 監視を有効化 | 監視を無効化 |
| `omega-bouclier-wg` サービス、nftables テーブル、`/etc/omega-bouclier-wg/` | シールド：設置 | シールド：撤去 |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | IP 転送を有効化 | ファイルの削除 |

`tailscaled` の `override.conf` ファイルは、存在していても決して変更されません。

### init システム

| | systemd | OpenRC | runit |
|---|---|---|---|
| `tailscaled` サービス | `systemctl` | `rc-service` | `sv` |
| ログ | `journalctl` | サービスのログファイル | `svlogd`、`socklog` |
| 封じ込め | systemd の追加設定ファイル | コントロールグループ（cgroup v2） | コントロールグループ（cgroup v2） |
| 一時的な遮断 | systemd タイマー | あなたのアカウントで動く切り離されたプロセス | あなたのアカウントで動く切り離されたプロセス |
| ゲート、監視、シールド | systemd サービス | OpenRC サービス | runit サービス |

systemd 以外では、`tailscaled` が再起動するとコントロールグループによる封じ込めは失われます。その場合はアラートが再適用を提案します。

### IPv4 と IPv6

ゲート、リスト、グループ化、シールドは両方のアドレスファミリーを扱います。数えるプレフィックスは IPv4 で /24、IPv6 で /64 です。`::ffff:a.b.c.d` の形で現れる IPv4 アドレスは、IPv4 アドレスとして扱われます。

[↑ 目次](#目次)

---

## セキュリティ

omega-tail はインターネットに公開されたサービスに作用します。状況を決して悪化させないように設計されています。

- **root を使わない**：アプリケーション、HAProxy のゲート、監視はあなたのアカウントで動作します。sudo が求められるのはサービスの設置や撤去のときだけで、コマンドが先に表示されます。
- **非公開のチャネル**：ゲートの管理用ソケットは、モード 700 のフォルダー内にモード 600 で置かれます。ゲートのテーブルの同期も、同じフォルダー内のソケットを通じて行われます。
- **ロールバック**：Funnel の切り替えはすべてバックアップされ、検証され、失敗した場合は以前の状態に戻されます。
- **まず観察**：ゲート、グループ化、シールドは観察モードで設置されます。あなたが決めるまで、何も拒否されません。
- **tailnet は決して遮断されない**：ゲートは常にあなたのマシンを許可し、ブレーカーが遮断するのは Funnel だけです。
- **入力の検証**：HAProxy に渡るのは正規形のアドレスやネットワークだけです。tailnet のマシンが申告する名前は、表示前に無害化されます。
- **監査**：コードは監査済みです（claude-security、2026-11-25）。指摘された 7 点は、いずれも訪問者がリモートから悪用できるものではなく、当日中にすべて修正されました。
- まずはテスト用のマシンか観察モードで試し、IPv4 の試験には RFC 5737 のドキュメント用ネットワークを使ってください：`192.0.2.0/24`、`198.51.100.0/24`、`203.0.113.0/24`。

[↑ 目次](#目次)

---

## テストと品質

テストスイートには **179 件のテスト** があります：ドメイン、ユースケース、インフラストラクチャ（シミュレートした Funnel を使用）、実際のスタイルシートを使った Textual の画面、init システム、セキュリティ。コードは `ruff`、`mypy`、`import-linter`（層のルール）で検証されます。`tests/` フォルダーはアーカイブに含まれています。

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

ほとんどのテストは、Tailscale も HAProxy も root も必要としません。

[↑ 目次](#目次)

---

## プロジェクトの状況

### 稼働しているポイント

- Tailscale の完全な操作：サービス、接続、設定、公開、ネットワーク、ログ。
- TLS の前に置く HAProxy のゲート。2026-11-23 から本番稼働中で、ルール、リスト、グループ化、攻撃モードを備えます。
- サバイバル：封じ込め、ブレーカー、自動監視。
- WireGuard ポートのシールド。2026-11-24 から本番稼働中。
- レポートと TXT、HTML、JSON のエクスポート。
- omega-connect および omega-fire と互換。

### 既知の制限

- OpenRC と runit でのサービスはテストでカバーされていますが、まだ実機では検証されていません。
- ゲートが保護するのは、1 つのポートで、パス `/` を使い、HTTPS で公開された Funnel です。
- グループ化には Lua 付きでコンパイルされた HAProxy が必要です。Lua がなくても、ゲートはグループ化なしで動作します。
- カーネルを更新して再起動していない状態では、シールドを設置できません（モジュールがないため）。画面にそのことが表示されます。
- インターネット回線そのものを飽和させる攻撃は、マシンにインストールされたツールでは対処できません。
- Funnel で公開されたサイトのスループットは、引き続き Tailscale のリレーとルーターによって制限されます。

[↑ 目次](#目次)

---

## アンインストール

まず omega-tail から、システムに設置したものを次の順序で撤去します。

1. **Funnel ファイアウォール → 保護を無効化**（Funnel は以前の状態に戻ります）。
2. **サバイバル → 監視を無効化**。
3. **サバイバル → WireGuard ポートのシールド → 撤去**。
4. **サバイバル → 封じ込めを撤去**。

次にフォルダーを削除します。

```bash
rm -rf ~/omega-tail
```

ほかの場所に置いたエクスポート、`~/.bashrc` または `~/.zshrc` の `omega-tail` エイリアス、そして有効にしていた場合は `/etc/sysctl.d/99-omega-tail-forwarding.conf` ファイルを、手動で削除してください。Tailscale のオペレーター権限は `sudo tailscale set --operator=` で取り消せます。

[↑ 目次](#目次)

---

## ライセンス

Omega-Tail は **MIT** ライセンスで配布されています。全文はファイル [`LICENSE`](../../../LICENSE) を参照してください。

AS / 国のデータベースは [DB-IP](https://db-ip.com) による IP Geolocation を使用しており、[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) ライセンスで提供されています。

[↑ 目次](#目次)

---

> **Omega-Tail — Tailscale を操作し、Funnel を守る。**
>
> Tailscale のための TUI インターフェースと、あらゆる暗号化の前に悪用を拒否するゲート。
