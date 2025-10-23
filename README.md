# OSINT-phone-tool
Simple Termux-based OSINT tool to investigate phone numbers using public data only.
# OSINT-Phone-Tool

Lightweight OSINT helper to manage and investigate **phone numbers** using only public sources.

> **Purpose:** membantu MJ (dan pengguna berwenang) mengumpulkan bukti publik, membuat tautan pencarian otomatis, dan menyimpan log — **tanpa melanggar privasi** atau melakukan pelacakan ilegal.

---

## 🔍 Fitur Utama
- Normalisasi nomor ke format internasional (E.164) menggunakan `phonenumbers`.
- Membuat tautan pencarian publik otomatis:
  - Google Search
  - WhatsApp
  - TrueCaller
  - Telegram
  - Twitter (X)
  - YouTube
- Menyimpan hasil ke file `.csv` (ringan, cocok untuk Termux).
- Struktur repo langsung siap `git clone` + `bash install_termux.sh`.

---

## ⚖️ Disclaimer & Etika
**Wajib dibaca sebelum digunakan:**

- Tool ini hanya mengambil data **publik**, tidak menembus sistem operator atau server mana pun.  
- Tidak menyediakan pelacakan lokasi, IP, atau data pribadi tersembunyi.  
- Gunakan hanya untuk:
  - Investigasi keamanan pribadi yang sah.
  - Dokumentasi bukti publik untuk laporan resmi.  
- Untuk akses data operator (lokasi, CDR, IP), dibutuhkan prosedur hukum / laporan kepolisian.
- Penggunaan untuk stalking, doxxing, atau penyalahgunaan **dilarang keras**.

---

## 📁 Struktur Folder
osint-phone-tool/ ├─ README.md ├─ LICENSE ├─ .gitignore ├─ install_termux.sh ├─ run_light.sh ├─ requirements.txt ├─ numbers.txt.example ├─ osint_phone_tool_light.py ├─ osint_phone_tool.py        # versi penuh (opsional) └─ docs/ └─ usage_guide.md

---

> Dibuat oleh MJ & Elara — untuk investigasi publik yang **etis, ringan, dan aman**.
