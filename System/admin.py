import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'kasir',
    password = 'yes',
    database = 'kasir_database'
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM produk")
result_produk = mycursor.fetchall()
for ip in result_produk:
    rp = ip

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM keranjang")
result_keranjang = mycursor.fetchall()
for ik in result_keranjang:
    rk = ik

nama = "Nama Barang"
harga = "harga"
jumlah = "Stok"

def option_admin():
    while True:
        print("""
            1. Tambah / Buat Stok
            2. Update Stok
            3. Hapus Stok
            """)

        while True:
            user_option = input("PIlih Tindakan menu admin: ").lower()
            print("Tekan 5 untuk keluar dari menu admin")
            match user_option:
                case "1":
                    create()
                case "2":
                    update()
                case "3":
                    delete()
                case "5":
                    return
def create():
    print("\n"+"="*53)
    print(f"{nama:20} | {harga:20} | {jumlah:5}")
    print("-"*53)

    for i in result_produk:
        s = i
        print("{:<20} | {:<20} | {:<5}".format(i[1], i[2], i[3]))
    print("Masukkan Informasi Stok Barang Yang Ingin Ditambahkan")
    while True:
        barang_inp = input("Nama barang : ").lower()

        is_barang_exist = False
        for row in result_produk:
            if barang_inp == row[1]:
                is_barang_exist = True
                break

        if is_barang_exist:
            print("NAMA BARANG SUDAH ADA, HARGA BARANG DAN JUMLAH BARANG AKAN DI UPDATE")
            update_exist(index=barang_inp)
            return
        else:
            break
    while True:
        try:
            harga_inp = int(input("harga barang : "))
            break
        except:
            print("masukkan angka yang benar")
    while True:
        try:
            jumlah_inp = int(input("Jumlah barang : "))
            break
        except:
            print("masukkan angka yang benar")
              
    try:
        sql = 'INSERT INTO produk(nama_barang,harga,jumlah) VALUES (%s,%s,%s)'
        val = (barang_inp,harga_inp,jumlah_inp)
        mycursor.execute(sql,val)
        mydb.commit()
        print("Berhasil Memasukkan barang di dalam stok")
    except mysql.connector.errors.DataError:
        print("Tidak boleh ada angka minus di Harga dan Jumlah")
        mydb.rollback()
    except:
        print("Gagal menambah barang")
        mydb.rollback()

def delete():
    print("\n"+"="*53)
    print(f"{nama:20} | {harga:20} | {jumlah:5}")
    print("-"*53)

    for i in result_produk:
        s = i
        print("{:<20} | {:<20} | {:<5}".format(i[1], i[2], i[3]))

    while True:
        user_input2 = input("Pilih Stok Barang Yang Ingin Di Hapus : ").lower()

        is_name_exist = False
        for iine in result_produk:
            if user_input2 == iine[1]:
                is_name_exist = True

        if is_name_exist:
            break
        else:
            print("Masukkan nama barang yang benar")
    while True:
        try:
            sql = 'SELECT id FROM produk WHERE nama_barang = %s'
            val = (user_input2,)
            mycursor.execute(sql,val)
            result2 = mycursor.fetchall()
            for i in result2:
                sql_keranjang = 'DELETE FROM keranjang WHERE id_keranjang = %s'
                val_keranjang = (i[0],)
                mycursor.execute(sql_keranjang,val_keranjang)
                mydb.commit()

                sql_produk = 'DELETE FROM produk WHERE id = %s'
                val_produk = (i[0],)
                mycursor.execute(sql_produk,val_produk)
                mydb.commit()
                print("Stok Berhasil di hapus")
                return
        except mysql.connector.errors.ProgrammingError:
            print("Nama Barang Tidak ada di dalam stok")
            mydb.rollback()
        except:
            print("gagal menghapus stok")
            mydb.rollback()

def update():
    print("\n"+"="*53)
    print(f"{nama:20} | {harga:20} | {jumlah:5}")
    print("-"*53)

    for i in result_produk:
        s = i
        print("{:<20} | {:<20} | {:<5}".format(i[1], i[2], i[3]))
    print("Masukkan nama Barang Yang Ingin Diupdate")
    while True:
        barang_inp_up = input("Nama Barang : ").lower()

        is_barang_exist = False
        for ibne in result_produk:
            if barang_inp_up == ibne[1]:
                is_barang_exist = True
        try:
            if is_barang_exist:
                break
            else:
                print("Nama Barang tidak ada di dalam stok")
        except UnboundLocalError:
            print("STOK BARANG KOSONG ISI STOK BARANG TERLEBIH DAHULU UNTUK UPDATE")

    while True:
        try:
            harga_inp_up = int(input("harga barang : "))
            break
        except:
            print("masukkan angka yang benar")

    while True:
        try:
            jumlah_inp_up = int(input("Jumlah barang : "))
            break
        except:
            print("masukkan angka yang benar")

    mycursor.execute('SELECT * FROM produk WHERE nama_barang = %s',(barang_inp_up,))
    result_up_ex = mycursor.fetchall()
    for irux in result_up_ex:
        rrux = irux
    
    try:
        total1 = rrux[3] + jumlah_inp_up
        sql_up_br_harga = 'UPDATE produk SET harga = %s WHERE id = %s'
        val_up_br_harga = (harga_inp_up,rrux[0])
        mycursor.execute(sql_up_br_harga,val_up_br_harga)
        mydb.commit()
        sql_up_br_jumlah = 'UPDATE produk SET jumlah = %s WHERE id = %s'
        val_up_br_jumlah = (total1,rrux[0])
        mycursor.execute(sql_up_br_jumlah,val_up_br_jumlah)
        mydb.commit()
        print("Berhasil Update Stok dan harga")
    except:
        print("Gagal update data")
        mydb.rollback()

def update_exist(**kawrgs):
    barang_inp_up = kawrgs["index"]
    while True:
        try:
            harga_inp_up = int(input("harga barang baru : "))
            break
        except:
            print("masukkan angka yang benar")
    while True:
        try:
            jumlah_inp_up = int(input("Jumlah barang baru : "))
            break
        except:
            print("masukkan angka yang benar")
    mycursor.execute('SELECT * FROM produk WHERE nama_barang = %s',(barang_inp_up,))
    result_up_ex = mycursor.fetchall()
    for irux in result_up_ex:
        rrux = irux
    try:
        total5 = rrux[3] + jumlah_inp_up
        sql_up_br_harga = 'UPDATE produk SET harga = %s WHERE id = %s'
        val_up_br_harga = (harga_inp_up,rrux[0])
        mycursor.execute(sql_up_br_harga,val_up_br_harga)
        mydb.commit()
        sql_up_br_jumlah = 'UPDATE produk SET jumlah = %s WHERE id = %s'
        val_up_br_jumlah = (total5,rrux[0])
        mycursor.execute(sql_up_br_jumlah,val_up_br_jumlah)
        mydb.commit()
        print("Berhasil Update Stok dan harga")
    except:
        print("Gagal update data")
        mydb.rollback()
