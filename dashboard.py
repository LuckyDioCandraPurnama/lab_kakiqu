import pandas as pd
import login as log
from datetime import date,timedelta

#================================================================================================
# DATA HANDLING INPUT DAN UPDATE TANGGAL
#================================================================================================

def input_int(kata):
    while True:
        stok = input(f"{kata}").strip()
        if stok.isdigit():
            stok = int(stok)
            return stok
        else:
            print("Input tidak valid.")
            input("Tekan enter untuk mencoba kembali.")
            log.clear_alert(3)


def input_barang(kata):
    while True:
        nama = input(f"{kata}").strip().lower()
        # if nama and nama.isalpha():

        if nama:
            return nama
        else:
            print("Input harus berupa huruf")
            input("Tekan Enter untuk mencoba kembali.")
            log.clear_alert(3)


def update_status():
    data = log.cek_file('peminjaman.csv')
    today = date.today()

    # Mengubah format String kolom 'tenggat' menjadi 'date'
    data['tenggat'] = pd.to_datetime(data['tenggat']).dt.date
    
    data.loc[
        (data['status'] == 'dipinjam') & (data['tenggat'] < today), 'status'] = 'overdue'
    data.to_csv("peminjaman.csv", index=False)

#================================================================================================
# MENU UTAMA DAN NAVIGASI
#================================================================================================

def dashboard(user):
    print(
"""
╔════════════════════════════════════╗
║       Labolatorium   KaKiQu        ║
║┌──────────────────────────────────┐║""")
    if user['role'] =="mahasiswa":
        print("║│  1. Daftar Alat dan Bahan        │║")
        print("║│  2. Barang Yang Sedang Dipinjam  │║")
        print("║│  3. Peminjaman Alat dan Bahan    │║")
        print("║│  4. Pengembalian Alat dan Bahan  │║")
        print("║│  5. History Peminjaman           │║")
        print("║│  6. Logout                       │║")
        print("║├──────────────────────────────────┤║")
        print(f"║│  Mahasiswa : {user['nama']}{' '*(20-len(user['nama']))}│║")
        print("║└──────────────────────────────────┘║")
    elif user['role'] == 'admin':
        print("║│  1. Daftar Alat dan Bahan        │║")
        print("║│  2. Update Alat dan Bahan        │║")
        print("║│  3. Peminjaman Alat dan Bahan    │║")
        print("║│  4. Pengembalian Alat dan Bahan  │║")
        print("║│  5. Barang Yang Sedang Dipinjam  │║")
        print("║│  6. History Peminjaman           │║")
        print("║│  7. Keluar                       │║")
        print("║├──────────────────────────────────┤║")
        print("║│            Menu Admin            │║")
        print("║└──────────────────────────────────┘║")
    print("╚════════════════════════════════════╝")


def pilih_dashboard(user):
    while True:
        if user['role'] == "mahasiswa":
            pilihan = input("Pilih Menu [1-6]: ")
            match pilihan:
                case "1":
                    menu_daftar_barang()
                case "2":
                    sedang_dipinjam(user)
                case "3":
                    menu_peminjaman(user)
                case "4":
                    menu_pengembalian(user)
                case "5":
                    menu_history(user)
                case "6":
                    log.logout()
                    break
                case _:
                    print("Pilihan Tidak Ada\n")
                    input("Tekan Enter untuk mencoba kembali.")
                    log.clear_alert(4)
                    continue
        
        elif user['role'] == "admin":
            pilihan = input("Pilih Menu [1-7]: ")
            match pilihan:
                case "1":
                    menu_daftar_barang()
                case "2":
                    menu_update_barang()
                case "3":
                    menu_peminjaman(user)
                case "4":
                    menu_pengembalian(user)
                case "5":
                    sedang_dipinjam(user)
                case "6":
                    history_admin()
                case "7":
                    log.logout()
                    break
                case _:
                    print("Pilihan Tidak Ada\n")
                    input("Tekan Enter untuk mencoba kembali.")
                    log.clear_alert(4)
                    continue
        break

#================================================================================================
# NAVIGASI SUB MENU
#================================================================================================

def menu_daftar_barang():
    while True:
        log.clear_terminal()
        print("==== Menu Data Barang ====")
        print(" [1] Daftar Alat")
        print(" [2] Daftar Bahan")
        print(" [3] Cari Alat")
        print(" [4] Cari Bahan")
        print(" [5] Kembali")
        print("-"*24)
        sub_pilihan = input("Pilih Menu [1/2/3/4]: ")
        match sub_pilihan:
            case "1":
                tampilan_daftar("alat.csv","Alat")
                print("-"*24)
            case "2":
                tampilan_daftar("bahan.csv","Bahan")
                print("-"*24)
            case "3":
                cari_barang("alat.csv","Alat")
            case "4":
                cari_barang("bahan.csv","Bahan")
            case "5":
                log.clear_terminal()
                return
            case _:
                print("Pilihan Tidak Ada\n")
                input("Tekan Enter untuk mencoba kembali.")
                log.clear_alert(4)
                continue
            
        input("\nTekan Enter untuk kembali ke Menu Utama.")
        log.clear_terminal()
        break


