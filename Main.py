import os
import System as System

if __name__ == "__main__":
    check_os = os.name

    match check_os:
        case "posix": os.system("clear")
        case "nt": os.system("cls")

while(True):
    match check_os:
        case "posix": os.system("clear")
        case "nt": os.system("cls")

    print("======SELAMAT DATANG DI APLIKASI KASIR=======")
    print("""

        1. Belanja Barang
        2. Menu Admin

    """)
    while True:
        user_option = input("PIlih Tindakan : ").lower()
        match user_option:
            case "1":
                System.belanja()
                break
            case "2":
                System.option_admin()
                break
            case "5":
                System.login_wallet()
                break