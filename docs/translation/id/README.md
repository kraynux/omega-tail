<!-- Copyright (c) 2026 kraynux - kraynux@proton.me - Licence MIT (voir fichier LICENSE) -->

<div align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/assets/omega-tail.png" alt="Omega-Tail" width="512">
</div>

# 🔒 OMEGA-TAIL

**Pengelola kendali TAILSCALE dengan firewall terpadu untuk FUNNEL**

OMEGA-TAIL adalah alat dalam suite OMEGA yang mengendalikan **Tailscale** di sebuah mesin dan **melindunginya** ketika
mesin itu memublikasikan layanan ke Internet melalui **Tailscale Funnel**.

> Dikembangkan oleh [kraynux](https://github.com/kraynux) untuk [Omega-Server](https://kraynux.snake-mackarel.ts.net) · [Halaman resmi](https://kraynux.snake-mackarel.ts.net/omega-tail/translation/id/) · [Tangkapan layar](https://kraynux.snake-mackarel.ts.net/omega-tail/screenshots/)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-5-E34F26.svg)](https://developer.mozilla.org/docs/Web/HTML)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2020%2B-F7DF1E.svg)](https://developer.mozilla.org/docs/Web/JavaScript)
![Interface](https://img.shields.io/badge/Interface-CLI%20%2B%20TUI-cyan.svg)
[![Textual](https://img.shields.io/badge/Textual-TUI-5A5AFB.svg)](https://textual.textualize.io/)
[![Platform](https://img.shields.io/badge/Platform-Linux-informational.svg)](https://www.linux.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../../../LICENSE)

🌐 Antarmuka, dokumentasi, ekspor, dan halaman pengunjung tersedia dalam **17 bahasa** — lihat [Bahasa antarmuka](#bahasa-antarmuka).  
**Bahasa:**
<img src="https://flagcdn.com/w20/fr.png" alt="France" style="height:14px;"> [Français](../../../README.md) · <img src="https://flagcdn.com/w20/gb.png" alt="English" style="height:14px;"> [English](../en/README.md) · <img src="https://flagcdn.com/w20/es.png" alt="Español" style="height:14px;"> [Español](../es/README.md) · <img src="https://flagcdn.com/w20/br.png" alt="Português (Brasil)" style="height:14px;"> [Português (Brasil)](../pt-BR/README.md) · <img src="https://flagcdn.com/w20/it.png" alt="Italiano" style="height:14px;"> [Italiano](../it/README.md) · <img src="https://flagcdn.com/w20/de.png" alt="Deutsch" style="height:14px;"> [Deutsch](../de/README.md) · <img src="https://flagcdn.com/w20/nl.png" alt="Nederlands" style="height:14px;"> [Nederlands](../nl/README.md) · <img src="https://flagcdn.com/w20/pl.png" alt="Polski" style="height:14px;"> [Polski](../pl/README.md) · <img src="https://flagcdn.com/w20/ru.png" alt="Русский" style="height:14px;"> [Русский](../ru/README.md) · <img src="https://flagcdn.com/w20/cn.png" alt="中文" style="height:14px;"> [中文](../zh-CN/README.md) · <img src="https://flagcdn.com/w20/vn.png" alt="Tiếng Việt" style="height:14px;"> [Tiếng Việt](../vi/README.md) · <img src="https://flagcdn.com/w20/th.png" alt="ไทย" style="height:14px;"> [ไทย](../th/README.md) · <img src="https://flagcdn.com/w20/id.png" alt="Bahasa Indonesia" style="height:14px;"> [Bahasa Indonesia](README.md) · <img src="https://flagcdn.com/w20/jp.png" alt="日本語" style="height:14px;"> [日本語](../ja/README.md) · <img src="https://flagcdn.com/w20/kr.png" alt="한국어" style="height:14px;"> [한국어](../ko/README.md) · <img src="https://flagcdn.com/w20/in.png" alt="हिन्दी" style="height:14px;"> [हिन्दी](../hi/README.md) · <img src="https://flagcdn.com/w20/ae.png" alt="العربية" style="height:14px;"> [العربية](../ar/README.md)

---

**OMEGA-TAIL** adalah aplikasi TUI (Terminal User Interface) berbasis Python yang dibangun dengan
[Textual](https://textual.textualize.io/). Aplikasi ini memungkinkan Anda mengelola dan mengatur **Tailscale** dalam
mode lanjutan dari sebuah antarmuka, tanpa perlu menghafal satu perintah pun. Aplikasi ini juga menambahkan
perlindungan (firewall, pembatasan, ketahanan…) untuk mode **Funnel**, yang membuka layanan mesin ke seluruh Internet.

Setiap tindakan yang mengubah mesin terlebih dahulu menampilkan perintahnya. Kata sandi sudo diketik di terminal,
tindakan demi tindakan, dan tidak ada yang dijalankan di latar belakang tanpa sepengetahuan Anda.

<p align="center">
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-tail/A.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-tail/B.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-tail/C.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-tail/D.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-tail/E.png" width="32%" />
  <img src="https://raw.githubusercontent.com/kraynux/kraynux/refs/heads/main/docs/translation/id/omega-tail/F.png" width="32%" />
</p>

Proyek ini dirancang mengikuti prinsip **Clean Architecture**, dengan `app/` sebagai akar komposisi: domain bisnis,
orkestrasi, infrastruktur, dan antarmuka dipisahkan.

## Daftar isi

- [Pengenalan](#pengenalan)
- [Memahami Tailscale dan Funnel](#memahami-tailscale-dan-funnel)
- [Fitur](#fitur)
- [Rincian perlindungan](#rincian-perlindungan)
- [Pengukuran](#pengukuran)
- [Arsitektur](#arsitektur)
- [Prasyarat](#prasyarat)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Tema dan terminal](#tema-dan-terminal)
- [Berkas, layanan, dan kompatibilitas](#berkas-layanan-dan-kompatibilitas)
- [Keamanan](#keamanan)
- [Pengujian dan kualitas](#pengujian-dan-kualitas)
- [Status proyek](#status-proyek)
- [Pencopotan](#pencopotan)
- [Lisensi](#lisensi)

---

## Pengenalan

### Mengapa omega-tail

Tailscale Funnel memublikasikan layanan mesin ke Internet tanpa membuka port di router: para pengunjung melewati
relai Tailscale. Cara ini sederhana dan aman dari sisi jaringan, tetapi masih ada satu kelemahan.

- **Biaya enkripsi.** Dalam mode Funnel bawaan, layanan `tailscaled` di mesin itulah yang melakukan jabat tangan
  TLS untuk setiap pengunjung. Diukur pada mesin kecil, ini sekitar **80 % dari biaya sebuah koneksi**. Beberapa
  ratus koneksi baru per detik sudah cukup untuk membuat prosesor jenuh: satu komputer biasa, dengan skrip sederhana,
  dapat menjatuhkan situs dan mesinnya.
- **Pengunjung yang tak terlihat.** Firewall yang biasa (nftables, ufw, fail2ban) tidak melihat pengunjung ini:
  mereka tiba dalam keadaan terenkripsi, melalui terowongan Tailscale, dengan alamat sebuah relai.
- **Pengaturan yang tersebar.** Pengaturan Tailscale (operator, simpul keluar, rute, SSH, perisai…) sangat banyak,
  terbagi antara perintah dan konsol web, dan sebagian dapat memutus sesi yang sedang berjalan.

### Tujuan

- Mengendalikan Tailscale sepenuhnya dari sebuah antarmuka, dengan satu kalimat penjelasan untuk setiap pengaturan.
- Menolak koneksi yang menyalahgunakan **sebelum** enkripsi apa pun, dengan melihat alamat asli setiap pengunjung.
- Menjaga mesin tetap berdiri saat diserang: administrasi dan layanan lain tetap dapat dijangkau.
- Tidak pernah memaksakan apa pun: mengusulkan, menampilkan perintah, bertanya, dan dapat dibatalkan.
- Berjalan di distribusi Linux apa pun, di bawah systemd, OpenRC, atau runit.

### Yang dilakukan omega-tail

- Menampilkan status Tailscale, mesin, dan apa yang dipublikasikan, dengan peringatan yang mengarah ke layar untuk
  memperbaikinya.
- Memulai, menghentikan, dan memulai ulang `tailscaled`, dengan pengaman jika sesi Anda melewati Tailscale.
- Mengelola koneksi, akun, dan semua pengaturan `tailscale set`, yang diperiksa sebelum diterapkan.
- Memublikasikan, mencabut, menangguhkan, dan menguji layanan Serve dan Funnel, dengan cadangan dan pemulihan.
- Menampilkan perangkat di tailnet, jalurnya (langsung atau melalui relai), diagnostik jaringan, dan log.
- Menempatkan sebuah **gerbang** HAProxy antara Funnel dan situs Anda: aturan per alamat, per prefiks, anggaran global,
  daftar tepercaya dan daftar hitam, pengelompokan menurut sidik jari JA4, jaringan asal (AS) dan negara, mode
  serangan otomatis.
- Membatasi `tailscaled`, memutus Funnel sementara atau sepenuhnya, dan dapat melakukannya sendiri berkat
  pengawasan otomatis.
- Melindungi port WireGuard milik `tailscaled` dengan sebuah tabel nftables (perisai).
- Membuat laporan tentang mesin dan serangan selama 7 hari terakhir, dalam TXT, HTML, atau JSON.

### Yang tidak dilakukan proyek ini

- Tidak menggantikan Tailscale: hanya mengendalikannya.
- Tidak melindungi dari serangan volumetrik yang membuat jalur Internet itu sendiri jenuh (router, tautan).
- Tidak mengelola konsol administrasi web Tailscale (kebijakan akses, persetujuan simpul keluar, aktivasi Funnel untuk
  tailnet).
- Tidak melindungi layanan yang dipublikasikan selain melalui Funnel: untuk port-port tersebut, ada omega-fire.
- Tidak pernah berjalan sebagai root dan tidak menjalankan apa pun di latar belakang tanpa persetujuan Anda.
- Tidak berjalan di Windows maupun macOS.

[↑ Daftar isi](#daftar-isi)

---

## Memahami Tailscale dan Funnel

omega-tail mengandaikan beberapa pengertian dasar tentang Tailscale. Bagian ini mengumpulkannya, tanpa mengandaikan
hal lain.

### Kosakata

| Istilah | Artinya |
|---|---|
| **Tailnet** | Jaringan pribadi Tailscale Anda: semua mesin yang terhubung ke akun yang sama (atau organisasi yang sama). Setiap mesin di dalamnya menerima alamat `100.x.y.z` (rentang 100.64.0.0/10) dan alamat IPv6 dalam `fd7a:115c:a1e0::/48`. |
| **`tailscaled`** | Layanan (daemon) yang berjalan di mesin: ia menjaga terowongan terenkripsi WireGuard, tumpukan jaringan Tailscale, dan, untuk Serve dan Funnel, relai ke layanan Anda. |
| **`tailscale`** | Perintah yang mengendalikan `tailscaled` (`tailscale status`, `tailscale set`, `tailscale funnel`…). omega-tail menggunakannya untuk Anda. |
| **WireGuard** | Protokol terowongan terenkripsi yang digunakan antarmesin. Untuk itu `tailscaled` mendengarkan pada sebuah port UDP (41641 secara bawaan), yang sering dibuka oleh router (UPnP). |
| **Relai DERP** | Server Tailscale yang meneruskan lalu lintas ketika dua mesin tidak dapat saling menjangkau secara langsung (NAT yang sulit). Jalur « langsung » lebih cepat. |
| **MagicDNS** | Nama mesin di tailnet, dalam bentuk `machine.nom-du-tailnet.ts.net`. |
| **Serve** | Memublikasikan layanan lokal (situs, API…) **hanya untuk tailnet**, dalam HTTPS dengan sertifikat `*.ts.net` yang valid. |
| **Funnel** | Memublikasikan layanan lokal **untuk seluruh Internet**, di alamat `https://machine.nom-du-tailnet.ts.net`. Hanya port 443, 8443, dan 10000 yang dapat dibuka. |
| **Relai Funnel** | Server Tailscale yang menerima pengunjung dari Internet dan memasukkan mereka ke tailnet Anda (tampil sebagai « funnel-ingress-node »). |
| **Operator** | Akun Linux yang diizinkan mengatur Tailscale tanpa sudo (`tailscale set --operator=…`). omega-tail menawarkannya satu kali, melalui sudo. |
| **Simpul keluar (exit node)** | Mesin di tailnet yang dipakai mesin lain untuk melewatkan seluruh lalu lintas Internetnya (seperti VPN). Mesin ini harus disetujui di konsol Tailscale. |
| **Subnet yang diumumkan (subnet router)** | Jaringan lokal (misalnya `192.168.1.0/24`) yang dibuat dapat dijangkau oleh sebuah mesin bagi seluruh tailnet. |
| **Perisai (shields up)** | Pengaturan Tailscale yang menolak semua koneksi masuk yang berasal dari tailnet. |
| **SSH Tailscale** | Server SSH yang disediakan Tailscale, diizinkan oleh kebijakan tailnet. |
| **Header PROXY v2** | Header singkat yang ditambahkan di awal koneksi untuk meneruskan alamat asli pengunjung kepada penerimanya. |
| **Sidik jari JA4** | Tanda tangan dari cara sebuah perangkat lunak membuka koneksi TLS: peramban dan alat serangan tidak memiliki tanda tangan yang sama. |
| **AS (sistem otonom)** | Jaringan asal sebuah alamat: penyedia akses, penyedia hosting, cloud. |

### Jalur seorang pengunjung

**Funnel bawaan, tanpa omega-tail.** `tailscaled` melakukan semuanya: ia mendekripsi terowongan WireGuard,
melakukan jabat tangan TLS dengan pengunjung, lalu meneruskan permintaan dalam HTTP ke situs Anda. Tidak ada firewall
di mesin yang melihat pengunjung, dan setiap koneksi baru mahal bagi `tailscaled`.

```text
Pengunjung ──HTTPS──▶ Relai Funnel ──WireGuard──▶ tailscaled (TLS + relai HTTP) ──HTTP──▶ situs Anda
                      (Tailscale)                 └── seluruh biaya ada di sini
```

**Funnel dengan gerbang omega-tail.** Funnel beralih ke mode TCP: `tailscaled` tidak lagi menangani TLS, ia
meneruskan aliran yang masih terenkripsi ke gerbang, diawali dengan alamat asli pengunjung (header PROXY v2). Gerbang
memutuskan **sebelum** enkripsi apa pun: koneksi yang ditolak nyaris tanpa biaya, dan hanya koneksi yang diterima yang
didekripsi, oleh OpenSSL, yang lebih cepat daripada TLS milik `tailscaled`.

```text
Pengunjung ──HTTPS──▶ Relai Funnel ──WireGuard──▶ tailscaled (TCP + PROXY v2)
                                                       │
                                                       ▼
                                        Gerbang omega-tail (HAProxy, 127.0.0.1)
                                        ├── ditolak sebelum TLS: daftar hitam, laju, anggaran, nama tujuan, pengelompokan
                                        └── diterima: TLS (sertifikat *.ts.net) ──HTTP──▶ situs Anda
```

Gerbang hanya mendengarkan pada loopback mesin dan berjalan di bawah akun Anda. Mesin-mesin di tailnet Anda selalu
diterima, sebelum aturan apa pun: hanya pengunjung Funnel yang disaring.

### Yang harus diizinkan Tailscale (konsol administrasi)

Pengaturan ini dilakukan sekali, di konsol web Tailscale; omega-tail tidak mengubahnya.

- **MagicDNS** dan **sertifikat HTTPS** diaktifkan untuk tailnet (diperlukan untuk Serve, Funnel, dan sertifikat
  gerbang).
- **Funnel diizinkan** untuk mesin tersebut dalam kebijakan akses tailnet (atribut `funnel`).
- Untuk simpul keluar atau subnet yang diumumkan: **persetujuan** keduanya di konsol.

[↑ Daftar isi](#daftar-isi)

---

## Fitur

Menu utama memiliki dua kolom berisi enam: **TAILSCALE** untuk mengendalikan, **PERLINDUNGAN** untuk bertahan.

### TAILSCALE

#### 1. Dasbor

- **Tailscale**: layanan, status koneksi, versi yang berjalan dan yang terpasang, nama mesin, alamat, akun,
  perangkat yang daring, kedaluwarsa kunci, operator, simpul keluar yang ditawarkan dan yang digunakan, subnet yang
  diumumkan.
- **Mesin**: CPU seluruh mesin, beban per inti, suhu, memori, CPU dan memori `tailscaled`, pembatasan, lalu
  status perlindungan (Funnel, firewall dan mode serangan, daftar hitam, pengawasan, perisai).
- **Publikasi**: setiap port yang dipublikasikan, untuk Internet (Funnel) atau untuk tailnet (Serve), mode dan
  tujuannya.
- **Peringatan**, dari yang paling serius hingga yang paling ringan, dengan « Perbaiki » yang membuka layar terkait.
  Misalnya: layanan berhenti, pembaruan terpasang tetapi belum diterapkan, kunci akan kedaluwarsa, Funnel
  dipublikasikan tanpa perlindungan, suhu tinggi, `tailscaled` terlalu boros atau tidak dibatasi, daftar hitam yang
  terus membesar.
- Nilai berwarna hijau, oranye, atau merah menurut ambang (CPU, beban, suhu, memori, `tailscaled`).

#### 2. Layanan tailscaled

- Status menurut sistem init, versi yang berjalan dan yang terpasang, perintah peluncuran, berkas tambahan
  (drop-in), pembatasan.
- **Mulai**, **Hentikan**, **Mulai ulang** (misalnya untuk menerapkan pembaruan yang sudah terpasang).
- **Pengaman**: jika sesi Anda melewati Tailscale (SSH melalui tailnet), Hentikan meminta konfirmasi kedua, karena
  Anda tidak akan bisa menjalankannya lagi.
- **Perbaiki proses mulai**: menemukan berkas tambahan yang menjalankan `tailscale up` saat boot dan berisiko
  mengeluarkan mesin dari tailnet pada perubahan pengaturan pertama; perbaikannya ditampilkan dan berkas aslinya
  disimpan.

#### 3. Koneksi dan pengaturan

- **Hubungkan**, **Putuskan**, **Tambah akun**, **Ganti akun**, **Logout permanen** (nama mesin harus diketik).
- **Semua pengaturan `tailscale set`**, masing-masing dengan kalimat penjelasannya: nama dan nama panggilan mesin,
  rute, DNS tailnet, perisai, penyaringan stateful, mode netfilter, simpul keluar, akses ke jaringan lokal, menawarkan
  mesin sebagai simpul keluar, subnet yang diumumkan, SSH Tailscale, antarmuka web, pembaruan, relai peer, operator.
- Saat mengetik, sebuah bingkai menampilkan **sebelum → sesudah** dan perintahnya; setelah diterapkan, setiap nilai
  yang dibaca ulang ditandai ✔ (diterapkan) atau ✖ (tidak).
- Sebuah peringatan muncul ketika suatu perubahan dapat memutus sesi yang melewati Tailscale.
- **Penerusan IP**: diaktifkan dengan satu tombol ketika mesin berfungsi sebagai simpul keluar atau mengumumkan subnet.

#### 4. Publikasi

- Semua yang dipublikasikan mesin: port, publik (Funnel) atau tailnet (Serve), mode, jalur, tujuan, perlindungan.
- **Publikasikan** layanan lokal dalam HTTPS, HTTP, TCP, atau TLS terminated; **Cabut**; **Tangguhkan Funnel** dan
  **Pulihkan Funnel** (persis seperti semula).
- **Uji ujung ke ujung**: koneksi sungguhan, seperti seorang pengunjung (respons, waktu, sertifikat, versi TLS).
- **Cadangan**: keadaan sebelum setiap perubahan (50 yang terbaru), dapat dipulihkan.
- Setiap perubahan diperiksa; jika ada selisih, publikasi dibangun ulang, jika tidak keadaan sebelumnya dikembalikan.

#### 5. Jaringan dan perangkat

- **Perangkat** di tailnet: sistem, daring atau tidak, jalur (langsung atau melalui relai), terakhir terlihat, alamat,
  lalu lintas yang dipertukarkan; relai Funnel milik Tailscale disembunyikan secara bawaan.
- **Ping Tailscale** (jalur dan latensi), **Siapa ini?** (pemilik sebuah alamat tailnet).
- **Diagnostik jaringan**: UDP, IPv4 / IPv6, jenis NAT, pembukaan port oleh router (UPnP, NAT-PMP, PCP), relai
  terdekat dan latensinya.
- **DNS**, **kunci tailnet**, dan **penghitung internal** Tailscale.
- Hanya baca: tidak ada di layar ini yang mengubah pengaturan.

#### 6. Log

- Log `tailscaled` (journalctl, atau berkas layanan di luar systemd) dan log gerbang, dapat disaring dan diekspor.
- Setiap informasi punya warnanya sendiri, diambil dari tema: tanggal, proses, kategori pesan (kontrol, jaringan, DNS,
  mesin WireGuard), alamat dicetak tebal, galat berwarna merah, peringatan berwarna oranye; untuk gerbang: alasan
  penolakan, pengelompokan, AS, dan negara.

### PERLINDUNGAN

#### 7. Firewall Funnel

- **Pasang HAProxy** melalui pengelola paket distribusi (pacman, apt, dnf, zypper, apk, xbps, emerge).
- **Aktifkan perlindungan**: sertifikat `*.ts.net`, daftar-daftar, konfigurasi yang diperiksa, layanan gerbang,
  peralihan Funnel lalu uji dari Internet; jika gagal, publikasi semula langsung dikembalikan.
- **Nonaktifkan perlindungan**: Funnel dikembalikan persis seperti sebelumnya, dan diperiksa.
- **Aturan** diterapkan tanpa memulai ulang, mode **pengamatan** untuk menyetel ambang tanpa risiko,
  **pengelompokan** (lihat [Rincian perlindungan](#rincian-perlindungan)).
- **Perbarui basis data** AS / negara (DB-IP Lite), dalam proses terpisah.

#### 8. Ketahanan

- **Pembatasan `tailscaled`**: batas atas CPU, bobot dan prioritas, opsi prioritas untuk akses SSH.
- **Pemutus sirkuit Funnel**: ambang CPU dan suhu, pemutusan 10 menit (dihidupkan kembali secara otomatis) atau
  total.
- **Pengawasan otomatis**: hal yang sama tanpa ada orang di depan layar.
- **Perisai port WireGuard**: tombol menuju layarnya (pengamatan, aktif, pasang, pasang ulang, lepas, serahkan).

#### 9. Serangan dan keputusan

- Penghitung gerbang (diterima masuk, ditolak sebelum enkripsi, diizinkan, sedang berjalan) dan alamat yang paling
  aktif, dibaca ulang setiap 2 detik, dengan negara, AS, dan status setiap alamat.
- **Blokir**, **Daftar hitam**, **Buka blokir**, **Percayai**: diterapkan seketika, tanpa memulai ulang gerbang;
  notifikasi menyebutkan dalam satu baris tindakan dan posisi alamat tersebut.
- Tampilan **Sidik jari**, **AS**, dan **Negara**; status mode serangan dan koneksi yang ditolak oleh pengelompokan.
- **Pengelolaan daftar hitam**: daftar lengkap dengan tanggal penambahan dan asal, penambahan, penghapusan, impor
  berkas TXT (duplikat, jaringan yang sudah tercakup, dan alamat tailnet disisihkan), pembersihan dengan pratinjau
  (menurut umur, N yang tertua, rentang baris, satu asal, semuanya), ekspor TXT (dapat diimpor ulang), HTML, dan JSON.
  Batas 50.000 entri.

#### 10. Laporan

- Semua yang diketahui omega-tail tentang mesin, berupa fakta: Tailscale, publikasi, mesin, firewall, ketahanan,
  peringatan, dan **serangan selama 7 hari terakhir** yang dibaca dari log gerbang.
- **Privasi**: secara bawaan, tanpa akun Tailscale maupun nama dan alamat perangkat di tailnet, agar dapat
  dikirim kepada orang lain.
- Ekspor **TXT**, **HTML** (tema sesuai pilihan), dan **JSON**; **Lihat ekspor** membuka folder di peramban.

#### 11. Pengaturan

- Bahasa antarmuka dan ekspor, tema antarmuka dan ekspor, folder ekspor dan tangkapan layar, serta
  pembersihannya.

#### 12. Bantuan

- Satu bagian per layar, pintasan, baris perintah, dan **Kontak dan dukungan**.

[↑ Daftar isi](#daftar-isi)

---

## Rincian perlindungan

Setiap perlindungan menjawab ancaman tertentu; tidak ada yang dipaksakan.

| Perlindungan | Melawan apa | Di mana |
|---|---|---|
| Gerbang (aturan) | Lonjakan dari satu atau beberapa alamat, koneksi yang tidak menuju situs | Firewall Funnel |
| Pengelompokan | Serangan dengan alamat yang tersebar (ribuan alamat, masing-masing satu koneksi) | Firewall Funnel |
| Daftar hitam | Alamat dan jaringan yang dikenal menyerang, disimpan dalam jangka panjang | Serangan dan keputusan |
| Pembatasan | `tailscaled` yang bisa menghabiskan seluruh mesin saat diserang | Ketahanan |
| Pemutus sirkuit | Mesin tetap jenuh meski sudah dilindungi: memutus Funnel sementara | Ketahanan |
| Pengawasan otomatis | Hal yang sama, tanpa ada orang di depan layar | Ketahanan |
| Perisai WireGuard | Banjir paket UDP di port `tailscaled`, baik Funnel terbuka maupun tidak | Ketahanan |

### Gerbang (Firewall Funnel)

Aturan diterapkan dalam urutan ini, semuanya sebelum enkripsi:

1. **Mesin tailnet** (100.64.0.0/10, fd7a:115c:a1e0::/48): selalu diterima.
2. **Daftar tepercaya**: tidak pernah dibatasi. **Daftar hitam**: ditolak sampai dihapus dari daftar.
3. **Laju per alamat** (40 koneksi / 10 dtk secara bawaan): jika terlampaui, alamat diblokir selama durasi yang
   dipilih (60 mnt secara bawaan).
4. **Laju per prefiks** /24 untuk IPv4, /64 untuk IPv6.
5. **Anggaran global** koneksi yang diterima per detik: prosesor tidak pernah kewalahan.
6. **Nama tujuan**: koneksi yang tidak menuju nama mesin akan ditolak.

Sertifikat `*.ts.net` milik gerbang diminta dari Tailscale, diperiksa setiap hari, dan diperbarui tanpa memulai ulang
30 hari sebelum kedaluwarsa. Mode **pengamatan** menghitung semuanya tanpa menolak apa pun.

### Pengelompokan (sidik jari, AS, negara)

Menghadapi serangan dengan alamat yang tersebar, aturan per alamat hanya melihat setiap alamat satu kali. Karena itu
gerbang juga mengelompokkan setiap klien menurut **sidik jari JA4**, **AS**, dan **negaranya**, lalu menghitung laju
setiap kelompok.

- **Mode serangan otomatis**: di atas 80 koneksi masuk per detik (dapat diatur), gerbang beralih sendiri ke mode
  serangan, dan keluar darinya setelah 5 menit tenang.
- Hanya dalam mode serangan: sidik jari tak dikenal yang melonjak, AS penyedia hosting atau cloud (daftar dapat
  diubah), atau negara dalam daftar Anda (kosong secara bawaan) yang melampaui lajunya akan ditolak.
- **Peramban umum** (Chrome, Edge, Firefox) tidak pernah terkena aturan ini; **klien yang dikenal** (diterima dalam
  24 jam terakhir) didahulukan sebelum anggaran global.
- **Pembelajaran**: selama 7 hari, gerbang mempelajari sidik jari yang biasa bagi situs Anda (tidak pernah selama
  serangan); sampai saat itu pengelompokan tetap dalam mode pengamatan.
- Di luar serangan, satu dari sepuluh koneksi dikelompokkan; saat serangan, semuanya.
- Basis data AS / negara adalah **DB-IP Lite**, diunduh dan diperbarui sebulan sekali.

### Ketahanan

- **Pembatasan**: sebuah berkas tambahan terpisah membatasi `tailscaled` (misalnya satu inti penuh pada mesin dengan
  4 thread) dan menurunkan prioritasnya. Konfigurasi Anda sendiri tidak pernah diubah.
- **Pemutus sirkuit**: ketika `tailscaled` tetap di atas ambang CPU (80 % dari satu inti selama 60 dtk secara bawaan)
  atau suhu mencapai 85 °C, omega-tail menawarkan untuk memutus Funnel selama 10 menit (dihidupkan kembali secara
  otomatis, persis seperti semula, bahkan saat omega-tail ditutup), memutusnya sepenuhnya, atau menunggu. Tailnet
  tidak pernah diputus.
- **Pengawasan otomatis** (nonaktif secara bawaan): sebuah layanan di bawah akun Anda memutus Funnel sendiri setelah
  tiga kali ambang terlampaui, 15 menit pada kali pertama, 30 pada kali kedua, lalu satu jam, dan menghidupkannya
  kembali sendiri.

### Perisai port WireGuard

`tailscaled` menghabiskan sekitar satu inti prosesor untuk 100.000 paket per detik yang diterima di port UDP-nya,
bahkan paket yang tidak valid. Perisai adalah tabel nftables yang dipasang di depannya, pada kartu jaringan:

- **peer yang dikenal** (yang dikirimi data oleh `tailscaled`) tidak pernah dibatasi;
- jabat tangan dibatasi 20 per detik per sumber;
- sumber lain memiliki anggaran (masing-masing 500 paket per detik, total 5.000);
- paket yang bukan WireGuard ditolak.

Perisai dipasang terlebih dahulu dalam mode **pengamatan**, lalu **aktif**. Jika terhubung melalui omega-connect,
**omega-fire** (3.7.0 atau lebih baru) dapat memasang dan mengelolanya sebagai pengganti omega-tail: tabelnya sama,
dan berpindah tangan tanpa disentuh.

[↑ Daftar isi](#daftar-isi)

---

## Pengukuran

Pilihan-pilihan omega-tail berasal dari pengukuran, pada mesin dari generasi yang sama dengan mesin yang
dilindunginya (prosesor tahun 2010 hingga 2016, sebagian besar tanpa akselerasi AES).

| Pengukuran | Hasil |
|---|---|
| Porsi TLS dalam biaya sebuah koneksi Funnel bawaan | sekitar 80 % |
| Biaya koneksi yang **ditolak** oleh gerbang, dibandingkan dengan Funnel bawaan | **4,6 kali lebih rendah** |
| Biaya koneksi yang **diterima** oleh gerbang, dibandingkan dengan Funnel bawaan | **2 kali lebih rendah** |
| Throughput dengan gerbang, koneksi tetap terbuka (dibandingkan dengan TLS dalam Go seperti milik `tailscaled`) | **+15 %** permintaan, −20 % CPU |
| Perisai WireGuard: banjir yang menghabiskan satu inti penuh `tailscaled` | **1 %** dari satu inti |
| Memori layanan (gerbang, pengawasan, perisai) | sekitar 67 MB |

Jadi gerbang tidak menurunkan throughput sebuah situs: pada mesin-mesin ini, enkripsi itu sendirilah yang membatasi,
dengan atau tanpa omega-tail, dan di produksi Funnel bagaimanapun juga melewati relai Tailscale dan router.

[↑ Daftar isi](#daftar-isi)

---

## Arsitektur

```text
src/omega_tail/
├── app/              Akar komposisi: merakit lapisan, titik masuk (antarmuka, baris perintah)
├── core/             Konstanta bersama
├── domain/           Logika bisnis murni: aturan gerbang, peringatan, pemutus sirkuit, pengawasan, daftar hitam…
├── application/      Kasus penggunaan: publikasi, firewall, ketahanan, laporan, pengaturan
├── ports/            Kontrak (Protocol) yang diharapkan oleh aplikasi
├── infrastructure/   Tailscale, HAProxy, nftables, systemd / OpenRC / runit, log, ekspor, skrip Lua
├── interfaces/       tui/ (Textual), cli/ (baris perintah), shared/ (bantuan, laporan, presentasi)
└── shared/           Bahasa (gettext)
```

### Prinsip desain

- `domain/` tidak berisi pembacaan maupun penulisan apa pun: semuanya dapat diuji tanpa mesin.
- `application/` mengorkestrasi kasus penggunaan melalui domain dan port; antarmuka dan baris perintah memanggil
  kasus penggunaan yang sama.
- Hanya `infrastructure.commands` dan `infrastructure.privileged` yang menjalankan perintah; antarmuka tidak pernah
  menjalankannya secara langsung. Aturan ini diperiksa secara otomatis (import-linter).
- Antarmuka bertumpu pada [omega-lib](https://github.com/kraynux), pustaka yang dipakai bersama oleh seluruh suite
  OMEGA (tema, deteksi terminal, bahasa, kontak dan dukungan, perisai WireGuard). Pustaka ini tidak dipublikasikan di
  PyPI: ia disertakan dalam arsip (`vendor/omega-lib/`).
- Setiap panggilan yang lambat (Tailscale, HAProxy, disk, jaringan) berjalan sebagai tugas latar belakang: antarmuka
  tidak pernah membeku.

[↑ Daftar isi](#daftar-isi)

---

## Prasyarat

### Sistem

- Linux, distribusi apa pun (diuji di Arch Linux dan turunannya).
- Python 3.10 atau lebih baru, dengan modul `venv`.
- Sistem init: **systemd**, **OpenRC**, atau **runit**.
- `sudo` untuk tindakan yang mengubah mesin (diminta tindakan demi tindakan, tidak pernah saat peluncuran).
- Terminal minimal 80×24 (lihat [Tema dan terminal](#tema-dan-terminal)).

### Tailscale

- **Tailscale** terpasang dan terhubung (klien `tailscale` dan layanan `tailscaled`); diuji dengan versi 1.104.
- Untuk Funnel: MagicDNS, sertifikat HTTPS, dan Funnel diizinkan di konsol Tailscale (lihat
  [Yang harus diizinkan Tailscale](#yang-harus-diizinkan-tailscale-konsol-administrasi)).

### Dependensi Python

Dipasang oleh `install.sh` di dalam lingkungan virtual:

- `textual`: antarmuka.
- `omega-lib`: pustaka bersama suite OMEGA, disertakan dalam arsip.

### Komponen wajib dan opsional

omega-tail mendeteksi apa yang tersedia dan hanya mengaktifkan apa yang dapat digunakan.

| Komponen | Peran | Status |
|---|---|---|
| Tailscale (`tailscale`, `tailscaled`) | Semua yang dikendalikan omega-tail | **Wajib** |
| Python 3.10+, `textual`, `omega-lib` | Aplikasinya | **Wajib** |
| systemd, OpenRC, atau runit | Layanan gerbang, pengawasan, perisai | **Wajib** (salah satu dari ketiganya) |
| HAProxy 3.x | Gerbang Firewall Funnel | Opsional (dapat dipasang dari omega-tail) |
| HAProxy dengan Lua | Pengelompokan (sidik jari, AS, negara) | Opsional (umumnya tersedia di distribusi populer) |
| nftables (kernel dengan `nft_limit`) | Perisai port WireGuard | Opsional |
| Pembacaan log sistem (grup `systemd-journal`, `adm`, atau `wheel`) | Log, laporan serangan | Disarankan |
| Peramban dan desktop | « Lihat ekspor » di peramban (jika tidak ada, dibaca di dalam omega-tail) | Opsional |
| omega-connect | Registri, sinkronisasi, pembaruan suite | Opsional |
| omega-fire 3.7.0+ | Pengelolaan perisai WireGuard dari omega-fire | Opsional |

[↑ Daftar isi](#daftar-isi)

---

## Instalasi

Arsip resmi disediakan dalam format `.tar.gz`. Periksa integritasnya sebelum instalasi, dengan berkas `sha.txt` yang
dipublikasikan di sebelahnya:

```bash
sha256sum omega-tail-0.7.0.tar.gz
```

> ⚠️ **Ketiga metode ini untuk instalasi pertama.** Jika `~/omega-tail` sudah ada, gunakan bagian
> [Pembaruan](#pembaruan). Jangan pernah menjalankan ulang perintah ini dari dalam folder `omega-tail` yang sudah
> ada: `tar` akan membuat `omega-tail/omega-tail/` yang bersarang.

Tidak ada langkah instalasi yang memerlukan hak root: omega-tail dijalankan sebagai pengguna biasa.

### Metode 1 — skrip instalasi

```bash
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Tampaknya Anda sudah berada di folder omega-tail — lihat bagian Pembaruan di README." >&2; exit 1; }
[ -d omega-tail ] && echo "ℹ️ Sudah diekstrak di sini, langkah dilewati." || tar -xzf omega-tail-0.7.0.tar.gz
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail sudah ada, pemindahan dilewati." || mv omega-tail ~/
cd ~/omega-tail/
chmod +x install.sh
./install.sh
```

Skrip ini membuat lingkungan virtual, memasang dependensi (omega-lib yang disertakan lebih dulu), membuat peluncur
dapat dieksekusi, menulis token instalasi yang dibaca omega-connect, dan menawarkan alias `omega-tail`. Skrip ini
aman untuk dijalankan ulang.

### Metode 2 — instalasi lengkap yang tangguh

Perintah ini dapat dijalankan ulang: langkah yang sudah selesai akan dilewati.

```bash
([ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Tampaknya Anda sudah berada di folder omega-tail — lihat bagian Pembaruan di README." >&2; exit 1; }; [ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail sudah ada, ekstraksi dilewati." || (tar -xzf omega-tail-0.7.0.tar.gz && mv omega-tail ~/)) && cd ~/omega-tail/ && ([ -f .venv/bin/activate ] && echo "ℹ️ .venv sudah ada, langkah dilewati." || python3 -m venv .venv) && source .venv/bin/activate && ([ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib || true) && pip install -q -e . && chmod +x omega-tail.sh install.sh && ./omega-tail.sh synchro jeton > /dev/null && echo "✅ Omega-Tail terpasang. Jalankan ./omega-tail.sh."
```

### Metode 3 — instalasi terperinci

```bash
# 0. Memastikan tidak menjalankan ulang dari dalam omega-tail yang sudah ada
[ "$(basename "$PWD")" = "omega-tail" ] && { echo "❌ Tampaknya Anda sudah berada di folder omega-tail — lihat bagian Pembaruan di README." >&2; exit 1; }

# 1. Ekstrak
[ -d omega-tail ] && echo "ℹ️ Sudah diekstrak di sini, langkah dilewati." || tar -xzf omega-tail-0.7.0.tar.gz

# 2. Pindahkan ke home
[ -d ~/omega-tail ] && echo "ℹ️ ~/omega-tail sudah ada, pemindahan dilewati." || mv omega-tail ~/

# 3. Masuk ke proyek
cd ~/omega-tail/

# 4. Buat lingkungan virtual
[ -f .venv/bin/activate ] && echo "ℹ️ .venv sudah ada, pembuatan dilewati." || python3 -m venv .venv

# 5. Pasang dependensi (omega-lib yang disertakan lebih dulu)
source .venv/bin/activate
[ -d vendor/omega-lib ] && pip install -q -e vendor/omega-lib
pip install -q -e .

# 6. Jadikan peluncur dapat dieksekusi
chmod +x omega-tail.sh install.sh

# 7. Tulis token instalasi (dibaca oleh omega-connect; opsional)
./omega-tail.sh synchro jeton

# 8. Jalankan
./omega-tail.sh
```

Di Debian, Ubuntu, dan turunannya, modul `venv` tidak selalu terpasang bersama Python:
`sudo apt install python3-venv`.

### Pembaruan

Layanan omega-tail (gerbang, pengawasan) menggunakan berkas-berkas di `~/omega-tail/var/`. Karena itu pembaruan harus
**membiarkan folder ini di tempatnya**: arsip tidak berisi `var/`, dan diekstrak menimpa instalasi yang sudah ada.

Dari folder yang berisi arsip, **selain `~/omega-tail`**:

```bash
# 1. Cadangkan instalasi saat ini (termasuk var/)
tar -czf ~/omega-tail-sauvegarde-$(date +%Y%m%d).tar.gz -C ~ omega-tail

# 2. Ekstrak versi baru di atasnya (var/ dipertahankan)
tar -xzf omega-tail-0.7.0.tar.gz -C ~/

# 3. Pasang ulang (dependensi, peluncur, token instalasi)
cd ~/omega-tail
./install.sh

# 4. Jalankan kembali omega-tail
./omega-tail.sh
```

Jika gerbang aktif, **Firewall Funnel → « Terapkan aturan »** membuat ulang konfigurasinya dengan versi baru, tanpa
memulai ulang. Jika pengawasan otomatis aktif, **Ketahanan → « Aktifkan pengawasan »** menjalankannya kembali dengan
kode baru. omega-connect juga dapat melakukan pembaruan (layar Updater).

### Alias Bash atau Zsh

`install.sh` menawarkan alias. Untuk menambahkannya secara manual:

```bash
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.bashrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.bashrc
grep -qxF 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' ~/.zshrc 2>/dev/null || echo 'alias omega-tail="$HOME/omega-tail/omega-tail.sh"' >> ~/.zshrc
```

Alias ini bernama `omega-tail`, bukan `tail`, agar tidak menutupi perintah sistem `tail`.

[↑ Daftar isi](#daftar-isi)

---

## Penggunaan

### Menjalankan

```bash
cd ~/omega-tail
./omega-tail.sh

# atau cukup, jika alias telah dibuat:
omega-tail
```

Peluncur tidak meminta hak yang lebih tinggi: omega-tail berjalan di bawah akun Anda, dan sudo hanya diminta oleh
tindakan yang memerlukannya, di terminal, dengan perintah yang ditampilkan lebih dulu.

### Langkah pertama yang disarankan

Untuk melindungi situs yang dipublikasikan melalui Funnel, dalam urutan ini:

1. **Dasbor**: baca peringatan; **Jadi operator** (sekali, melalui sudo) untuk mengatur Tailscale tanpa sudo.
2. **Ketahanan → Terapkan pembatasan**: `tailscaled` tidak akan bisa lagi menghabiskan seluruh mesin.
3. **Publikasi**: publikasikan situs dalam **HTTPS di port 443**, jalur `/`, lalu lakukan **uji ujung ke ujung**.
4. **Firewall Funnel → Pasang HAProxy**, lalu **Aktifkan perlindungan**, mula-mula dalam mode **pengamatan**.
5. Beberapa hari kemudian, **Serangan dan keputusan**: jika penghitung hanya menunjukkan penyalahgunaan, alihkan gerbang
   ke mode **normal**.
6. Biarkan **pengelompokan** belajar selama 7 hari dalam mode pengamatan, lalu alihkan ke **diterapkan**.
7. **Ketahanan → Perisai port WireGuard**: pasang dalam mode pengamatan, lalu alihkan ke aktif.
8. Untuk mesin tanpa orang di depan layar: **Ketahanan → Aktifkan pengawasan**.

### Bahasa antarmuka

17 bahasa: Prancis, Inggris, Spanyol, Portugis (Brasil), Italia, Jerman, Belanda, Polandia, Rusia, Tionghoa,
Vietnam, Thai, Indonesia, Jepang, Korea, Hindi, Arab.

- Dipilih di pengaturan (tombol `s`, « Langue / Language », label yang tidak pernah diterjemahkan), diterapkan dengan
  memulai ulang antarmuka saja.
- Sesekali: `OMEGA_TAIL_LANG=en ./omega-tail.sh`.
- Di konsol teks Linux (TTY), bahasa yang aksaranya tidak ada di font konsol ditampilkan dalam bahasa Inggris selama
  sesi tersebut; bahasa Arab ditampilkan dari kanan ke kiri.
- **Bahasa ekspor** (laporan, daftar hitam, log) diatur terpisah, bawaannya « Sama dengan antarmuka ».

### Kontak dan dukungan

Bantuan (tombol `a`) menyediakan layar **Kontak dan dukungan**:

- *Traktir kopi* (halaman PayPal pengembang);
- *Hubungi dukungan* (alamat email dan formulir situs, ditampilkan apa adanya);
- *Daftarkan saya sebagai pengguna (anonim)*;
- *Periksa pembaruan*.

Pendaftaran bersifat sukarela, nonaktif secara bawaan, dan dikirim hanya sekali. Pendaftaran hanya digunakan untuk
menghitung pengguna dan, jika Anda mau, benua atau negara mereka (daftar tertutup, tidak pernah teks bebas). Yang
dikirim adalah kunci yang diambil secara acak, nama perangkat lunak (`omega-tail`), dan versinya; tidak pernah nama,
nama mesin, pengaturan, maupun alamat tailnet. Penarikan kapan saja dari layar yang sama (*Jangan daftarkan saya
lagi*). Pemeriksaan pembaruan hanya membaca daftar versi yang dipublikasikan di situs, dan tidak pernah tanpa klik.

### Tautan dengan alat omega lainnya

- **omega-connect**: `install.sh` menulis token instalasi (`var/omega-jeton.json`) yang menjelaskan alat ini dan
  versinya, tanpa menjalankan apa pun. omega-connect menggunakannya untuk Registri, sinkronisasi, perbaikan, pembaruan,
  dan instalasi. `./omega-tail.sh synchro jeton` menulisnya ulang secara manual.
- **omega-fire** (3.7.0 atau lebih baru), yang terhubung melalui omega-connect, dapat memasang dan mengelola perisai
  port WireGuard; daftar aturannya menampilkan perisai tersebut dengan asal omega-tail.

### Baris perintah

Semua perintah ditulis `./omega-tail.sh …` (atau `omega-tail …` dengan alias):

| Perintah | Peran |
|---|---|
| `omega-tail` | Antarmuka |
| `omega-tail etat [--format json]` | Status Tailscale, mesin, dan peringatan, dalam teks atau untuk skrip |
| `omega-tail aide` | Bantuan lengkap dalam teks |
| `omega-tail rapport [--format txt\|html\|json] [--prive] [--exporter]` | Laporan, ditampilkan atau disimpan |
| `omega-tail disjoncteur etat \| couper --minutes N \| couper --totale \| retablir` | Memutus atau menghidupkan kembali Funnel |
| `omega-tail veille etat` | Status pengawasan otomatis dan baris-baris terakhirnya |
| `omega-tail porte etat` | Status gerbang dan penghitung |
| `omega-tail porte certificat [--si-besoin]` | Memperbarui sertifikat `*.ts.net` milik gerbang |
| `omega-tail porte groupes` | Pengelompokan: mode serangan, sidik jari, AS, negara |
| `omega-tail porte base` | Memperbarui basis data AS / negara |
| `omega-tail porte bloquer ADRESSE [--toujours]` | Memblokir sebuah alamat atau jaringan (daftar hitam dengan `--toujours`) |
| `omega-tail porte debloquer ADRESSE` | Membuka blokir |
| `omega-tail porte confiance ADRESSE` | Menjadikan tepercaya |
| `omega-tail synchro jeton` | Menulis token instalasi (omega-connect) |
| `omega-tail --version` | Versinya |

### Alur umum

1. Layar pembuka, lalu menu utama dalam dua kolom (TAILSCALE dan PERLINDUNGAN).
2. Di bawah judul setiap layar, **pita status** merangkum semuanya: layanan, CPU mesin dan `tailscaled`, suhu,
   memori, Funnel, firewall, pengawasan, koneksi. Pita ini dibaca ulang setiap 5 detik.
3. Setiap tindakan yang mengubah mesin menampilkan perintahnya, lalu meminta konfirmasi; sudo diketik di terminal,
   lalu antarmuka kembali.
4. Tindakan sensitif (logout permanen, pembersihan total daftar hitam) meminta Anda mengetik sebuah kata.
5. Hasilnya ditampilkan dalam satu baris, diperiksa berdasarkan status yang dibaca ulang.

### Navigasi

- Panah atas / bawah: berpindah dari satu elemen ke elemen lain (baris tabel, tombol).
- Tab / Shift+Tab: berpindah dari satu area layar ke area lain.
- Enter atau klik: mengaktifkan tombol yang dipilih; di tabel peringatan, « Perbaiki ».
- `Esc`: kembali ke layar sebelumnya (di menu: keluar).
- `a`: bantuan, dari layar mana pun.
- `s`: pengaturan, dari layar mana pun.
- `t`: tema berikutnya (disimpan).
- `r`: menggambar ulang layar, menampilkan ukuran terminal, dan membaca ulang status.
- `q`: keluar, dengan konfirmasi.
- `Ctrl+P`: perintah (tema, tangkapan layar SVG di folder tangkapan layar, keluar).

[↑ Daftar isi](#daftar-isi)

---

## Tema dan terminal

Sepuluh tema `omega-*` dipakai bersama seluruh suite OMEGA:

```text
omega-base       omega-dark       omega-light
omega-neon       omega-burn       omega-pink
omega-hack       omega-contrast   omega-mono
omega-minimal
```

- Beralih antartema dengan `t`, atau pilih salah satu di pengaturan (`s`); pilihan Anda disimpan.
- Ekspor HTML memiliki temanya sendiri: `omega-base`, `omega-burn`, `omega-neon`, `light-basic`, `light-alt`.
- omega-tail menyesuaikan kompleksitas visual dengan terminal yang terdeteksi melalui **profil tampilan**: Lengkap,
  Standar, Ringkas, atau Mono (hanya ASCII).

| Ukuran minimum | Profil | Terminal umum |
|---|---|---|
| 120×32 atau lebih | Lengkap | Ghostty, Alacritty, WezTerm, Kitty |
| 100×28 atau lebih | Standar | Konsole, GNOME Terminal, Terminator, xfce4-terminal |
| 80×24 atau lebih | Ringkas | urxvt, xterm, SSH modern |
| di bawah 80×24 | Mono (hanya ASCII) | Linux TTY, SSH lama |

Setelah ukuran diubah, `r` membaca ulang ukuran terminal; ukuran itu ditampilkan di bagian atas, di sebelah tema.

[↑ Daftar isi](#daftar-isi)

---

## Berkas, layanan, dan kompatibilitas

### Di folder omega-tail

Seluruh status omega-tail berada di `~/omega-tail/var/`, dibuat ulang saat mulai dan tidak pernah dipublikasikan:

```text
var/
├── settings.json         pengaturan (bahasa, tema, folder, ambang, aturan gerbang)
├── omega-jeton.json      token instalasi (omega-connect)
├── porte/                konfigurasi gerbang, sertifikat, daftar tepercaya dan daftar hitam, basis data AS / negara
├── veille/               log pengawasan otomatis
├── survie/               berkas asli dari berkas yang diubah, status pemutus sirkuit
├── funnel/sauvegardes/   publikasi sebelum setiap perubahan (50 yang terbaru)
├── exports/              laporan, log, dan daftar yang diekspor
└── screenshots/          tangkapan layar (Ctrl+P)
```

### Di sistem (hanya jika Anda mengaktifkan perlindungan terkait)

Setiap berkas dipasang melalui sudo, dengan perintah yang ditampilkan, dan dilepas oleh tindakan kebalikannya di
omega-tail.

| Berkas atau layanan | Dipasang oleh | Dilepas oleh |
|---|---|---|
| Layanan `omega-tail-porte` (systemd, OpenRC, atau runit) dan `omega-tail-porte-certificat` (timer systemd, atau satu baris bertanda di crontab Anda) | Aktifkan perlindungan | Nonaktifkan perlindungan |
| `/etc/systemd/system/tailscaled.service.d/50-omega-tail.conf` (atau sebuah control group di luar systemd) | Terapkan pembatasan | Lepas pembatasan |
| Timer `omega-tail-retablir-*` (menghidupkan kembali setelah pemutusan) | Pemutus sirkuit | Akhir pemutusan |
| Layanan `omega-tail-veille` | Aktifkan pengawasan | Nonaktifkan pengawasan |
| Layanan `omega-bouclier-wg`, tabel nftables, `/etc/omega-bouclier-wg/` | Perisai: Pasang | Perisai: Lepas |
| `/etc/sysctl.d/99-omega-tail-forwarding.conf` | Aktifkan penerusan IP | Penghapusan berkas |

Berkas `override.conf` milik `tailscaled`, jika ada, tidak pernah diubah.

### Sistem init

| | systemd | OpenRC | runit |
|---|---|---|---|
| Layanan `tailscaled` | `systemctl` | `rc-service` | `sv` |
| Log | `journalctl` | berkas layanan | `svlogd`, `socklog` |
| Pembatasan | berkas tambahan systemd | control group (cgroup v2) | control group (cgroup v2) |
| Pemutusan sementara | timer systemd | proses terlepas di bawah akun Anda | proses terlepas di bawah akun Anda |
| Gerbang, pengawasan, perisai | layanan systemd | layanan OpenRC | layanan runit |

Di luar systemd, pembatasan melalui control group hilang jika `tailscaled` dimulai ulang: sebuah peringatan kemudian
menawarkan untuk memasangnya kembali.

### IPv4 dan IPv6

Gerbang, daftar-daftar, pengelompokan, dan perisai menangani kedua keluarga. Prefiks yang dihitung adalah /24 untuk
IPv4 dan /64 untuk IPv6; alamat IPv4 yang terlihat dalam bentuk `::ffff:a.b.c.d` diperlakukan sebagai alamat IPv4.

[↑ Daftar isi](#daftar-isi)

---

## Keamanan

omega-tail bekerja pada layanan yang terekspos ke Internet; ia dirancang agar tidak pernah memperburuk keadaan.

- **Tidak pernah root**: aplikasi, gerbang HAProxy, dan pengawasan berjalan di bawah akun Anda; sudo hanya diminta
  untuk memasang atau melepas layanan, dengan perintah yang ditampilkan lebih dulu.
- **Saluran privat**: socket administrasi gerbang bermode 600 di dalam folder 700; sinkronisasi tabel-tabelnya
  melewati socket di folder yang sama.
- **Pembatalan**: setiap peralihan Funnel dicadangkan, diperiksa, dan keadaan sebelumnya dikembalikan jika gagal.
- **Pengamatan terlebih dahulu**: gerbang, pengelompokan, dan perisai dipasang dalam mode pengamatan; tidak ada yang
  ditolak sebelum Anda memutuskannya.
- **Tailnet tidak pernah diputus**: gerbang selalu menerima mesin-mesin Anda, dan pemutus sirkuit hanya memutus
  Funnel.
- **Masukan diperiksa**: hanya alamat atau jaringan dalam bentuk kanonis yang mencapai HAProxy; nama yang dideklarasikan
  oleh mesin tailnet dibersihkan sebelum ditampilkan.
- **Audit**: kode telah diaudit (claude-security, 2026-11-25); 7 temuan yang dilaporkan, tidak satu pun dapat
  dieksploitasi dari jarak jauh oleh pengunjung, telah diperbaiki pada hari yang sama.
- Uji terlebih dahulu pada mesin uji atau dalam mode pengamatan, dan gunakan jaringan dokumentasi RFC 5737 untuk uji
  IPv4: `192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`.

[↑ Daftar isi](#daftar-isi)

---

## Pengujian dan kualitas

Rangkaian ini berisi **179 tes**: domain, kasus penggunaan, infrastruktur (dengan Funnel tersimulasi), layar Textual
dengan stylesheet sebenarnya, sistem init, keamanan. Kode diperiksa oleh `ruff`, `mypy`, dan `import-linter`
(aturan lapisan). Folder `tests/` disertakan dalam arsip.

```bash
cd ~/omega-tail
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check src tests
mypy src
lint-imports
```

Sebagian besar tes tidak memerlukan Tailscale, HAProxy, maupun root.

[↑ Daftar isi](#daftar-isi)

---

## Status proyek

### Poin yang sudah berjalan

- Kendali penuh atas Tailscale: layanan, koneksi, pengaturan, publikasi, jaringan, log.
- Gerbang HAProxy sebelum TLS, di produksi sejak 2026-11-23, dengan aturan, daftar, pengelompokan, dan mode serangan.
- Ketahanan: pembatasan, pemutus sirkuit, pengawasan otomatis.
- Perisai port WireGuard, di produksi sejak 2026-11-24.
- Laporan dan ekspor TXT, HTML, JSON.
- Kompatibel dengan omega-connect dan omega-fire.

### Keterbatasan yang diketahui

- Layanan di bawah OpenRC dan runit tercakup oleh tes, tetapi belum divalidasi di mesin sungguhan.
- Gerbang melindungi Funnel yang dipublikasikan dalam HTTPS di satu port saja, dengan jalur `/`.
- Pengelompokan memerlukan HAProxy yang dikompilasi dengan Lua; tanpa Lua, gerbang berjalan tanpa pengelompokan.
- Perisai tidak dapat dipasang pada kernel yang diperbarui tanpa memulai ulang (modul tidak ada): layar
  memberitahukannya.
- Serangan yang membuat jalur Internet itu sendiri jenuh tetap berada di luar jangkauan alat yang terpasang di mesin.
- Throughput situs yang dipublikasikan melalui Funnel tetap dibatasi oleh relai Tailscale dan oleh router.

[↑ Daftar isi](#daftar-isi)

---

## Pencopotan

Pertama, lepaskan dari omega-tail apa yang telah dipasang di sistem, dalam urutan ini:

1. **Firewall Funnel → Nonaktifkan perlindungan** (Funnel dikembalikan seperti sebelumnya).
2. **Ketahanan → Nonaktifkan pengawasan**.
3. **Ketahanan → Perisai port WireGuard → Lepas**.
4. **Ketahanan → Lepas pembatasan**.

Lalu hapus foldernya:

```bash
rm -rf ~/omega-tail
```

Hapus secara manual ekspor yang ditempatkan di tempat lain, alias `omega-tail` dari `~/.bashrc` atau `~/.zshrc`, dan,
jika Anda pernah mengaktifkannya, berkas `/etc/sysctl.d/99-omega-tail-forwarding.conf`. Hak operator Tailscale dicabut
dengan `sudo tailscale set --operator=`.

[↑ Daftar isi](#daftar-isi)

---

## Lisensi

Omega-Tail didistribusikan di bawah lisensi **MIT**. Lihat berkas [`LICENSE`](../../../LICENSE) untuk teks lengkapnya.

Basis data AS / negara menggunakan IP Geolocation by [DB-IP](https://db-ip.com), di bawah lisensi
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

[↑ Daftar isi](#daftar-isi)

---

> **Omega-Tail — Mengendalikan Tailscale, melindungi Funnel.**
>
> Antarmuka TUI untuk Tailscale, dan sebuah gerbang yang menolak penyalahgunaan sebelum enkripsi apa pun.