def menu_update_barang():
    while True:
        log.clear_terminal()
        print("=== Pilih Update Barang ===")
        print(" [1] Tambah Alat")
        print(" [2] Tambah Bahan")
        print(" [3] Edit Alat")
        print(" [4] Edit Bahan")
        print(" [5] Kembali")
        print("-"*24)
        sub_pilihan = input("Pilih Menu [1/2/3/4/5]: ")
        match sub_pilihan:
            case "1":
                tambah_barang("alat.csv","Alat")
            case "2":
                tambah_barang("bahan.csv","Bahan")
            case "3":
                sub_menu_update_barang('alat.csv','Alat')
                # tampilan_daftar("alat.csv","Alat")
                # edit_produk("alat.csv","Alat")
            case "4":
                sub_menu_update_barang('bahan.csv','Bahan')
                # tampilan_daftar("bahan.csv","Alat")
                # edit_produk("bahan.csv","Bahan")
            case "5":
                log.clear_terminal()
                return
            case _:
                print("Pilihan Tidak Ada\n")
                input("Tekan Enter untuk mencoba kembali.")
                log.clear_alert(4)
                continue

        # input("\nTekan Enter untuk kembali ke menu")
        # log.clear_terminal()
        # break


def sub_menu_update_barang(file, judul):
    while True:
        log.clear_terminal()
        print(f"=== Pilih Update {judul} ===")
        print(f" [1] Edit Nama {judul}")
        print(" [2] Edit Jenis")
        print(" [3] Edit Stok")
        print(" [4] Kembali")
        print("-"*24)
        sub_pilihan = input("Pilih Menu [1/2/3/4]: ")
        match sub_pilihan:
            case "1":
                tampilan_daftar(file,judul)
                edit_nama(file,judul)
            case "2":
                tampilan_daftar(file,judul)
                edit_jenis(file,judul)
            case "3":
                tampilan_daftar(file,judul)
                edit_stok(file,judul)
            case "4":
                log.clear_terminal()
                return
            case _:
                print("Pilihan Tidak Ada\n")
                input("Tekan Enter untuk mencoba kembali.")
                log.clear_alert(4)
                continue

        input("\nTekan Enter untuk kembali ke menu")
        log.clear_terminal()
        break


def menu_peminjaman(user):
    while True:
        log.clear_terminal()
        print("==== Menu Peminjaman ====")
        print(" [1] Pinjam Alat")
        print(" [2] Pinjam Bahan")
        print(" [3] Kembali")
        print("-"*24)
        sub_pilihan = input("Pilih Menu [1/2/3]: ")
        match sub_pilihan:
            case "1":
                tambah_pinjam("alat.csv","Alat",user)
            case "2":
                tambah_pinjam("bahan.csv","Bahan",user)
            case "3":
                log.clear_terminal()
                return
            case _:
                print("Pilihan Tidak Ada\n")
                input("Tekan Enter untuk mencoba kembali.")
                log.clear_alert(4)
                continue
        input("\nTekan Enter untuk kembali ke menu.")
        log.clear_terminal()
        break


def menu_pengembalian(user):
    while True:
        log.clear_terminal()
        print("==== Menu Pengembalian ====")
        print(" [1] Kembalikan Alat")
        print(" [2] Kembalikan Bahan")
        print(" [3] Kembali")
        print("-"*24)
        sub_pilihan = input("Pilih Menu [1/2]: ")
        match sub_pilihan:
            case "1":
                kembali_pinjam("alat.csv","Alat",user)
            case "2":
                kembali_pinjam("bahan.csv","Bahan",user)
            case "3":
                log.clear_terminal()
                return
            case _:
                print("Pilihan Tidak Ada\n")
                input("Tekan Enter untuk mencoba kembali.")
                log.clear_alert(4)
                continue
        input("\nTekan Enter untuk kembali ke menu.")
        log.clear_terminal()
        break


def menu_history(user):
    while True:
        log.clear_terminal()
        print("=== Cari History Peminjaman ===")
        print(" [1] History Peminjaman Alat")
        print(" [2] History Peminjaman Bahan")
        print(" [3] Kembali")
        print("-"*24)
        sub_pilihan = input("Pilih Menu [1/2]: ")
        match sub_pilihan:
            case "1":
                history_user("peminjaman.csv", user, 'Alat')
            case "2":
                history_user("peminjaman.csv", user, 'Bahan')
            case "3":
                log.clear_terminal()
                return
            case _:
                print("Pilihan Tidak Ada\n")
                input("Tekan Enter untuk mencoba kembali.")
                log.clear_alert(4)
                continue
        input("\nTekan Enter untuk kembali ke menu")
        log.clear_terminal()
        break

