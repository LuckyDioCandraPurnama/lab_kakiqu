import pandas as pd
import os
import sys

login_status = False  # Variabel global untuk melacak status login

def clear_alert(n=1):
    for _ in range(n):
        # Gerakkan kursor ke atas satu baris, lalu hapus baris
        print("\033[F\033[K", end='')


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

#================================================================================================
# DATA HANDLING
#================================================================================================
def cek_file(file):
    try:
        return pd.read_csv(f"{file}")
    except FileNotFoundError:
        print("File tidak ditemukan. \nSilahkan periksa kembali nama dan lokasinya.")
        sys.exit()

def halo():
    pass

def input_nama(kata):
    sesuai = True
    while True:
        nama = input(f"{kata}").strip()
        # Memeriksa apakah inputan nama kosong atau tidak 
        if nama :
            # Memeriksa apakah nama hanya mengandung huruf dan spasi
            for char in nama:
                if not (char.isalpha() or char.isspace()):
                    sesuai = False
                    break
            if sesuai:        
                return nama
            
            else:
                print("Input hanya boleh huruf")
                input("Tekan Enter untuk mencoba kembali.")
                clear_alert(3)

        else:
            print("Input tidak boleh kosong")
            input("Tekan Enter untuk mencoba kembali.")
            clear_alert(3)


def input_nim(kata):
    while True:
        angka = input(f"{kata}").strip()
        # Cek jika input merupakan angka dan memiliki 12 digit angka
        if angka.isdigit() and len(angka) == 12:
            angka = int(angka)
            return angka 
        elif not angka.isdigit():
            print("Input harus berupa angka.")
            input("Tekan Enter untuk mencoba kembali.")
            clear_alert(3)
        elif len(angka) != 12:
            print("Input harus terdiri dari 12 digit.")
            input("Tekan Enter untuk mencoba kembali.")
            clear_alert(3)


#================================================================================================
# FITUR
#================================================================================================

def login():
    global login_status  # Mengakses variabel global login_status

    data = cek_file("users.csv")
    while True:
        clear_terminal()
        print("==== Login ====")
        nim = input_nim("NIM: ")
        password = input("Password: ").strip()
        
        user = data[
            (data['nim'] == nim) & 
            (data['password'] == password)]


        if not user.empty:
            user_login = {
                "nama" : user.iloc[0]['nama'],
                "nim" : user.iloc[0]['nim'],
                "role" : user.iloc[0]['role']
            }
            login_status = True  # Update status login saat berhasil
            clear_terminal()
            print("="*(36+len(user_login["nama"])))
            print(f"= Login berhasil! Selamat datang, {user_login['nama']} =")
            print("="*(36+len(user_login["nama"])))

            return user_login

        else:
            print("\nNIM atau Password salah. Silakan coba lagi.")
            input("Tekan Enter untuk melanjutkan.\n")
            clear_alert(3)


def register():
    users = cek_file("users.csv")

    while True:
        clear_terminal()
        print("=== Registrasi Anggota Baru ===")

        nama = input_nama("Nama: ")
        nim = input_nim("NIM: ")
        # Cek apakah username sudah digunakan
        while nim in users['nim'].values:
            print("NIM sudah Terdaftar")
            input("Tekan Enter untuk mencoba kembali.")
            clear_alert(3)
            nim = input_nim("NIM: ")

        password = input("Masukkan password: ").strip()

        print("-" * 26)
        print("Apakah data sudah benar: ")
        print(" [1] Konfirmasi")
        print(" [2] Ulangi")
        print(" [3] Batal")
        print("-" * 26)
        while True:
            pilih = input("Pilih Menu [1/2/3]: ")
            match pilih:
                case "1":
                    # Menambahkan pengguna baru sebagai
                    user_baru = pd.DataFrame([{
                        'nama': nama,
                        'nim': nim,
                        'password': password,
                        'role': 'mahasiswa'
                    }])

                    # Tambahkan data pengguna baru ke dalam DataFrame users
                    users = pd.concat([users, user_baru])

                    # Simpan DataFrame ke dalam 'users.csv'
                    users.to_csv("users.csv", index=False)

                    print("\n==== Registrasi berhasil! ====")
                    print(f"'{nama}' telah ditambahkan sebagai anggota baru.")
                    input("Tekan Enter untuk kembali ke Menu.")
                    return
                case "2":
                    break
                case "3":
                    print("=" * 24)
                    print("==== Peminjaman Dibatalkan ====")
                    input("Tekan Enter untuk kembali ke menu")
                    return  # Keluar dari fungsi jika dibatalkan
                case _:
                    print("Pilihan tidak ada")
                    input("Tekan Enter untuk mencoba kembali")
                    clear_alert(3)
        

def logout():
    global login_status  # Mengakses variabel global login_status
    if login_status:
        clear_terminal()
        print("=" * 19)
        print("= Logout Berhasil =")
        print("=" * 19)
        input("Tekan Enter untuk melanjutkan.")

        login_status = False  # Mengubah status login menjadi False setelah logout
        return login_status
    else:
        print("Anda belum login.")
        input("Tekan Enter untuk melanjutkan.")

#================================================================================================
# NAVIGASI [Tidak Dipakai]
#================================================================================================

def pil_menu():
    while True:
        pilihan = input("Pilih Menu [1/2/3]: ")
        match pilihan:
            case "1":
                login()
                return pilihan
            case "2":
                register()
                return pilihan
            case "3":
                print("Terima Kasih")
                return pilihan
            case _: 
                print("Pilihan tidak ada")
                input("Tekan Enter untuk mencoba kembali")
                clear_alert(3)

#================================================================================================
# Tampilan Menu Login Page
#================================================================================================

def menu_login():
    clear_terminal()

    print(
"""
╔══════════════════╗
║  Selamat Datang  ║
║┌────────────────┐║""")
    
    print("║│  1. Login      │║")
    print("║│  2. Register   │║")
    print("║│  3. Keluar     │║")
    print("║├────────────────┤║")
    print("║│   Login Page   │║")
    print("║└────────────────┘║")
    print("╚══════════════════╝")




