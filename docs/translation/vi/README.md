<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**Trình điều khiển TAILSCALE với tường lửa tích hợp cho FUNNEL**

OMEGA-TAIL là công cụ của bộ OMEGA dùng để điều khiển **Tailscale** trên một máy và **bảo vệ** máy đó khi nó
công bố một dịch vụ ra Internet qua **Tailscale Funnel**.

> Được phát triển bởi [kraynux](https://github.com/kraynux) cho [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Trang chính thức](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/vi/) · [Ảnh chụp màn hình](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Giao diện, tài liệu, bản xuất và trang dành cho khách truy cập có sẵn bằng **17 ngôn ngữ** — xem [Ngôn ngữ giao diện](#ngôn-ngữ-giao-diện).  
**Ngôn ngữ:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](../id/README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** là một ứng dụng TUI (Terminal User Interface) viết bằng Python, xây dựng với
[Textual](https://textual.textualize.io/). Nó cho phép quản lý và tinh chỉnh **Tailscale** ở chế độ nâng cao từ một
giao diện, không cần nhớ một lệnh nào. Nó còn bổ sung các lớp bảo vệ (tường lửa, giới hạn tài nguyên, sinh tồn…) cho
chế độ **Funnel**, chế độ mở một dịch vụ của máy ra toàn bộ Internet.

Mỗi thao tác làm thay đổi máy đều hiển thị lệnh của nó trước. Mật khẩu sudo được nhập trong terminal, từng thao tác
một, và không có gì được chạy nền mà bạn không biết.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/vi/omega-tail/F.png" width="32%" />
</p>

Dự án được thiết kế theo các nguyên tắc của **Clean Architecture**, với `app/` là gốc kết hợp (composition root):
miền nghiệp vụ, điều phối, hạ tầng và giao diện được tách biệt.

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Hiểu về Tailscale và Funnel](#hiểu-về-tailscale-và-funnel)
- [Tính năng](#tính-năng)
- [Chi tiết các lớp bảo vệ](#chi-tiết-các-lớp-bảo-vệ)
- [Kết quả đo](#kết-quả-đo)
- [Kiến trúc](#kiến-trúc)
- [Yêu cầu](#yêu-cầu)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Chủ đề và terminal](#chủ-đề-và-terminal)
- [Tệp, dịch vụ và khả năng tương thích](#tệp-dịch-vụ-và-khả-năng-tương-thích)
- [Bảo mật](#bảo-mật)
- [Kiểm thử và chất lượng](#kiểm-thử-và-chất-lượng)
- [Tình trạng dự án](#tình-trạng-dự-án)
- [Gỡ cài đặt](#gỡ-cài-đặt)
- [Giấy phép](#giấy-phép)

---

## Giới thiệu

### Vì sao có omega-tail

Tailscale Funnel công bố một dịch vụ của máy ra Internet mà không cần mở cổng trên modem/router: khách truy cập đi
qua các máy chuyển tiếp của Tailscale. Về mặt mạng, cách này đơn giản và an toàn, nhưng vẫn còn một điểm yếu.

- **Chi phí mã hóa.** Ở chế độ Funnel mặc định, chính dịch vụ `tailscaled` của máy thực hiện bắt tay TLS với từng
  khách truy cập. Đo trên một máy nhỏ, phần này chiếm khoảng **80 % chi phí của một kết nối**. Chỉ vài trăm kết nối
  mới mỗi giây là đủ làm bão hòa bộ xử lý: một máy tính bình thường, với một script đơn giản, có thể đánh sập trang
  web và cả máy.
- **Khách truy cập vô hình.** Các tường lửa thông thường (nftables, ufw, fail2ban) không thấy những khách truy cập
  này: họ đến dưới dạng đã mã hóa, qua đường hầm của Tailscale, với địa chỉ của một máy chuyển tiếp.
- **Thiết lập rải rác.** Các thiết lập của Tailscale (người vận hành, nút thoát, tuyến, SSH, lá chắn…) rất nhiều,
  chia giữa dòng lệnh và bảng quản trị web, và một số có thể cắt phiên làm việc hiện tại.

### Mục tiêu

- Điều khiển Tailscale hoàn toàn từ một giao diện, với một câu giải thích cho mỗi thiết lập.
- Từ chối các kết nối lạm dụng **trước** mọi bước mã hóa, khi thấy được địa chỉ thật của từng khách truy cập.
- Giữ máy đứng vững khi bị tấn công: phần quản trị và các dịch vụ khác vẫn truy cập được.
- Không bao giờ áp đặt: đề xuất, hiển thị lệnh, hỏi, và luôn có thể quay lại.
- Hoạt động trên mọi bản phân phối Linux, dưới systemd, OpenRC hoặc runit.

### omega-tail làm gì

- Hiển thị trạng thái của Tailscale, của máy và của những gì đang được công bố, với các cảnh báo dẫn tới màn hình
  có thể sửa lỗi.
- Khởi động, dừng và khởi động lại `tailscaled`, với một rào chắn an toàn nếu phiên của bạn đi qua Tailscale.
- Quản lý kết nối, tài khoản và mọi thiết lập của `tailscale set`, được kiểm tra trước khi áp dụng.
- Công bố, gỡ, tạm dừng và thử các dịch vụ của Serve và Funnel, với sao lưu và khôi phục.
- Hiển thị các thiết bị của tailnet, đường đi của chúng (trực tiếp hoặc qua chuyển tiếp), chẩn đoán mạng và nhật ký.
- Đặt một **cổng gác** HAProxy giữa Funnel và trang web của bạn: quy tắc theo địa chỉ, theo tiền tố, ngân sách toàn
  cục, danh sách tin cậy và danh sách đen, gom nhóm theo dấu vân tay JA4, mạng nguồn (AS) và quốc gia, chế độ tấn
  công tự động.
- Giới hạn tài nguyên của `tailscaled`, ngắt Funnel tạm thời hoặc hoàn toàn, và có thể tự làm việc đó nhờ chế độ
  giám sát tự động.
- Bảo vệ cổng WireGuard của `tailscaled` bằng một bảng nftables (lá chắn).
- Tạo báo cáo về máy và các cuộc tấn công trong 7 ngày gần nhất, dưới dạng TXT, HTML hoặc JSON.

### Những gì dự án không làm

- Không thay thế Tailscale: nó điều khiển Tailscale.
- Không bảo vệ trước một cuộc tấn công dung lượng làm bão hòa chính đường truyền Internet (modem/router, đường
  dây).
- Không quản lý bảng quản trị web của Tailscale (chính sách truy cập, phê duyệt nút thoát, bật Funnel cho
  tailnet).
- Không bảo vệ một dịch vụ được công bố bằng cách khác ngoài Funnel: với các cổng đó, đã có omega-fire.
- Không bao giờ chạy với quyền root và không chạy gì ở chế độ nền khi chưa có sự đồng ý của bạn.
- Không hoạt động trên Windows hay macOS.

[↑ Mục lục](#mục-lục)

---

## Hiểu về Tailscale và Funnel

omega-tail giả định bạn biết một vài khái niệm của Tailscale. Phần này tập hợp chúng lại, không giả định gì thêm.

### Từ vựng

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Tailnet** | Mạng riêng Tailscale của bạn: mọi máy kết nối vào cùng một tài khoản (hoặc cùng một tổ chức). Mỗi máy nhận một địa chỉ dạng `100.x.y.z` (dải 100.64.0.0/10) và một địa chỉ IPv6 trong `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | Dịch vụ (daemon) chạy trên máy: nó duy trì đường hầm mã hóa WireGuard, ngăn xếp mạng của Tailscale và, với Serve và Funnel, việc chuyển tiếp tới các dịch vụ của bạn. |
| **`tailscale`** | Lệnh điều khiển `tailscaled` (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail dùng lệnh này thay bạn. |
| **WireGuard** | Giao thức đường hầm mã hóa dùng giữa các máy. Để làm việc đó, `tailscaled` lắng nghe trên một cổng UDP (mặc định 41641), thường được modem/router mở sẵn (UPnP). |
| **Máy chuyển tiếp DERP (DERP relay)** | Các máy chủ của Tailscale chuyển tiếp lưu lượng khi hai máy không thể kết nối trực tiếp với nhau (NAT khó). Đường đi « trực tiếp » nhanh hơn. |
| **MagicDNS** | Tên của các máy trong tailnet, dạng `machine.nom-du-tailnet.ts.net`. |
| **Serve** | Công bố một dịch vụ cục bộ (một trang web, một API…) **chỉ cho tailnet**, qua HTTPS với chứng chỉ `*.ts.net` hợp lệ. |
| **Funnel** | Công bố một dịch vụ cục bộ **cho toàn bộ Internet**, tại địa chỉ `https://machine.nom-du-tailnet.ts.net`. Chỉ có thể mở các cổng 443, 8443 và 10000. |
| **Máy chuyển tiếp Funnel (Funnel relay)** | Các máy chủ của Tailscale nhận khách truy cập từ Internet và đưa họ vào tailnet của bạn (chúng xuất hiện dưới tên « funnel-ingress-node »). |
| **Người vận hành (operator)** | Một tài khoản Linux được phép điều chỉnh Tailscale mà không cần sudo (`tailscale set --operator=…`). omega-tail đề xuất việc này một lần, qua sudo. |
| **Nút thoát (exit node)** | Một máy trong tailnet mà máy khác cho toàn bộ lưu lượng Internet của mình đi qua (giống một VPN). Nó phải được phê duyệt trong bảng quản trị của Tailscale. |
| **Mạng con được quảng bá (subnet router)** | Một mạng cục bộ (ví dụ `192.168.1.0/24`) mà một máy làm cho phần còn lại của tailnet truy cập được. |
| **Lá chắn (shields up)** | Thiết lập của Tailscale từ chối mọi kết nối đến từ tailnet. |
| **SSH Tailscale (Tailscale SSH)** | Một máy chủ SSH do Tailscale cung cấp, được cho phép bởi chính sách của tailnet. |
| **Tiêu đề PROXY v2** | Một tiêu đề ngắn được thêm vào đầu kết nối để truyền địa chỉ thật của khách truy cập cho bên nhận. |
| **Dấu vân tay JA4** | Chữ ký của cách một phần mềm mở kết nối TLS: một trình duyệt và một công cụ tấn công không có cùng dấu vân tay. |
| **AS (hệ thống tự trị)** | Mạng nguồn của một địa chỉ: nhà cung cấp truy cập, nhà cung cấp hosting, đám mây. |

### Đường đi của một khách truy cập

**Funnel mặc định, không có omega-tail.** `tailscaled` làm tất cả: nó giải mã đường hầm WireGuard, thực hiện bắt tay
TLS với khách truy cập, rồi chuyển tiếp yêu cầu bằng HTTP tới trang web của bạn. Không tường lửa nào của máy thấy
khách truy cập, và mỗi kết nối mới đều tốn kém cho `tailscaled`.

```text
Khách truy cập ──HTTPS──▶ Chuyển tiếp Funnel ──WireGuard──▶ tailscaled (TLS + chuyển tiếp HTTP) ──HTTP──▶ trang của bạn
                          (Tailscale)                       └── toàn bộ chi phí nằm ở đây
```

**Funnel với cổng gác của omega-tail.** Funnel chuyển sang chế độ TCP: `tailscaled` không làm TLS nữa, nó chuyển
luồng dữ liệu vẫn còn mã hóa tới cổng gác, kèm phía trước là địa chỉ thật của khách truy cập (tiêu đề PROXY v2). Cổng
gác quyết định **trước** mọi bước mã hóa: một kết nối bị từ chối gần như không tốn gì, và chỉ các kết nối được chấp
nhận mới được giải mã, bởi OpenSSL, nhanh hơn TLS của `tailscaled`.

```text
Khách truy cập ──HTTPS──▶ Chuyển tiếp Funnel ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                                 │
                                                                 ▼
                                                  Cổng gác omega-tail (HAProxy, 127.0.0.1)
                                                  ├── từ chối trước TLS: danh sách đen, tốc độ, ngân sách, tên đích, gom nhóm
                                                  └── chấp nhận: TLS (chứng chỉ *.ts.net) ──HTTP──▶ trang của bạn
```

Cổng gác chỉ lắng nghe trên giao diện loopback của máy và chạy dưới tài khoản của bạn. Các máy trong tailnet của bạn
luôn được chấp nhận, trước mọi quy tắc: chỉ khách truy cập qua Funnel bị lọc.

### Những gì Tailscale phải cho phép (bảng quản trị)

Các thiết lập này được làm một lần, trong bảng quản trị web của Tailscale; omega-tail không thay đổi chúng.

- **MagicDNS** và **chứng chỉ HTTPS** được bật cho tailnet (cần cho Serve, Funnel và chứng chỉ của cổng gác).
- **Funnel được cho phép** cho máy trong chính sách truy cập của tailnet (thuộc tính `funnel`).
- Với nút thoát hoặc các mạng con được quảng bá: **phê duyệt** chúng trong bảng quản trị.

[↑ Mục lục](#mục-lục)

---

## Tính năng

Menu chính có hai cột, mỗi cột sáu mục: **TAILSCALE** để điều khiển, **BẢO VỆ** để phòng thủ.

### TAILSCALE

#### 1. Bảng điều khiển

- **Tailscale**: dịch vụ, trạng thái kết nối, phiên bản đang chạy và đã cài, tên máy, địa chỉ, tài khoản, thiết bị
  trực tuyến, ngày hết hạn của khóa, người vận hành, nút thoát được đề xuất và đang dùng, mạng con được quảng bá.
- **Máy**: CPU của toàn máy, tải theo từng lõi, nhiệt độ, bộ nhớ, CPU và bộ nhớ của `tailscaled`, giới hạn tài
  nguyên, rồi trạng thái các lớp bảo vệ (Funnel, tường lửa và chế độ tấn công, danh sách đen, giám sát, lá chắn).
- **Công bố**: từng cổng được công bố, cho Internet (Funnel) hoặc cho tailnet (Serve), chế độ và đích của nó.
- **Cảnh báo**, từ nghiêm trọng nhất đến ít nghiêm trọng nhất, với « Sửa » mở màn hình liên quan. Ví dụ: dịch vụ
  đã dừng, bản cập nhật đã cài nhưng chưa áp dụng, khóa sắp hết hạn, Funnel được công bố mà không có bảo vệ, nhiệt
  độ cao, `tailscaled` quá ngốn tài nguyên hoặc chưa bị giới hạn, danh sách đen phình to.
- Giá trị hiển thị màu xanh, cam hoặc đỏ theo các ngưỡng (CPU, tải, nhiệt độ, bộ nhớ, `tailscaled`).

#### 2. Dịch vụ tailscaled

- Trạng thái theo hệ thống init, phiên bản đang chạy và đã cài, lệnh khởi chạy, các tệp bổ sung (drop-in), giới hạn
  tài nguyên.
- **Khởi động**, **Dừng**, **Khởi động lại** (ví dụ để áp dụng một bản cập nhật đã được cài).
- **Rào chắn an toàn**: nếu phiên của bạn đi qua Tailscale (SSH qua tailnet), Dừng sẽ yêu cầu xác nhận lần thứ hai,
  vì bạn sẽ không thể khởi động lại được nữa.
- **Sửa khởi động**: phát hiện một tệp bổ sung chạy `tailscale up` khi khởi động và có nguy cơ đưa máy ra khỏi
  tailnet ở lần đổi thiết lập đầu tiên; bản sửa được hiển thị và bản gốc được giữ lại.

#### 3. Kết nối và thiết lập

- **Đăng nhập**, **Đăng xuất**, **Thêm tài khoản**, **Đổi tài khoản**, **Đăng xuất vĩnh viễn** (phải gõ tên máy).
- **Mọi thiết lập của `tailscale set`**, mỗi thiết lập kèm câu giải thích: tên và biệt danh của máy, tuyến, DNS của
  tailnet, lá chắn, lọc có trạng thái, chế độ netfilter, nút thoát, truy cập mạng cục bộ, đề xuất máy làm nút thoát,
  mạng con được quảng bá, SSH Tailscale, giao diện web, cập nhật, chuyển tiếp ngang hàng (peer relay), người vận
  hành.
- Trong lúc nhập, một khung hiển thị **trước → sau** và lệnh; sau khi áp dụng, mỗi giá trị được đọc lại sẽ được đánh
  dấu ✔ (đã có hiệu lực) hoặc ✖ (chưa).
- Một cảnh báo báo trước khi một thay đổi có thể cắt một phiên đi qua Tailscale.
- **Chuyển tiếp IP**: bật bằng một nút khi máy làm nút thoát hoặc quảng bá mạng con.

#### 4. Công bố

- Mọi thứ máy đang công bố: cổng, công khai (Funnel) hoặc tailnet (Serve), chế độ, đường dẫn, đích, bảo vệ.
- **Công bố** một dịch vụ cục bộ qua HTTPS, HTTP, TCP hoặc TLS kết thúc tại máy (TLS-terminated); **Gỡ**; **Tạm dừng
  Funnel** và **Khôi phục Funnel** (y như cũ).
- **Thử đầu cuối**: một kết nối thật, như một khách truy cập (phản hồi, thời gian, chứng chỉ, phiên bản TLS).
- **Bản sao lưu**: trạng thái trước mỗi thay đổi (50 bản gần nhất), có thể khôi phục.
- Mỗi thay đổi đều được kiểm tra; nếu có sai lệch, việc công bố được dựng lại, nếu không thì trạng thái cũ được đặt
  lại.

#### 5. Mạng và thiết bị

- **Thiết bị** của tailnet: hệ điều hành, trực tuyến hay không, đường đi (trực tiếp hoặc qua chuyển tiếp), lần thấy
  gần nhất, địa chỉ, lưu lượng trao đổi; các máy chuyển tiếp Funnel của Tailscale được ẩn theo mặc định.
- **Ping Tailscale** (đường đi và độ trễ), **Đây là ai?** (một địa chỉ của tailnet thuộc về ai).
- **Chẩn đoán mạng**: UDP, IPv4 / IPv6, loại NAT, mở cổng bởi modem/router (UPnP, NAT-PMP, PCP), máy chuyển tiếp gần
  nhất và độ trễ.
- **DNS**, **khóa tailnet (tailnet lock)** và **bộ đếm nội bộ** của Tailscale.
- Chỉ đọc: không có gì trong màn hình này thay đổi một thiết lập.

#### 6. Nhật ký

- Nhật ký của `tailscaled` (journalctl, hoặc các tệp của dịch vụ khi không dùng systemd) và nhật ký của cổng gác, có
  thể lọc và xuất.
- Mỗi thông tin có màu riêng, lấy từ chủ đề: ngày giờ, tiến trình, loại thông báo (điều khiển, mạng, DNS, bộ máy
  WireGuard), địa chỉ in đậm, lỗi màu đỏ, cảnh báo màu cam; với cổng gác: lý do từ chối, gom nhóm, AS và quốc gia.

### BẢO VỆ

#### 7. Tường lửa Funnel

- **Cài HAProxy** bằng trình quản lý gói của bản phân phối (pacman, apt, dnf, zypper, apk, xbps, emerge).
- **Bật bảo vệ**: chứng chỉ `*.ts.net`, các danh sách, cấu hình đã kiểm tra, dịch vụ cổng gác, chuyển Funnel sang
  rồi thử từ Internet; nếu thất bại, cấu hình công bố ban đầu được đặt lại ngay lập tức.
- **Tắt bảo vệ**: Funnel được đặt lại chính xác như trước, có kiểm tra.
- **Quy tắc** áp dụng nóng, chế độ **quan sát** để chỉnh ngưỡng mà không rủi ro, **gom nhóm** (xem
  [Chi tiết các lớp bảo vệ](#chi-tiết-các-lớp-bảo-vệ)).
- **Cập nhật cơ sở dữ liệu** AS / quốc gia (DB-IP Lite), trong một tiến trình riêng.

#### 8. Sinh tồn

- **Giới hạn tài nguyên của `tailscaled`**: trần CPU, trọng số và mức ưu tiên, tùy chọn ưu tiên truy cập SSH.
- **Cầu dao Funnel**: ngưỡng CPU và nhiệt độ, ngắt 10 phút (tự động bật lại) hoặc ngắt hoàn toàn.
- **Giám sát tự động**: cùng việc đó, khi không có ai trước màn hình.
- **Lá chắn cổng WireGuard**: nút dẫn tới màn hình riêng của nó (quan sát, hoạt động, đặt, đặt lại, gỡ, giao lại).

#### 9. Tấn công và quyết định

- Bộ đếm của cổng gác (đã nhận, bị từ chối trước khi mã hóa, được chấp nhận, đang diễn ra) và các địa chỉ hoạt động
  nhiều nhất, đọc lại mỗi 2 giây, kèm quốc gia, AS và trạng thái của từng địa chỉ.
- **Chặn**, **Danh sách đen**, **Bỏ chặn**, **Tin cậy**: áp dụng ngay, không cần khởi động lại cổng gác; thông báo nói
  trong một dòng thao tác đã làm và vị trí của địa chỉ.
- Các chế độ xem **Dấu vân tay**, **AS** và **Quốc gia**; trạng thái chế độ tấn công và các kết nối bị gom nhóm từ
  chối.
- **Quản lý danh sách đen**: danh sách đầy đủ kèm ngày thêm và nguồn gốc, thêm, xóa, nhập một tệp TXT (loại bỏ mục
  trùng, mạng đã được bao phủ và địa chỉ của tailnet), dọn dẹp có xem trước (theo độ cũ, N mục cũ nhất, một khoảng
  dòng, một nguồn gốc, tất cả), xuất TXT (nhập lại được), HTML và JSON. Tối đa 50 000 mục.

#### 10. Báo cáo

- Mọi điều omega-tail biết về máy, dưới dạng dữ kiện: Tailscale, công bố, máy, tường lửa, sinh tồn, cảnh báo, và
  **các cuộc tấn công trong 7 ngày gần nhất** đọc từ nhật ký của cổng gác.
- **Quyền riêng tư**: theo mặc định, không có tài khoản Tailscale cũng như tên và địa chỉ của các thiết bị trong
  tailnet, để có thể gửi cho người khác.
- Xuất **TXT**, **HTML** (chủ đề tùy chọn) và **JSON**; **Xem bản xuất** mở thư mục trong trình duyệt.

#### 11. Thiết lập

- Ngôn ngữ của giao diện và bản xuất, chủ đề của giao diện và bản xuất, thư mục bản xuất và ảnh chụp màn hình, và
  việc dọn dẹp chúng.

#### 12. Trợ giúp

- Một phần cho mỗi màn hình, phím tắt, dòng lệnh, và **Liên hệ và hỗ trợ**.

[↑ Mục lục](#mục-lục)

---

## Chi tiết các lớp bảo vệ

Mỗi lớp bảo vệ đáp ứng một mối đe dọa cụ thể; không lớp nào bị áp đặt.

| Bảo vệ | Chống lại gì | Ở đâu |
|---|---|---|
| Cổng gác (quy tắc) | Các đợt dồn dập từ một hoặc vài địa chỉ, kết nối không nhắm tới trang web | Tường lửa Funnel |
| Gom nhóm | Tấn công từ các địa chỉ phân tán (hàng nghìn địa chỉ, mỗi địa chỉ một kết nối) | Tường lửa Funnel |
| Danh sách đen | Địa chỉ và mạng đã biết là tấn công, được giữ lâu dài | Tấn công và quyết định |
| Giới hạn tài nguyên | `tailscaled` có thể chiếm toàn bộ máy khi bị tấn công | Sinh tồn |
| Cầu dao | Máy vẫn bị bão hòa dù vậy: ngắt Funnel một lúc | Sinh tồn |
| Giám sát tự động | Như trên, khi không có ai trước màn hình | Sinh tồn |
| Lá chắn WireGuard | Lũ gói UDP trên cổng của `tailscaled`, dù Funnel mở hay không | Sinh tồn |

### Cổng gác (Tường lửa Funnel)

Các quy tắc được áp dụng theo thứ tự này, tất cả đều trước khi mã hóa:

1. **Máy trong tailnet** (100.64.0.0/10, fd7a:115c:a1e0::/48): luôn được chấp nhận.
2. **Danh sách tin cậy**: không bao giờ bị giới hạn. **Danh sách đen**: bị từ chối cho đến khi được gỡ ra.
3. **Tốc độ theo địa chỉ** (mặc định 40 kết nối / 10 s): vượt quá mức này, địa chỉ bị chặn trong khoảng thời gian đã
   chọn (mặc định 60 phút).
4. **Tốc độ theo tiền tố** /24 với IPv4, /64 với IPv6.
5. **Ngân sách toàn cục** cho số kết nối được chấp nhận mỗi giây: bộ xử lý không bao giờ bị quá tải.
6. **Tên đích**: một kết nối không nhắm tới tên của máy sẽ bị từ chối.

Chứng chỉ `*.ts.net` của cổng gác được yêu cầu từ Tailscale, kiểm tra hằng ngày và gia hạn nóng 30 ngày trước khi
hết hạn. Chế độ **quan sát** đếm mọi thứ mà không từ chối gì.

### Gom nhóm (dấu vân tay, AS, quốc gia)

Trước một cuộc tấn công từ các địa chỉ phân tán, các quy tắc theo địa chỉ chỉ thấy mỗi địa chỉ một lần. Vì vậy cổng
gác còn phân loại mỗi máy khách theo **dấu vân tay JA4**, **AS** và **quốc gia** của nó, và đếm tốc độ của từng
nhóm.

- **Chế độ tấn công tự động**: vượt quá 80 kết nối đến mỗi giây (có thể chỉnh), cổng gác tự chuyển sang chế độ tấn
  công, và thoát ra sau 5 phút yên tĩnh.
- Chỉ trong chế độ tấn công: một dấu vân tay lạ tăng vọt, một AS của nhà cung cấp hosting hoặc đám mây (danh sách
  có thể sửa) hoặc một quốc gia trong danh sách của bạn (mặc định trống) vượt quá tốc độ của nó sẽ bị từ chối.
- Các **trình duyệt phổ biến** (Chrome, Edge, Firefox) không bao giờ bị các quy tắc này ảnh hưởng; các **máy khách
  đã biết** (được chấp nhận trong 24 giờ qua) được ưu tiên trước ngân sách toàn cục.
- **Học**: trong 7 ngày, cổng gác học các dấu vân tay quen thuộc của trang web bạn (không bao giờ trong lúc bị tấn
  công); cho đến lúc đó, gom nhóm vẫn ở chế độ quan sát.
- Ngoài lúc bị tấn công, cứ mười kết nối thì một kết nối được phân loại; khi bị tấn công, tất cả.
- Cơ sở dữ liệu AS / quốc gia là **DB-IP Lite**, được tải về và cập nhật mỗi tháng một lần.

### Sinh tồn

- **Giới hạn tài nguyên**: một tệp bổ sung riêng đặt trần cho `tailscaled` (ví dụ một lõi trọn vẹn trên một máy 4
  luồng) và hạ mức ưu tiên của nó. Cấu hình riêng của bạn không bao giờ bị sửa.
- **Cầu dao**: khi `tailscaled` liên tục vượt ngưỡng CPU (mặc định 80 % một lõi trong 60 s) hoặc nhiệt độ đạt
  85 °C, omega-tail đề xuất ngắt Funnel 10 phút (tự động bật lại, y như cũ, kể cả khi omega-tail đã đóng), ngắt
  hoàn toàn, hoặc chờ. Tailnet không bao giờ bị ngắt.
- **Giám sát tự động** (mặc định tắt): một dịch vụ chạy dưới tài khoản của bạn tự ngắt Funnel sau ba lần vượt
  ngưỡng, 15 phút lần đầu, 30 phút lần thứ hai, rồi một giờ, và tự bật lại.

### Lá chắn cổng WireGuard

`tailscaled` tiêu tốn khoảng một lõi bộ xử lý cho 100 000 gói mỗi giây nhận được trên cổng UDP của nó, kể cả gói
không hợp lệ. Lá chắn là một bảng nftables đặt trước nó, trên các card mạng:

- các **máy ngang hàng đã biết** (những máy mà `tailscaled` gửi dữ liệu tới) không bao giờ bị giới hạn;
- các lần bắt tay bị giới hạn ở 20 mỗi giây cho mỗi nguồn;
- các nguồn khác có một ngân sách (500 gói mỗi giây cho mỗi nguồn, tổng cộng 5 000);
- các gói không phải WireGuard bị từ chối.

Nó được đặt trước tiên ở chế độ **quan sát**, sau đó ở chế độ **hoạt động**. Nếu được omega-connect liên kết,
**omega-fire** (3.7.0 trở lên) có thể đặt và quản lý nó thay cho omega-tail: đó là cùng một bảng, đổi người quản lý
mà không bị động chạm tới.

[↑ Mục lục](#mục-lục)

---

## Kết quả đo

Các lựa chọn của omega-tail dựa trên kết quả đo, trên những máy cùng thế hệ với các máy mà nó bảo vệ (bộ xử lý từ
2010 đến 2016, phần lớn không có tăng tốc AES).

| Phép đo | Kết quả |
|---|---|
| Tỷ lệ của TLS trong chi phí một kết nối Funnel mặc định | khoảng 80 % |
| Chi phí của một kết nối **bị từ chối** bởi cổng gác, so với Funnel mặc định | **ít hơn 4,6 lần** |
| Chi phí của một kết nối **được chấp nhận** bởi cổng gác, so với Funnel mặc định | **ít hơn 2 lần** |
| Thông lượng với cổng gác, kết nối được giữ mở (so với một TLS viết bằng Go như của `tailscaled`) | **+15 %** yêu cầu, −20 % CPU |
| Lá chắn WireGuard: luồng gói từng chiếm trọn một lõi của `tailscaled` | **1 %** một lõi |
| Bộ nhớ của các dịch vụ (cổng gác, giám sát, lá chắn) | khoảng 67 MB |

Do đó cổng gác không làm giảm thông lượng của trang web: trên những máy này, chính việc mã hóa là giới hạn, có hay
không có omega-tail, và khi vận hành thật, Funnel dù sao cũng đi qua các máy chuyển tiếp của Tailscale và qua
modem/router.

[↑ Mục lục](#mục-lục)

---

## Kiến trúc

```text
src/omega_tail/
├── app/              Gốc kết hợp: ghép các lớp, điểm vào (giao diện, dòng lệnh)
├── core/             Hằng số dùng chung
├── domain/           Logic nghiệp vụ thuần: quy tắc cổng gác, cảnh báo, cầu dao, giám sát, danh sách đen…
├── application/      Ca sử dụng: công bố, tường lửa, sinh tồn, báo cáo, thiết lập
├── ports/            Hợp đồng (Protocol) mà tầng ứng dụng cần
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, nhật ký, xuất, script Lua
├── interfaces/       tui/ (Textual), cli/ (dòng lệnh), shared/ (trợ giúp, báo cáo, trình bày)
└── shared/           Ngôn ngữ (gettext)
```

### Nguyên tắc thiết kế

- `domain/` không đọc cũng không ghi gì: mọi thứ trong đó có thể kiểm thử mà không cần máy thật.
- `application/` điều phối các ca sử dụng thông qua miền nghiệp vụ và các port; giao diện và dòng lệnh gọi cùng các
  ca sử dụng.
- Chỉ `infrastructure.commands` và `infrastructure.privileged` chạy lệnh; giao diện không bao giờ chạy lệnh trực
  tiếp. Các quy tắc này được kiểm tra tự động (import-linter).
- Giao diện dựa trên [omega-lib](https://github.com/kraynux), thư viện dùng chung của toàn bộ bộ OMEGA (chủ đề,
  phát hiện terminal, ngôn ngữ, liên hệ và hỗ trợ, lá chắn WireGuard). Thư viện này không phát hành trên PyPI: nó
  được đóng gói sẵn trong tệp lưu trữ (`vendor/omega-lib/`).
- Mọi lời gọi chậm (Tailscale, HAProxy, ổ đĩa, mạng) đều chạy nền: giao diện không bao giờ bị đứng.

[↑ Mục lục](#mục-lục)

---

## Yêu cầu

### Hệ thống

- Linux, mọi bản phân phối (đã thử nghiệm trên Arch Linux và các bản dẫn xuất).
- Python 3.10 trở lên, với mô-đun `venv`.
- Một hệ thống init: **systemd**, **OpenRC** hoặc **runit**.
- `sudo` cho các thao tác làm thay đổi máy (được hỏi theo từng thao tác, không bao giờ lúc khởi chạy).
- Một terminal tối thiểu 80×24 (xem [Chủ đề và terminal](#chủ-đề-và-terminal)).

### Tailscale

- **Tailscale** đã được cài và kết nối (trình khách `tailscale` và dịch vụ `tailscaled`); đã thử nghiệm với phiên
  bản 1.104.
- Với Funnel: MagicDNS, chứng chỉ HTTPS và Funnel được cho phép trong bảng quản trị của Tailscale (xem
  [Những gì Tailscale phải cho phép](#những-gì-tailscale-phải-cho-phép-bảng-quản-trị)).

### Phụ thuộc Python

Được `install.sh` cài vào một môi trường ảo:

- `textual`: giao diện.
- `omega-lib`: thư viện dùng chung của bộ OMEGA, đóng gói sẵn trong tệp lưu trữ.

### Thành phần bắt buộc và tùy chọn

omega-tail phát hiện những gì có mặt và chỉ kích hoạt những gì dùng được.

| Thành phần | Vai trò | Trạng thái |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Mọi thứ omega-tail điều khiển | **Bắt buộc** |
| Python 3.10+, `textual`, `omega-lib` | Ứng dụng | **Bắt buộc** |
| systemd, OpenRC hoặc runit | Dịch vụ của cổng gác, giám sát, lá chắn | **Bắt buộc** (một trong ba) |
| HAProxy 3.x | Cổng gác của Tường lửa Funnel | Tùy chọn (có thể cài từ omega-tail) |
| HAProxy có Lua | Gom nhóm (dấu vân tay, AS, quốc gia) | Tùy chọn (trường hợp của các bản phân phối phổ biến) |
| nftables (kernel có `nft_limit`) | Lá chắn cổng WireGuard | Tùy chọn |
| Quyền đọc nhật ký hệ thống (nhóm `systemd-journal`, `adm` hoặc `wheel`) | Nhật ký, báo cáo tấn công | Khuyến nghị |
| Trình duyệt và môi trường desktop | « Xem bản xuất » trong trình duyệt (nếu không, đọc trong omega-tail) | Tùy chọn |
| omega-connect | Sổ đăng ký, đồng bộ, cập nhật cho bộ công cụ | Tùy chọn |
| omega-fire 3.7.0+ | Quản lý lá chắn WireGuard từ omega-fire | Tùy chọn |

[↑ Mục lục](#mục-lục)

---

## Cài đặt

Tệp lưu trữ chính thức được cung cấp ở định dạng `.tar.gz`. Hãy kiểm tra tính toàn vẹn trước khi cài đặt, với tệp
`sha.txt` được phát hành bên cạnh:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Ba phương pháp này dành cho lần cài đặt đầu tiên.** Nếu `~/omega-tail` đã tồn tại, hãy dùng phần
> [Cập nhật](#cập-nhật). Đừng bao giờ chạy lại các lệnh này từ bên trong một thư mục `omega-tail` đã có: `tar` sẽ
> tạo ra một `omega-tail/omega-tail/` lồng nhau.

Không bước cài đặt nào cần quyền root: omega-tail chạy dưới tài khoản người dùng thông thường.

### Phương pháp 1 — script cài đặt

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Có vẻ bạn đã ở trong một thư mục omega-tail — xem phần Cập nhật trong README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Đã giải nén ở đây, bỏ qua bước này." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail đã tồn tại, bỏ qua việc di chuyển." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

Script tạo môi trường ảo, cài các phụ thuộc (omega-lib đóng gói sẵn trước tiên), cấp quyền thực thi cho các trình
khởi chạy, ghi mã thông báo cài đặt mà omega-connect đọc và đề xuất alias `omega-tail`. Có thể chạy lại mà không có
rủi ro.

### Phương pháp 2 — cài đặt đầy đủ bền vững

Lệnh này có thể chạy lại: nó bỏ qua các bước đã thực hiện.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Có vẻ bạn đã ở trong một thư mục omega-tail — xem phần Cập nhật trong README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail đã tồn tại, bỏ qua việc giải nén." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv đã tồn tại, bỏ qua bước này." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Đã cài Omega-Tail. Chạy ./omega-tail.sh."
```

### Phương pháp 3 — cài đặt chi tiết

```bash
# 0. Kiểm tra rằng không chạy lại từ bên trong một omega-tail đã có
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Có vẻ bạn đã ở trong một thư mục omega-tail — xem phần Cập nhật trong README." >&2; exit 1; }

# 1. Giải nén
[ -d omega-tail ] && echo "ℹ️ Đã giải nén ở đây, bỏ qua bước này." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Di chuyển vào thư mục home
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail đã tồn tại, bỏ qua việc di chuyển." || mv omega-tail ~/

# 3. Vào thư mục dự án
cd ~/omega-tail/

# 4. Tạo môi trường ảo
[ -f .venv/bin/activate ] && echo "ℹ️ .venv đã tồn tại, bỏ qua việc tạo." || python3 -m venv .venv

# 5. Cài các phụ thuộc (omega-lib đóng gói sẵn trước tiên)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Cấp quyền thực thi cho các trình khởi chạy
chmod +x omega-tail.sh install.sh

# 7. Ghi mã thông báo cài đặt (omega-connect đọc; tùy chọn)
./omega-tail.sh synchro jeton

# 8. Khởi chạy
./omega-tail.sh
```

Trên Debian, Ubuntu và các bản dẫn xuất, mô-đun `venv` không phải lúc nào cũng được cài cùng Python:
`sudo apt install python3-venv`.

### Cập nhật

Các dịch vụ của omega-tail (cổng gác, giám sát) dùng các tệp trong `~/omega-tail/var/`. Vì vậy một lần cập nhật phải
**giữ nguyên thư mục này tại chỗ**: tệp lưu trữ không chứa `var/`, và được giải nén đè lên bản cài hiện có.

Từ thư mục chứa tệp lưu trữ, **không phải `~/omega-tail`**:

```bash
# 1. Sao lưu bản cài hiện tại (kể cả var/)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Giải nén phiên bản mới đè lên (var/ được giữ lại)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Cài lại (phụ thuộc, trình khởi chạy, mã thông báo cài đặt)
cd ~/omega-tail
./install.sh

# 4. Khởi chạy lại omega-tail
./omega-tail.sh
```

Nếu cổng gác đang hoạt động, **Tường lửa Funnel → « Áp dụng quy tắc »** tạo lại cấu hình của nó với phiên bản mới,
áp dụng nóng. Nếu giám sát tự động đang bật, **Sinh tồn → « Bật giám sát »** khởi chạy lại nó với mã mới.
omega-connect cũng có thể thực hiện cập nhật (màn hình Updater).

### Alias Bash hoặc Zsh

`install.sh` đề xuất alias. Để tự thêm:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

Alias có tên `omega-tail`, không phải `tail`, để không che mất lệnh hệ thống `tail`.

[↑ Mục lục](#mục-lục)

---

## Sử dụng

### Khởi chạy

```bash
cd ~/omega-tail
./omega-tail.sh

# hoặc đơn giản, nếu đã tạo alias:
omega-tail
```

Trình khởi chạy không yêu cầu nâng quyền: omega-tail chạy dưới tài khoản của bạn, và sudo chỉ được yêu cầu bởi các
thao tác cần đến nó, trong terminal, với lệnh được hiển thị trước.

### Những bước đầu tiên được khuyến nghị

Để bảo vệ một trang web được công bố qua Funnel, theo thứ tự sau:

1. **Bảng điều khiển**: đọc các cảnh báo; **Trở thành người vận hành** (một lần, qua sudo) để điều chỉnh Tailscale mà không cần sudo.
2. **Sinh tồn → Áp dụng giới hạn tài nguyên**: `tailscaled` sẽ không thể chiếm toàn bộ máy nữa.
3. **Công bố**: công bố trang web qua **HTTPS trên cổng 443**, đường dẫn `/`, rồi chạy **thử đầu cuối**.
4. **Tường lửa Funnel → Cài HAProxy**, rồi **Bật bảo vệ**, trước tiên ở chế độ **quan sát**.
5. Vài ngày sau, **Tấn công và quyết định**: nếu các bộ đếm chỉ cho thấy hành vi lạm dụng, chuyển cổng gác sang
   chế độ **bình thường**.
6. Để **gom nhóm** học trong 7 ngày ở chế độ quan sát, rồi chuyển sang **áp dụng**.
7. **Sinh tồn → Lá chắn cổng WireGuard**: đặt ở chế độ quan sát, rồi chuyển sang hoạt động.
8. Với một máy không có ai trước màn hình: **Sinh tồn → Bật giám sát**.

### Ngôn ngữ giao diện

17 ngôn ngữ: tiếng Pháp, tiếng Anh, tiếng Tây Ban Nha, tiếng Bồ Đào Nha (Brazil), tiếng Ý, tiếng Đức, tiếng Hà Lan,
tiếng Ba Lan, tiếng Nga, tiếng Trung, tiếng Việt, tiếng Thái, tiếng Indonesia, tiếng Nhật, tiếng Hàn, tiếng Hindi,
tiếng Ả Rập.

- Chọn trong thiết lập (phím `s`, « Langue / Language », nhãn không bao giờ được dịch), áp dụng bằng cách chỉ khởi
  động lại giao diện.
- Dùng một lần: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- Trong console văn bản Linux (TTY), các ngôn ngữ có chữ viết không có trong phông chữ của console được hiển thị
  bằng tiếng Anh trong phiên đó; tiếng Ả Rập hiển thị từ phải sang trái.
- **Ngôn ngữ bản xuất** (báo cáo, danh sách đen, nhật ký) được đặt riêng, mặc định « Giống giao diện ».

### Liên hệ và hỗ trợ

Phần trợ giúp (phím `a`) có màn hình **Liên hệ và hỗ trợ**:

- *Mời một ly cà phê* (trang PayPal của nhà phát triển);
- *Liên hệ hỗ trợ* (địa chỉ email và biểu mẫu của trang web, hiển thị rõ ràng);
- *Khai báo là người dùng (ẩn danh)*;
- *Kiểm tra cập nhật*.

Việc khai báo là tự nguyện, tắt theo mặc định và chỉ gửi một lần. Nó chỉ dùng để đếm số người dùng và, nếu bạn muốn,
châu lục hoặc quốc gia của họ (danh sách đóng, không bao giờ là văn bản tự do). Nó gửi một khóa được tạo ngẫu nhiên,
tên phần mềm (`omega-tail`) và phiên bản của nó; không bao giờ gửi tên, tên máy, thiết lập hay địa chỉ của tailnet.
Có thể rút lại bất cứ lúc nào từ cùng màn hình (*Không khai báo tôi nữa*). Việc kiểm tra cập nhật chỉ đọc danh sách
các phiên bản đã phát hành trên trang web, và không bao giờ khi chưa nhấp.

### Liên kết với các công cụ omega khác

- **omega-connect**: `install.sh` ghi một mã thông báo cài đặt (`var/omega-jeton.json`) mô tả công cụ và phiên bản
  của nó, mà không thực thi gì. omega-connect dùng nó cho Sổ đăng ký, đồng bộ, sửa chữa, cập nhật và cài đặt.
  `./omega-tail.sh synchro jeton` ghi lại nó bằng tay.
- **omega-fire** (3.7.0 trở lên), được omega-connect liên kết, có thể đặt và quản lý lá chắn cổng WireGuard; danh
  sách quy tắc của nó hiển thị lá chắn với nguồn gốc omega-tail.

### Dòng lệnh

Mọi lệnh được viết dạng `./omega-tail.sh …` (hoặc `omega-tail …` với alias):

| Lệnh | Vai trò |
|---|---|
| `omega-tail` | Giao diện |
| `omega-tail etat [--format json]` | Trạng thái của Tailscale, của máy và các cảnh báo, dạng văn bản hoặc cho một script |
| `omega-tail aide` | Trợ giúp đầy đủ dạng văn bản |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | Báo cáo, hiển thị hoặc lưu lại |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Ngắt hoặc bật lại Funnel |
| `omega-tail veille etat` | Trạng thái giám sát tự động và các dòng gần nhất của nó |
| `omega-tail porte etat` | Trạng thái cổng gác và bộ đếm |
| `omega-tail porte certificat [--si-besoin]` | Gia hạn chứng chỉ `*.ts.net` của cổng gác |
| `omega-tail porte groupes` | Gom nhóm: chế độ tấn công, dấu vân tay, AS, quốc gia |
| `omega-tail porte base` | Cập nhật cơ sở dữ liệu AS / quốc gia |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Chặn một địa chỉ hoặc một mạng (đưa vào danh sách đen với `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Bỏ chặn |
| `omega-tail porte confiance ADRESSE` | Đưa vào danh sách tin cậy |
| `omega-tail synchro jeton` | Ghi mã thông báo cài đặt (omega-connect) |
| `omega-tail --version` | Phiên bản |

### Luồng chung

1. Màn hình khởi động, sau đó là menu chính hai cột (TAILSCALE và BẢO VỆ).
2. Dưới tiêu đề của mỗi màn hình, **thanh trạng thái** tóm tắt mọi thứ: dịch vụ, CPU của máy và của `tailscaled`,
   nhiệt độ, bộ nhớ, Funnel, tường lửa, giám sát, kết nối. Nó được đọc lại mỗi 5 giây.
3. Mỗi thao tác làm thay đổi máy hiển thị lệnh của nó, rồi yêu cầu xác nhận; sudo được nhập trong terminal và giao
   diện quay lại sau đó.
4. Các thao tác nhạy cảm (đăng xuất vĩnh viễn, dọn sạch toàn bộ danh sách đen) yêu cầu gõ một từ.
5. Kết quả hiển thị trong một dòng, được kiểm tra trên trạng thái đọc lại.

### Điều hướng

- Mũi tên lên / xuống: chuyển từ phần tử này sang phần tử khác (các dòng của bảng, các nút).
- Tab / Shift+Tab: chuyển từ vùng này sang vùng khác của màn hình.
- Enter hoặc nhấp chuột: kích hoạt nút đã chọn; trong bảng cảnh báo, « Sửa ».
- `Esc`: quay lại màn hình trước (ở menu: thoát).
- `a`: trợ giúp, từ bất kỳ màn hình nào.
- `s`: thiết lập, từ bất kỳ màn hình nào.
- `t`: chủ đề tiếp theo (được lưu lại).
- `r`: vẽ lại màn hình, hiển thị kích thước terminal và đọc lại trạng thái.
- `q`: thoát, có xác nhận.
- `Ctrl+P`: các lệnh (chủ đề, chụp màn hình SVG vào thư mục ảnh chụp, thoát).

[↑ Mục lục](#mục-lục)

---

## Chủ đề và terminal

Mười chủ đề `omega-*` được dùng chung với phần còn lại của bộ OMEGA:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Chuyển đổi giữa các chủ đề bằng `t`, hoặc chọn một chủ đề trong thiết lập (`s`); lựa chọn được ghi nhớ.
- Các bản xuất HTML có chủ đề riêng: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail điều chỉnh độ phức tạp hình ảnh theo terminal được phát hiện thông qua một **hồ sơ hiển thị**: Đầy đủ,
  Tiêu chuẩn, Rút gọn hoặc Mono (chỉ ASCII).

| Kích thước tối thiểu | Hồ sơ | Terminal tiêu biểu |
|---|---|---|
| 120×32 trở lên | Đầy đủ | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 trở lên | Tiêu chuẩn | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 trở lên | Rút gọn | urxvt, xterm, SSH hiện đại |
| dưới 80×24 | Mono (chỉ ASCII) | Linux TTY, SSH cũ |

Sau khi thay đổi kích thước, `r` đọc lại kích thước terminal; kích thước được hiển thị ở phía trên, bên cạnh chủ đề.

[↑ Mục lục](#mục-lục)

---

## Tệp, dịch vụ và khả năng tương thích

### Trong thư mục của omega-tail

Toàn bộ trạng thái của omega-tail nằm trong `~/omega-tail/var/`, được tạo lại khi khởi động và không bao giờ được
phát hành:

```text
var/
├── settings.json         thiết lập (ngôn ngữ, chủ đề, thư mục, ngưỡng, quy tắc của cổng gác)
├── omega-jeton.json      mã thông báo cài đặt (omega-connect)
├── porte/                cấu hình cổng gác, chứng chỉ, danh sách tin cậy và danh sách đen, cơ sở dữ liệu AS / quốc gia
├── veille/               nhật ký của giám sát tự động
├── survie/               bản gốc của các tệp đã sửa, trạng thái cầu dao
├── funnel/sauvegardes/   cấu hình công bố trước mỗi thay đổi (50 bản gần nhất)
├── exports/              báo cáo, nhật ký và danh sách đã xuất
└── screenshots/          ảnh chụp màn hình (Ctrl+P)
```

### Trên hệ thống (chỉ khi bạn bật lớp bảo vệ tương ứng)

Mỗi tệp được đặt qua sudo, với lệnh được hiển thị, và được gỡ bởi thao tác ngược lại trong omega-tail.

| Tệp hoặc dịch vụ | Được đặt bởi | Được gỡ bởi |
|---|---|---|
| Dịch vụ `omega-tail-porte` (systemd, OpenRC hoặc runit) và `omega-tail-porte-certificat` (timer systemd, hoặc một dòng có đánh dấu trong crontab của bạn) | Bật bảo vệ | Tắt bảo vệ |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (hoặc một nhóm kiểm soát khi không dùng systemd) | Áp dụng giới hạn tài nguyên | Gỡ giới hạn tài nguyên |
| Các timer `omega-tail-retablir-*` (bật lại sau khi ngắt) | Cầu dao | Kết thúc lần ngắt |
| Dịch vụ `omega-tail-veille` | Bật giám sát | Tắt giám sát |
| Dịch vụ `omega-bouclier-wg`, bảng nftables, `/etc/omega-bouclier-wg/` | Lá chắn: Đặt | Lá chắn: Gỡ |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | Bật chuyển tiếp IP | Xóa tệp |

Tệp `override.conf` của `tailscaled`, nếu có, không bao giờ bị sửa.

### Hệ thống init

| | systemd | OpenRC | runit |
|---|---|---|---|
| Dịch vụ `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Nhật ký | `journalctl` | tệp của dịch vụ | `svlogd`, `socklog` |
| Giới hạn tài nguyên | tệp bổ sung systemd | nhóm kiểm soát (cgroup v2) | nhóm kiểm soát (cgroup v2) |
| Ngắt tạm thời | timer systemd | tiến trình tách rời dưới tài khoản của bạn | tiến trình tách rời dưới tài khoản của bạn |
| Cổng gác, giám sát, lá chắn | dịch vụ systemd | dịch vụ OpenRC | dịch vụ runit |

Khi không dùng systemd, giới hạn tài nguyên bằng nhóm kiểm soát sẽ mất nếu `tailscaled` khởi động lại: khi đó một
cảnh báo đề xuất đặt lại nó.

### IPv4 và IPv6

Cổng gác, các danh sách, gom nhóm và lá chắn xử lý cả hai họ địa chỉ. Các tiền tố được đếm là /24 với IPv4 và /64 với
IPv6; một địa chỉ IPv4 xuất hiện dưới dạng `::ffff:a.b.c.d` được xử lý như địa chỉ IPv4.

[↑ Mục lục](#mục-lục)

---

## Bảo mật

omega-tail tác động lên một dịch vụ lộ ra Internet; nó được thiết kế để không bao giờ làm tình hình tệ hơn.

- **Không bao giờ root**: ứng dụng, cổng gác HAProxy và giám sát chạy dưới tài khoản của bạn; sudo chỉ được yêu cầu
  để đặt hoặc gỡ một dịch vụ, với lệnh được hiển thị trước.
- **Kênh riêng tư**: các socket quản trị của cổng gác ở chế độ 600 trong một thư mục 700; việc đồng bộ các bảng của
  nó đi qua một socket trong cùng thư mục.
- **Quay lui**: mỗi lần chuyển đổi Funnel đều được sao lưu, kiểm tra, và trạng thái trước đó được đặt lại nếu thất
  bại.
- **Quan sát trước**: cổng gác, gom nhóm và lá chắn được đặt ở chế độ quan sát; không có gì bị từ chối trước khi
  bạn quyết định.
- **Tailnet không bao giờ bị ngắt**: cổng gác luôn chấp nhận các máy của bạn, và cầu dao chỉ ngắt Funnel.
- **Dữ liệu đầu vào được kiểm tra**: chỉ địa chỉ hoặc mạng ở dạng chuẩn tắc mới tới được HAProxy; các tên do máy
  trong tailnet khai báo được làm sạch trước khi hiển thị.
- **Kiểm định**: mã nguồn đã được kiểm định (claude-security, 2026-11-25); 7 điểm được nêu ra, không điểm nào có
  thể bị khách truy cập khai thác từ xa, đã được sửa ngay trong ngày.
- Hãy thử trước trên một máy thử nghiệm hoặc ở chế độ quan sát, và dùng các mạng tài liệu RFC 5737 cho các phép
  thử IPv4: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Mục lục](#mục-lục)

---

## Kiểm thử và chất lượng

Bộ kiểm thử gồm **179 bài kiểm thử**: miền nghiệp vụ, ca sử dụng, hạ tầng (với một Funnel mô phỏng), các màn hình
Textual với các bảng định kiểu thật, hệ thống init, bảo mật. Mã nguồn được kiểm tra bằng `ruff`, `mypy` và
`import-linter` (quy tắc các lớp). Thư mục `tests/` có trong tệp lưu trữ.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

Phần lớn bài kiểm thử không cần Tailscale, HAProxy hay quyền root.

[↑ Mục lục](#mục-lục)

---

## Tình trạng dự án

### Điểm đã vận hành

- Điều khiển Tailscale đầy đủ: dịch vụ, kết nối, thiết lập, công bố, mạng, nhật ký.
- Cổng gác HAProxy trước TLS, vận hành thật từ 2026-11-23, với quy tắc, danh sách, gom nhóm và chế độ tấn công.
- Sinh tồn: giới hạn tài nguyên, cầu dao, giám sát tự động.
- Lá chắn cổng WireGuard, vận hành thật từ 2026-11-24.
- Báo cáo và xuất TXT, HTML, JSON.
- Tương thích với omega-connect và omega-fire.

### Hạn chế đã biết

- Các dịch vụ dưới OpenRC và runit được bộ kiểm thử bao phủ, nhưng chưa được xác nhận trên máy thật.
- Cổng gác bảo vệ một Funnel được công bố qua HTTPS trên một cổng duy nhất, với đường dẫn `/`.
- Gom nhóm cần một HAProxy được biên dịch có Lua; không có Lua, cổng gác vẫn hoạt động nhưng không có gom nhóm.
- Không thể đặt lá chắn trên một kernel đã cập nhật mà chưa khởi động lại (thiếu mô-đun): màn hình sẽ báo điều này.
- Một cuộc tấn công làm bão hòa chính đường truyền Internet vẫn nằm ngoài tầm của một công cụ cài trên máy.
- Thông lượng của một trang web được công bố qua Funnel vẫn bị giới hạn bởi các máy chuyển tiếp của Tailscale và bởi
  modem/router.

[↑ Mục lục](#mục-lục)

---

## Gỡ cài đặt

Trước tiên, từ omega-tail, hãy gỡ những gì đã được đặt lên hệ thống, theo thứ tự sau:

1. **Tường lửa Funnel → Tắt bảo vệ** (Funnel được đặt lại như trước).
2. **Sinh tồn → Tắt giám sát**.
3. **Sinh tồn → Lá chắn cổng WireGuard → Gỡ**.
4. **Sinh tồn → Gỡ giới hạn tài nguyên**.

Sau đó xóa thư mục:

```bash
rm -rf ~/omega-tail
```

Tự xóa các bản xuất được đặt ở nơi khác, alias `omega-tail` trong `~/.bashrc` hoặc `~/.zshrc`, và, nếu bạn đã bật
nó, tệp `/etc/sysctl.d/99-omega-tail-forwarding.conf`. Quyền người vận hành của Tailscale được gỡ bằng
`sudo tailscale set --operator=`.

[↑ Mục lục](#mục-lục)

---

## Giấy phép

Omega-Tail được phân phối theo giấy phép **MIT**. Xem tệp [`LICENSE`](../../../LICENSE) để biết toàn văn.

Cơ sở dữ liệu AS / quốc gia sử dụng IP Geolocation by [DB-IP](https://db-ip.com), theo giấy phép
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Mục lục](#mục-lục)

---

> **Omega-Tail — Điều khiển Tailscale, bảo vệ Funnel.**
>
> Một giao diện TUI cho Tailscale, và một cổng gác từ chối hành vi lạm dụng trước mọi bước mã hóa.