#================================================================================================
# KELOLA ALAT DAN BAHAN
#================================================================================================

def tampilan_daftar(file,judul):
     # Membaca file CSV ke dalam DataFrame
    log.clear_terminal()
    data = log.cek_file(file)
    print(f"======== Daftar {judul} ========")
    print(data.to_string(index=False)) 
    return data


def cari_barang(file,judul):
    log.clear_terminal()
    data = log.cek_file(file)

    print(f"\n==== Cari {judul} ====")
    nama_barang = input_barang(f"Nama {judul}: ")

    # Filter data berdasarkan input nama produk (case-insensitive)
    hasil_cari = data[data['nama'].str.lower().str.contains(nama_barang.lower())]
    
    print("\n=== Hasil Pencarian ===")

    if not hasil_cari.empty:
    # if len(hasil_cari)>0:
        print(hasil_cari[['id', 'nama', 'jenis', 'stok']].to_string(index=False))
        
        print("-"* (19 + hasil_cari['nama'].str.len().max()))      # cuma ngeprint tampilan, menyesuaikan panjang nama barang yang ditampilkan
    else:
        print("-"*23)
        print(f"{judul} tidak ditemukan")


def tambah_barang(file,judul):
    log.clear_terminal()
    # Membaca data dari produk.csv
    data = log.cek_file(file)
    if not data.empty:
    # if len(data)>0:
        # id_baru = data['id'].max() + 1
        id_baru = data.iloc[-1]["id"]+1
    else:
        id_baru = 1
        
    print(f"==== Tambah {judul} ====")
    while True:
        # Validasi: Cek apakah nama produk sudah ada
        nama_barang = input_barang(f"Masukkan nama {judul} baru: ")
        while nama_barang in data['nama'].str.lower().values:
            print(f"Nama {judul} sudah ada. Silakan gunakan nama lain.")
            input("Tekan Enter untuk mencoba kembali")
            log.clear_alert(3)
            nama_barang = input_barang(f"Masukkan nama {judul} baru: ")
        if judul == 'Alat':
            jenis = input_barang(f"Masukkan jenis {judul} [Fragile/Unfragile]: ")
            while jenis not in ['fragile','unfragile']:
                print(f"Jenis tidak valid. Jenis harus [Fragile/Unfragile]")
                input("Tekan Enter untuk mencoba kembali")
                log.clear_alert(3)
                jenis = input_barang(f"Masukkan jenis {judul} [Fragile/Unfragile]: ")
        elif judul == 'Bahan' :
            jenis = input_barang(f"Masukkan jenis {judul} [Padat,Cair,Gas]: ")
            while jenis not in ['padat','cair','gas']:
                print(f"Jenis tidak valid. Jenis harus [Padat/Cair/Gas]")
                input("Tekan Enter untuk mencoba kembali")
                log.clear_alert(3)
                jenis = input_barang(f"Masukkan jenis {judul} [Padat,Cair,Gas]: ")
        stok = input_int(f"Masukkan stok {judul}: ")
        
        # Membuat DataFrame produk baru
        produk_baru = pd.DataFrame([{
            "id": id_baru,
            "nama": nama_barang,
            "jenis": jenis, 
            "stok": stok,
            "dipinjam": 0,
        }])
        break

    while True:
        log.clear_terminal()
        print("\nRingkasan Barang:")
        print("-" * 24)
        print(f"ID {judul}\t:{id_baru}")
        print(f"Nama {judul}\t:{nama_barang}")
        print(f"Jenis\t\t:{jenis}")
        print(f"Stok\t\t:{stok}")
        print("-" * 24)
        print(" [1] Selasai")
        print(" [2] Ulangi")
        print(" [3] Batal")
        print("-" * 24)
        
        lanjutkan = input("Pilih Menu [1/2/3]: ")
        match lanjutkan:
            case "1":
                data_baru = pd.concat([data, produk_baru])
                data_baru.to_csv(file, index=False)
                log.clear_terminal()
                print(f"==== Registrasi {judul} Berhasil ====")
                print("-" * 24)
                print(f"ID {judul}:\t{id_baru}")
                print(f"Nama {judul}:\t{nama_barang}")
                print(f"Jenis:\t\t{jenis}")
                print(f"Stok:\t\t{stok}")
                print("-" * 24)
                input("Tekan Enter untuk kembali")
                return  # Menyelesaikan fungsi setelah pinjam berhasil
            
            case "2":
                tambah_barang(file,judul)
                return
            
            case "3":
                print("=" * 24)
                print("==== Operasi Dibatalkan ====")
                input("Tekan Enter untuk kembali")
                break  # Keluar dari fungsi jika pinjam dibatalkan
            
            case _:
                print("Pilihan Tidak Ada")
                input("Tekan Enter untuk mencoba kembali")
                log.clear_alert(3)
                continue
            

