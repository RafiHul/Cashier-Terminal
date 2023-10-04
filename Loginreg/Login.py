import mysql.connector
import wallet

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'kasir',
    password = 'yes',
    database = 'kasir_database'
)

mycursor = mydb.cursor()

def login():
    t = 0
    while True:
        print("Masukkan infomasi login anda (Tidak Bisa memenukan akun anda ? tekan 2 untuk registrasi / daftar)")
        inp = input("Masukkan Username : ").lower()
        if inp == "2":
            registrasi()
        ps = input("Masukkan Password : ")

        sql = 'SELECT * FROM username WHERE username_akun = %s AND password_akun = %s'
        val = (inp,ps)
        mycursor.execute(sql,val)
        result = mycursor.fetchall()
        for i in result:
            t += 1
        if t == 1:
            print("Anda Berhasil Login")
            wallet.display_wallet(username_wallet=inp)
            return
        else:
            print("Password atau Email Invalid")

    while True:
        ex = input("Ketik (Y) Untuk melanjutkan ke wallet : ")
        if ex in ["y","Y"]:
            break