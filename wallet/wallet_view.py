import mysql.connector
from wallet import Wallet
from System import belanja

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

mycursor = mydb.cursor()

def display_wallet(username_wallet):
    mycursor.execute('SELECT * FROM data_dompet WHERE username_dompet = %s',(username_wallet,))
    result_wallet = mycursor.fetchall()
    for irw in result_wallet:
        rw = irw[1]

    user_dat = Wallet(username_wallet,rw)

    print(f"{username_wallet} Anda Memiliki saldo di dompet anda sebanyak {user_dat.get_amount}")
    print("Pilih Opsi Selanjutnya")
    print("""

        1. Topup Saldo
        2. Checkout Keranjang
    
    """)

    while True:
        user_option = input("PIlih Opsi : ").lower()
        match user_option:
            case "1":
                topup_wallet(username_wallet=user_dat)
            case "2":
                keranjang(username_wallet=user_dat)


def topup_wallet(username_wallet):
    while True:
        try:
            jumlah_inp = int(input("masukkan Jumlah topup saldo : "))
        except:
            print("masukkan angka yang benar")
        if jumlah_inp < 0:
            print("Tidak bisa topup di angka minus")
        else:
            break
    username_wallet.topup_amount = jumlah_inp
    try:
        mycursor.execute('UPDATE data_dompet SET saldo = %s WHERE username_dompet = %s',(username_wallet.get_amount,username_wallet.get_name))
        mydb.commit()
        username_wallet.topup_amount = jumlah_inp
        print("Sukses topup Saldo")
    except:
        print("Gagal Topup Saldo")
    
def keranjang(username_wallet):
    print("ini adalah isi keranjang belanja anda")
    nama = "Nama Barang"
    harga_satuan = "harga satuan"
    jumlah = "jumlah yang anda beli"
    total = "total"

    print("\n"+"="*77)
    print(f"{nama:20} | {harga:20} | {jumlah:15} | {total:10}")
    print("-"*77)

    mycursor.execute('SELECT produk.nama_barang,produk.harga,keranjang.jumlah,produk.harga * keranjang.jumlah as total FROM produk JOIN keranjang ON(produk.id = keranjang.id_keranjang)')
    result_otw_checkout = mycursor.fetchall()

    for i in result_otw_checkout:
        print("{:<20} | {:<20} | {:<21} | {:<10}".format(i[0], i[1], i[2], i[3]))
    while True:
        input_barang_checkout = input("Pilih Barang Yang Ingin Anda Checkout (jika ingin belanja barang ketik 100: ")

        if input_barang_checkout == "100":
            belanja()
            continue
        is_user_keranjang_exist = False
        for iiuke in result_otw_checkout:
            if input_barang_checkout == iiuke[0]:
                is_user_keranjang_exist = True

        if is_user_keranjang_exist:
            break
        else:
            print("Nama barang tidak ada di dalam keranjang anda")
    while True:
        while True:
            try:
                user_jumlah_checkout = int(input("jumlah barang yang ingin di checkout : "))
                break
            except:
                print("masukkan angka yang benar")
        try:
            mycursor.execute('SELECT keranjang.id_keranjang,produk.nama_barang,keranjang.jumlah,produk.harga FROM produk JOIN keranjang ON(produk.id = keranjang.id_keranjang) WHERE nama_barang = %s',(input_barang_checkout,))
            result_pcnm = mycursor.fetchall()
            for ipcnm in result_pcnm:
                rpccnm = ipcnm
            if user_jumlah_checkout <= rpccnm[2]:
                user_total_belanja = rpccnm[3] * user_jumlah_checkout
                if_zero = rpccnm[2] - user_jumlah_checkout
                if if_zero == 0:
                    mycursor.execute('DELETE from keranjang WHERE id_keranjang = %s',(rpccnm[0],))
                checkout(username_wallet=username_wallet,total=user_total_belanja,jumlah_checkout=user_jumlah_checkout,barang_checkout=input_barang_checkout)
                return
            else:
                print(f"Stok produk hanya yang ada di dalam keranjang anda hanya {rpccnm[2]}")
                
        except:
            print("Gagal checkout barang")
            return
    
def checkout(username_wallet,total,jumlah_checkout,barang_checkout):
    get_saldo = username_wallet.get_amount
    try:
        if total >= get_saldo:
            print(f"Saldo Anda Kurang anda hanya memiliki saldo sebanyak {get_saldo}")
            input("Asda")
        else:
            try:
                mycursor.execute('UPDATE produk SET jumlah = jumlah - %s WHERE nama_barang = %s',(jumlah_checkout,barang_checkout))
                mydb.commit()
                mycursor.execute('update keranjang set jumlah = jumlah - %s where id_keranjang in (select id_keranjang from produk where nama_barang = %s)',(jumlah_checkout,barang_checkout))
                mydb.commit()
                
                print("Berhasil Chechout Barang")
            except Exception as e:
                print(e)
            else:
                w = username_wallet.get_name
                username_wallet.checkout_amount = total
                mycursor.execute('UPDATE data_dompet SET saldo = saldo - %s WHERE username_dompet = %s',(total,w))
                mydb.commit()
                print(f"Berhasil belanja barang ")
                input("tessss")
    except Exception as a:
        print(a)