#================================================================================================
# FITUR EDIT UTAMA [Tidak Dipakai]
#================================================================================================

def edit_produk(file,judul):
    data = log.cek_file(file)
    while True:
            id_barang = input(f"Masukkan ID {judul} yang ingin diedit: ").strip()
        
            id_barang = int(id_barang)
            # Cek apakah ID produk ada dalam data
            if id_barang in data['id'].values:
                # Mengambil baris produk berdasarkan ID
                hasil_cari = data[data['id'] == id_barang]
                print(f"\nData {judul} yang akan diedit:")
                print("="*30)
                print(hasil_cari[['id', 'nama','jenis', 'stok']].to_string(index=False))
                print("="*30)

                # Meminta input untuk memperbarui nama barang
                nama_baru = input_barang(f"Nama {judul} baru: ")
                data.loc[data['id'] == id_barang, 'nama'] = nama_baru

                # Meminta input untuk memperbarui jenis barang
                if judul == 'Alat':
                    jenis_baru = input_barang(f"Jenis {judul} baru [Fragile/Unfragile]: ").lower()
                    while jenis_baru not in ['fragile','unfragile']:
                        print(f"Jenis tidak valid. Jenis harus [Fragile/Unfragile]")
                        input("Tekan Enter untuk mencoba kembali")
                        log.clear_alert(3)
                        jenis_baru = input_barang(f"Masukkan jenis {judul} [Fragile/Unfragile]: ")
                    data.loc[data['id'] == id_barang, 'jenis'] = jenis_baru

                elif judul == 'Bahan':
                    jenis_baru = input_barang(f"Jenis {judul} baru [Padat,Cair,Gas]: ")
                    while jenis_baru not in ['padat','cair','gas']:
                        print(f"Jenis tidak valid. Jenis harus [Padat/Cair/Gas]")
                        input("Tekan Enter untuk mencoba kembali")
                        log.clear_alert(3)
                        jenis_baru = input_barang(f"Masukkan jenis {judul} [Padat,Cair,Gas]: ")
                    data.loc[data['id'] == id_barang, 'jenis'] = jenis_baru

                # Meminta input untuk memperbarui stok barang
                stok_baru = input_int(f"Stok {judul} baru: ")
                data.loc[data['id'] == id_barang, 'stok'] = stok_baru

                # Menyimpan data yang telah diperbarui ke produk.csv
                data.to_csv(file, index=False)
                print("\nData produk berhasil diperbarui:")
                print("="*30)

                # Menampilkan data yang telah diperbarui 
                data = log.cek_file(file)
                hasil_cari = data[data['id'] == id_barang]
                print(hasil_cari[['id', 'nama','jenis', 'stok']].to_string(index=False))
                print("="*30)
                break

            else:
                print(f"ID {judul} tidak ditemukan.")
                input("Tekan Enter untuk mencoba kembali.")
                log.clear_alert(3)

#================================================================================================
# FITUR SUB EDIT
#================================================================================================

def edit_nama(file,judul):
    data = log.cek_file(file)
    print("="*30)

    while True:
        id_barang = input_int(f"Masukkan ID {judul} yang ingin diedit: ")
        # Cek apakah ID produk ada dalam data

        if id_barang in data['id'].values:
            # Mengambil baris produk berdasarkan ID
            hasil_cari = data[data['id'] == id_barang]
            print(f"\nData {judul} yang akan diedit:")
            print("="*30)
            print(hasil_cari[['id', 'nama','jenis', 'stok']].to_string(index=False))
            print("="*30)

            # Meminta input untuk memperbarui nama barang
            nama_baru = input_barang(f"Nama {judul} baru: ")
            data.loc[data['id'] == id_barang, 'nama'] = nama_baru

            # Menyimpan data yang telah diperbarui ke produk.csv
            data.to_csv(file, index=False)
            print("\nData produk berhasil diperbarui:")
            print("="*30)

            # Menampilkan data yang telah diperbarui 
            data = log.cek_file(file)
            hasil_cari = data[data['id'] == id_barang]
            print(hasil_cari[['id', 'nama','jenis', 'stok']].to_string(index=False))
            print("="*30)
            break

        else:
            print(f"ID {judul} tidak ditemukan.")
            input("Tekan Enter untuk mencoba kembali.")
            log.clear_alert(3)


