import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'kasir',
    password = 'yes',
    database = 'kasir_database'
)

mycursor = mydb.cursor()

def registrasi():
    while True:
        print("Masukkan infomasi pendaftaran ")
        em = input("Masukkan Username : ").lower()
        ps = input("Masukkan Password : ")
        try:
            sql = 'INSERT INTO username (username_akun,password_akun) VALUES (%s,%s)'
            val = (em,ps)
            mycursor.execute(sql,val)
            mydb.commit()
            print("Akun Telah Berhasil dibuat")
            break
        except mysql.connector.Error:
                print("Username sudah ada dalam database.")
                mydb.rollback()
        except:
            print("Masukkan infomasi registrasi dengan benar")
            mydb.rollback()

    while True:
        ex = input("Ketik (Y) Untuk melanjutkan ke wallet : ")
        if ex in ["y","Y"]:
            break
    