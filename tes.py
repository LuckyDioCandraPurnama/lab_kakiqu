import pandas as pd
# import login

def login():
    data = pd.read_csv("penggunas.csv")

    usernm = input("masukan username: ")

    pw = input("masukan password: ")

    user = data[
        (data['username'] == usernm) &
        (data['password'] == pw)]
    
    if not user.empty :
        # role = user.iloc[0]['role']        
        print("Login Berhasil")
        print(f"Selamat Datang {usernm}")

        return  
    else:
        print("Login Gagal")

def register():
    # data = login.cek_file("user.csv")
    data = pd.read_csv("penggunas.csv")

    print("=====PENDAFTARAN AKUN=====")
    usernm = input("masukan username: ")
    pw = input("masukan password: ")
    nama = input("masukan nama: ")
    nim = input("masukan NIM: ")

    new_user = pd.DataFrame([{
            'username' : usernm,
            'password' : pw,
            'nama' : nama,
            'nim' : nim,
            'role' : 'mahasiswa'
        }])

    hasil_tambah = pd.concat([data,new_user])
    hasil_tambah.to_csv("niko.csv", index=False)
    print("Sukses Sign Up")

register()
login()

# if fajar == 0 :
#     print(f"Belajar lagi {ayo}")

# nama = "fajar"
# umur = 18
# nim = 54

# data = pd.DataFrame([{
#     "nama" : nama, 
#     "umur" : umur, 
#     "nim" : nim, 
# }])

# print(data)
# print(data.to_string(index=False))