def edit_jenis(file,judul):
    data = log.cek_file(file)
    print("="*30)

    while True:
        id_barang = input_int(f"Masukkan ID {judul} yang ingin diedit: ")
        # Cek apakah ID produk ada dalam data

        if id_barang in data['id'].values:
            # Mengambil baris produk berdasarkan ID
            hasil_cari = data[data['id'] == id_barang]
            print(f"\nData {judul} yang akan diedit:")
            print("="*30)
            print(hasil_cari[['id', 'nama','jenis', 'stok']].to_string(index=False))
            print("="*30)

            # Meminta input untuk memperbarui jenis barang
            if judul == 'Alat':
                jenis_baru = input_barang(f"Jenis {judul} baru [Fragile/Unfragile]: ")
                while jenis_baru not in ['fragile','unfragile']:
                    print(f"Jenis tidak valid. Jenis harus [Fragile/Unfragile]")
                    input("Tekan Enter untuk mencoba kembali")
                    log.clear_alert(3)
                    jenis_baru = input_barang(f"Masukkan jenis {judul} [Fragile/Unfragile]: ")
                data.loc[data['id'] == id_barang, 'jenis'] = jenis_baru
            
            elif judul == 'Bahan':
                jenis_baru = input_barang(f"Jenis {judul} baru [Padat,Cair,Gas]: ")
                while jenis_baru not in ['padat','cair','gas']:
                    print(f"Jenis tidak valid. Jenis harus [Padat/Cair/Gas]")
                    input("Tekan Enter untuk mencoba kembali")
                    log.clear_alert(3)
                    jenis_baru = input_barang(f"Masukkan jenis {judul} [Padat,Cair,Gas]: ")
                data.loc[data['id'] == id_barang, 'jenis'] = jenis_baru



            # Menyimpan data yang telah diperbarui ke produk.csv
            data.to_csv(file, index=False)
            print("\nData produk berhasil diperbarui:")
            print("="*30)

            # Menampilkan data yang telah diperbarui 
            data = log.cek_file(file)
            hasil_cari = data[data['id'] == id_barang]
            print(hasil_cari[['id', 'nama','jenis', 'stok']].to_string(index=False))
            print("="*30)
            break

        else:
            print(f"ID {judul} tidak ditemukan.")
            input("Tekan Enter untuk mencoba kembali.")
            log.clear_alert(3)


def edit_stok(file,judul):
    data = log.cek_file(file)
    print("="*30)

    while True:
        id_barang = input_int(f"Masukkan ID {judul} yang ingin diedit: ")
        # Cek apakah ID produk ada dalam data

        if id_barang in data['id'].values:
            # Mengambil baris produk berdasarkan ID
            hasil_cari = data[data['id'] == id_barang]
            print(f"\nData {judul} yang akan diedit:")
            print("="*30)
            print(hasil_cari[['id', 'nama','jenis', 'stok']].to_string(index=False))
            print("="*30)

            # Meminta input untuk memperbarui stok barang
            stok_baru = input_int(f"Stok {judul} baru: ")
            data.loc[data['id'] == id_barang, 'stok'] = stok_baru

            # Menyimpan data yang telah diperbarui ke produk.csv
            data.to_csv(file, index=False)
            print("\nData produk berhasil diperbarui:")
            print("="*30)

            # Menampilkan data yang telah diperbarui 
            data = log.cek_file(file)
            hasil_cari = data[data['id'] == id_barang]
            print(hasil_cari[['id', 'nama','jenis', 'stok']].to_string(index=False))
            print("="*30)
            break

        else:
            print(f"ID {judul} tidak ditemukan.")
            input("Tekan Enter untuk mencoba kembali.")
            log.clear_alert(3)

#================================================================================================
# KELOLA UPDATE STOK PEMINJAMAN DAN PENGEMBALIAN OTOMATIS
#================================================================================================

def pinjam_stok(file,judul,id_barang, jumlah_pinjam):
    barang = tampilan_daftar(file,judul)
    # Mengurangi stok sesuai jumlah pinjam
    barang.loc[barang['id'] == id_barang, 'stok'] -= jumlah_pinjam
    barang.loc[barang['id'] == id_barang, 'dipinjam'] += jumlah_pinjam
    barang.to_csv(file, index=False)


def kembali_stok(file,id_barang, jumlah_pinjam):
    barang = log.cek_file(file)
    # Mengurangi stok sesuai jumlah pinjam
    barang.loc[barang['id'] == id_barang, 'stok'] += jumlah_pinjam
    barang.loc[barang['id'] == id_barang, 'dipinjam'] -= jumlah_pinjam
    barang.to_csv(file, index=False)

#================================================================================================
# KELOLA PEMINJAMAN DAN PENGEMBALIAN
#================================================================================================

