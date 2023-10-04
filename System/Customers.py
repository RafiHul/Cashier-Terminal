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
            
def belanja():
    print("Silahkan pilih barang yang anda mau")
    nama = "Nama Barang"
    harga = "harga"
    jumlah = "Stok"

    print("\n"+"="*53)
    print(f"{nama:20} | {harga:20} | {jumlah:5}")
    print("-"*53)

    mycursor.execute("SELECT nama_barang,harga,jumlah FROM produk")
    result = mycursor.fetchall()

    for i in result:
        print("{:<20} | {:<20} | {:<5}".format(i[0], i[1], i[2]))

    while True:
        user_belanja_barang_inp = input("Pilih Produk : ").lower()
        
        is_user_belanja_exist = False
        for iiube in result_produk:
            if user_belanja_barang_inp == iiube[1]:
                is_user_belanja_exist = True

        if is_user_belanja_exist:
            break
        else:
            print("Nama produk tidak ada di dalam stok")
    while True:
        while True:
            try:
                user_jumlah_barang_inp = int(input("jumlah barang : "))
                break
            except:
                print("masukkan angka yang benar")
        sql_produk_cek_nama_barang = 'SELECT * FROM produk WHERE nama_barang = %s'
        val_produk_cek_nama_barang = (user_belanja_barang_inp,)
        mycursor.execute(sql_produk_cek_nama_barang,val_produk_cek_nama_barang)
        result_pcnm = mycursor.fetchall()
        for ipcnm in result_pcnm:
            rpcnm = ipcnm
        try:
            if user_jumlah_barang_inp <= rpcnm[3]:
                sql_add_id_keranjang = 'INSERT INTO keranjang(id_keranjang,jumlah) VALUES(%s,%s)'
                val_add_id_keranjang = (rpcnm[0],user_jumlah_barang_inp)
                mycursor.execute(sql_add_id_keranjang,val_add_id_keranjang)
                mydb.commit()
                print(f"Barang {user_belanja_barang_inp} telah di tambahkan ke dalam keranjang anda")
                break
                break
            else:
                print(f"Stok produk hanya ada {rpcnm[3]}")
                continue
        except mysql.connector.errors.IntegrityError:
            print("produk sudah ada di dalam keranjang")
            mycursor.execute('SELECT * FROM KERANJANG WHERE id_keranjang = %s',(rpcnm[0],))
            result_ada_keranjang = mycursor.fetchall()
            for irak in result_ada_keranjang:
                rpak = irak
            while True:
                user_inp_update_keranjang = input(f"Ingin Update Jumlah Barang {user_belanja_barang_inp} di dalam keranjang ? (Y/N)")
                total_jumlah = irak[1] + user_jumlah_barang_inp
                if user_inp_update_keranjang in ["y","Y"]:
                    if total_jumlah <= rpcnm[3]:
                        val_rpcnm = (total_jumlah,rpcnm[0])
                        mycursor.execute('UPDATE keranjang SET jumlah = %s WHERE id_keranjang = %s',(val_rpcnm))
                        mydb.commit()
                        print(f"berhasil update stok {user_belanja_barang_inp} di keranjang")
                        return
                    else:
                        print(f"stok {user_belanja_barang_inp} di keranjang melebihi batas ketersediaan")
                        break
                elif user_inp_update_keranjang in ["n","N"]:
                    print("Keluar update jumlah stok keranjang")
                    return
