import login as log
# import db_randika as db
import dashboard as db

def main():
    db.update_status()
    while True:
        log.menu_login()
        pilihan = input("Pilih Menu [1-3]: ")
        match pilihan:
            case "1":
                user = log.login()
                while log.login_status:
                    db.dashboard(user)
                    db.pilih_dashboard(user)
            case "2":
                log.register()
            case "3":
                print("Terima Kasih")
                break
            case _: 
                print("Pilihan tidak ada")
                input("Tekan Enter untuk mencoba kembali")
                log.clear_alert(3)


main()