def tambah_pinjam(file, judul, user):
    barang = tampilan_daftar(file, judul)
    data = log.cek_file("peminjaman.csv")

    if not data.empty:
    # if len(data) > 0:
        id_pinjam = data.iloc[-1]["id"] + 1
    else:
        id_pinjam = 1

    print("=" * 32)
    if user['role'] == 'admin':
        # Admin dapat memasukkan nama dan NIM untuk pengguna
        user['nama'] = log.input_nama("Nama Peminjam: ")
        user['nim'] = log.input_nim("NIM: ")
        log.clear_alert(2)

    while True:
        # Memilih ID barang yang ingin dipinjam
        id_barang = input_int(f"Masukkan ID {judul} yang ingin dipinjam: ")
        if id_barang not in barang['id'].values:
            print(f"ID {judul} tidak ditemukan.")
            input("Tekan Enter untuk mencoba kembali.")
            log.clear_alert(3)
            continue
        barang_terpilih = barang[barang['id'] == id_barang].iloc[0]
        item = barang_terpilih['nama']
        item_jenis = barang_terpilih['jenis']
        item_stok = barang_terpilih['stok']
        if item_stok == 0:
            print(f"Stok {item} sedang kosong.")
            input("Tekan Enter untuk mencoba kembali.")
            log.clear_alert(3)
        else:
            break
        
    while True: 
        # Meminta jumlah yang ingin dipinjam
        jml = input_int(f"Masukkan jumlah {judul} yang ingin dipinjam: ")
        if jml < 1:
            print("Minimal pinjam 1.")
            input("Tekan Enter untuk mencoba lagi.")
            log.clear_alert(3)
        elif jml > item_stok:
            print("Jumlah melebihi stok yang tersedia.")
            input("Tekan Enter untuk mencoba lagi.")
            log.clear_alert(3)
        else:
            break
            
    while True:
        tenggat_hari = input_int("Masukkan lama waktu pinjam (dalam hari): ")
        if tenggat_hari < 1 :
            print("Minimal lama pinjam adalah 1 hari.")
            input("Tekan Enter untuk mencoba lagi.")
            log.clear_alert(3)
        else:
            tgl_pinjam = date.today()
            tenggat = tgl_pinjam + timedelta(days=tenggat_hari)
            break

    # Membuat dictionary untuk menyimpan data pinjaman
    data_pinjam = {
        "id": id_pinjam,               # ID pinjaman yang dihasilkan sebelumnya
        "nim": user['nim'],                    # NIM pengguna yang meminjam
        "nama": user['nama'],                  # Nama pengguna
        "kategori": judul.lower(),     # Kategori barang (judul yang diubah menjadi huruf kecil)
        "id_barang": id_barang,        # ID barang yang dipinjam
        "barang": item,                # Nama barang yang dipinjam
        "jenis": item_jenis,           # Jenis barang yang dipinjam
        "jml_pinjam": jml,             # Jumlah barang yang dipinjam
        "jml_kembali": 0,            # Jumlah barang yang kembali (0 karena masih dipinjam)
        "tgl_pinjam": tgl_pinjam,      # Tanggal pinjam
        "tgl_kembali": "-",            # Tanggal kembali (belum ada karena masih dipinjam)
        "tenggat": tenggat,            # Tenggat waktu pengembalian
        "status": "dipinjam"           # Status barang saat ini, yaitu 'dipinjam'
    }

    # Membuat DataFrame dengan data pinjaman yang telah disiapkan
    df = pd.DataFrame([data_pinjam])

    while True:
        log.clear_terminal()
        print("\nRingkasan Barang:")
        print("-" * 24)
        print(f"Barang\t:{item}")
        print(f"Jenis\t:{item_jenis}")
        print(f"Jumlah\t:{jml}")
        print(f"\nTanggal Pinjam\t:{tgl_pinjam}")
        print(f"Waktu Tenggat\t:{tenggat}")
        print("-" * 24)
        print(" [1] Ganti Barang")
        print(" [2] Edit Jumlah")
        print(" [3] Edit Lama Pinjam ")
        print(" [4] Selesai")
        print(" [5] Batal")
        print("-" * 24)
        
        lanjutkan = input("Pilih Menu [1/2/3/4/5]: ")
        match lanjutkan:
            case "1":
                while True:
                    log.clear_terminal()
                    tampilan_daftar(file, judul)
                    print("=" * 32)
                    # Memilih ID barang yang ingin dipinjam
                    id_barang_baru = input_int(f"Masukkan ID {judul} yang ingin dipinjam: ")
                    if id_barang_baru not in barang['id'].values:
                        print(f"ID {judul} tidak ditemukan.")
                        input("Tekan Enter untuk mencoba kembali.")
                        log.clear_alert(3)
                        continue
                    barang_terpilih = barang[barang['id'] == id_barang_baru].iloc[0]
                    item = barang_terpilih['nama']
                    item_jenis = barang_terpilih['jenis']
                    item_stok = barang_terpilih['stok']
                    if item_stok == 0:
                        print(f"Stok {item} sedang kosong.")
                        input("Tekan Enter untuk mencoba kembali.")
                        log.clear_alert(3)
                    elif item_stok < jml:
                        print(f"Jumlah pinjaman melebihi Stok yang tersedia.")
                        input("Tekan Enter untuk mencoba kembali.")
                        log.clear_alert(3)
                    else:
                        id_barang = id_barang_baru
                        df["id_barang"] = id_barang
                        df["barang"] = item
                        df["jenis"] = item_jenis
                        print("-"*24)
                        print("Barang Berhasil Diganti")
                        input("Tekan Enter untuk melanjutkan")
                        log.clear_terminal()
                        break

            case "2":
                while True:
                    # Meminta jumlah baru yang ingin dipinjam
                    log.clear_terminal()
                    # print(barang_terpilih[["nama","stok"]].to_string())
                    print("Nama Barang :",barang_terpilih[["nama"]].to_string(index=False))
                    print("Stok Tersedia :",barang_terpilih[["stok"]].to_string(index=False))
                    print("Jumlah Pesanan Anda :",jml)
                    print("=" * 32)
                    jml_baru = input_int(f"Masukkan jumlah baru : ")
                    if jml_baru < 1:
                        print("Minimal pinjam 1.")
                        input("Tekan Enter untuk mencoba lagi.")
                        log.clear_alert(3)
                    elif jml_baru > item_stok:
                        print("Jumlah melebihi stok yang tersedia.")
                        input("Tekan Enter untuk mencoba lagi.")
                        log.clear_alert(3)
                    else:
                        df["jml_pinjam"] = jml_baru
                        print("-"*24)
                        print("Jumlah Barang Berhasil Diganti")
                        input("Tekan Enter untuk melanjutkan")
                        log.clear_terminal()
                        break

            case "3":
                log.clear_terminal()
                print(f"Hari ini : {date.today()}")
                print(f"Deadline Sebelumnya : {tenggat}")
                while True:
                    tenggat_hari = input_int("Lama waktu pinjam (dalam hari): ")
                    if tenggat_hari <1:
                        print("Minimal lama pinjam adalah 1 hari.")
                        input("Tekan Enter untuk mencoba lagi.")
                        log.clear_alert(3)
                    else:
                        tenggat = tgl_pinjam + timedelta(days=tenggat_hari)   
                        df['tenggat'] = tenggat
                        print("-"*24)
                        print("Lama Pinjam Berhasil Diganti")
                        input("Tekan Enter untuk melanjutkan")
                        log.clear_terminal()
                        break

            case "4":
                pinjam_stok(file, judul, id_barang, jml)
                data_baru = pd.concat([data, df])
                data_baru.to_csv("peminjaman.csv", index=False)
                log.clear_terminal()
                print("==== Peminjaman Berhasil ====")
                print("Bukti Peminjaman:")
                print("-" * 24)
                print(f"Nama:\t{user['nama']}")
                print(f"NIM:\t{user['nim']}\n")
                print(f"Barang:\t{item}")
                print(f"Jenis:\t{item_jenis}")
                print(f"Jumlah:\t{jml}")
                print(f"\nTanggal Pinjam:\t{tgl_pinjam}")
                print(f"Waktu Tenggat:\t{tenggat}")
                print("-" * 24)
                return  # Menyelesaikan fungsi setelah pinjam berhasil
            
            case "5":
                print("=" * 24)
                print("==== Peminjaman Dibatalkan ====")
                return  # Keluar dari fungsi jika pinjam dibatalkan
            
            case _:
                print("Pilihan Tidak Ada")
                input("Tekan Enter untuk mencoba kembali")
                log.clear_alert(3)
                continue
        

