import os
import Loginreg as Loginreg

check_os = os.name
match check_os:
    case "posix": os.system("clear")
    case "nt": os.system("cls")

def login_wallet():
    while True:

        print("====Login Terlebih Dahulu Untuk Melanjutkan=====")
        print("=======Masukkan Informasi Login Anda=======")
        print("""
        
        1. Login
        2. Registrasi
        3. Kembali
        
        """)
        while True:
            user_input = input("Pilih tindakan : ")

            if user_input in ["login","Login","1"]:
                Loginreg.login()
                break
            elif user_input in ["registrasi","Registrasi","2"]:
                Loginreg.registrasi()
                break
            elif user_input in ["3"]:
                return
            else:
                print("Masukkan pilihan yang benar")

