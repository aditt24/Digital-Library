# Perpustakaan Digital

## Deskripsi
Proyek ini adalah sistem perpustakaan digital berbasis web yang dirancang untuk mempermudah mahasiswa dalam mengakses koleksi buku, meminjam, mengembalikan, dan menyumbangkan buku secara online. Aplikasi ini menggunakan Streamlit sebagai framework antarmuka.

## Fitur Utama
- **Login dan Sign Up**: Sistem autentikasi dengan enkripsi kata sandi menggunakan BCrypt.
- **Manajemen Buku**:
  - **Daftar Buku**: Menampilkan koleksi berdasarkan genre.
  - **Pinjam Buku**: Validasi ketersediaan stok buku dan pencatatan peminjaman.
  - **Kembalikan Buku**: Pengembalian Buku dan Menghitung denda jika ada keterlambatan pengembalian.
  - **Sumbang Buku**: Menambahkan buku baru ke koleksi perpustakaan.
- **Dashboard Interaktif**: Navigasi mudah melalui sidebar.

## Teknologi yang Digunakan
- **Bahasa Pemrograman**: Python
- **Framework**: Streamlit
- **Penyimpanan Data**: CSV
- **Enkripsi**: BCrypt untuk keamanan kata sandi

## Struktur Folder
```
Perpustakaan-Digital/
├── data/
│   ├── daftar_buku.csv
│   ├── data_pengguna.csv
│   ├── peminjaman.csv
│   └── pengembalian.csv
├── src/
│   └── projek_perpustakaan.py
├── README.md
└── requirements.txt
```

## Instalasi
1. **Clone Repository**:
   ```bash
   git clone https://github.com/username/Perpustakaan-Digital.git
   cd Perpustakaan-Digital
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan Aplikasi**:
   ```bash
   streamlit run src/projek_perpustakaan.py
   ```

## Penggunaan
1. **Login atau Sign Up**:
   - Pengguna baru harus mendaftar dengan nama, NIM, dan kata sandi.
   - Login dengan akun yang sudah terdaftar.
2. **Akses Fitur**:
   - Lihat daftar buku berdasarkan genre.
   - Pinjam buku dengan menentukan tanggal pengembalian.
   - Kembalikan buku dan bayar denda jika terlambat.
   - Tambahkan buku baru ke koleksi perpustakaan.

## Kontributor
- Aditya Saputra