def kembali_pinjam(file, judul, user):
    # Baca data peminjaman
    data = log.cek_file("peminjaman.csv")
    kategori = judul.lower()

    # Filter data peminjaman berdasarkan kategori dan status yang relevan
    filter_kondisi = (
        (data['kategori'] == kategori) &
        ((data['status'] == 'dipinjam') | (data['status'] == 'overdue'))
    )
    
    if user['role'] == 'admin':
        pinjaman = data[filter_kondisi]
        header =['id', 'nama', 'nim', 'barang', 'jml_pinjam', 'tgl_pinjam']

    elif user['role'] == 'mahasiswa':
        pinjaman = data[filter_kondisi & (data['nim'] == user['nim'])]
        header = ['id', 'barang', 'jml_pinjam', 'tgl_pinjam', 'tenggat'] 

    
    # Tampilkan data pinjaman yang relevan
    if pinjaman.empty:
        print(f"Tidak ada {judul} yang sedang dipinjam.")
        return
    
    print(f"\n======== {judul} yang Sedang Dipinjam ========")
    # if user['role'] == 'mahasiswa' :
        # header = ['id', 'barang', 'jml_pinjam', 'tgl_pinjam', 'tenggat'] 
    # elif user['role'] == 'admin' :
        # header =['id', 'nama', 'nim', 'barang', 'jml_pinjam', 'tgl_pinjam']

    print(pinjaman[header].to_string(index=False))
    print("-" * (40 + pinjaman['barang'].str.len().max()))

    # Memilih ID pinjaman yang ingin dikembalikan
    id_pinjam = input_int(f"Masukkan ID {judul} yang ingin dikembalikan: ")
    if id_pinjam not in pinjaman['id'].values:
        print(f"ID {judul} tidak valid.")
        return

    # Mengambil baris data peminjaman yang dipilih
    id_terpilih = pinjaman.loc[pinjaman['id'] == id_pinjam]
    print(f"\n==== Data {judul} yang akan dikembalikan ====")
    print(id_terpilih[['id', 'barang', 'jml_pinjam', 'jml_kembali']].to_string(index=False))
    print("-" * (40 + pinjaman['barang'].str.len().max()))

    # Meminta jumlah barang yang dikembalikan
    while True:
        jml_kembali = input_int(f"Banyak {judul} yang dikembalikan: ")
        total_kembali = jml_kembali + id_terpilih.iloc[0]['jml_kembali']
        
        if total_kembali > id_terpilih.iloc[0]["jml_pinjam"]:
            print("Barang yang dikembalikan melebihi jumlah pinjam.")
            input("Tekan Enter untuk melanjutkan")
            log.clear_alert(3)

        # elif jml_kembali < 1:
        #     print("Minimal barang yang dikembalikan adalah 1.")
        #     input("Tekan Enter untuk melanjutkan")
        #     log.clear_alert(3)

        else:

            # Update jumlah barang yang dikembalikan
            data.loc[data['id'] == id_pinjam, 'jml_kembali'] = total_kembali

            # Perbarui status peminjaman
            data.loc[data['id'] == id_pinjam, 'status'] = 'selesai' if total_kembali == id_terpilih.iloc[0]["jml_pinjam"] else 'dipinjam'
            break

    # Update stok barang yang dikembalikan dan tanggal kembali
    kembali_stok(file, id_terpilih.iloc[0]['id_barang'], jml_kembali)
    data.loc[data['id'] == id_pinjam, 'tgl_kembali'] = date.today()

    # Simpan perubahan ke file peminjaman.csv
    data.to_csv("peminjaman.csv", index=False)
    print(f"\n{judul} berhasil dikembalikan dan stok telah diperbarui.")


def sedang_dipinjam(user):
    log.clear_terminal()
    data = log.cek_file('peminjaman.csv')

    filter_kondisi = (
        (data['status'] == 'dipinjam') | (data['status'] == 'overdue'))
    
    if user['role'] == 'admin':
        pinjaman = data[filter_kondisi]
    elif user['role'] == 'mahasiswa':
        pinjaman = data[filter_kondisi & (data['nim'] == user['nim'])]

    if pinjaman.empty:
       print(f"Tidak ada barang yang sedang dipinjam.")
       input("Tekan Enter untuk kembali")
       log.clear_terminal()
       return
    

    print(f"======== Barang yang Sedang Dipinjam ========")
    if user['role'] == 'mahasiswa' :
        header = ['id', 'barang', 'jml_pinjam', 'tgl_pinjam', 'tenggat'] 
    elif user['role'] == 'admin' :
        header =['id', 'nama', 'nim', 'barang', 'jml_pinjam', 'tgl_pinjam']

    print(pinjaman[header].to_string(index=False))
    print("-" * (40 + pinjaman['barang'].str.len().max()))

#================================================================================================
# RIWAYAT TRANSAKSI
#================================================================================================

def history_user(file, user, judul):
    log.clear_terminal()
    data = log.cek_file(file)
    
    kategori = judul.lower()
    print(f"================ Riwayat Peminjaman {judul} ================")
    
    hasil_cari = data[(data['nim'] == user['nim']) & (data['kategori'] == kategori)]
    
    if not hasil_cari.empty:
    # if len(hasil_cari) > 0:
        print(hasil_cari[['id', 'barang', 'jml_pinjam','jml_kembali', 'tgl_pinjam', 'tenggat', 'status']].to_string(index=False))
        print("-" * (52 + hasil_cari['nama'].str.len().max()))
    else:
        print("-" * 52)
        print("Tidak ada riwayat peminjaman ditemukan.")

def history_admin():
    log.clear_terminal()
    data = log.cek_file('peminjaman.csv')

    print(f"================ Riwayat Peminjaman ================")
    if len(data) > 0:
        print(data[['id', 'barang', 'jml_pinjam','jml_kembali', 'nama','nim','tgl_pinjam', 'status']].to_string(index=False))
        print("-" * (52 + data['nama'].str.len().max()))
    else:
        print("-" * 52)
        print("Tidak ada riwayat peminjaman ditemukan.")

    input("Tekan Enter untuk kembali ke menu")
    log.clear_terminal()

