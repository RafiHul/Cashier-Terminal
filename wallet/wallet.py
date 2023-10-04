import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'kasir',
    password = 'yes',
    database = 'kasir_database'
)

mycursor = mydb.cursor()

class Wallet:
	def __init__(self,name,amount):
		self.__name = name
		self.__amount = amount
	
	@property
	def amount(self):
		return self.__amount

	@property
	def name(self):
		return self.__name

	@name.getter
	def get_name(self):
		return self.__name
	
	@amount.getter
	def get_amount(self):
		return self.__amount
	
	@amount.setter
	def topup_amount(self, inp):
		try:
			new_amount = self.__amount +inp
			mycursor.execute('UPDATE data_dompet SET saldo = %s WHERE username_dompet = %s',(new_amount,self.__name))
			mydb.commit()
		except:
			print("Gagal melakukan topup harap coba lagi")
			mydb.rollback()

	@amount.setter
	def checkout_amount(self, inp):
		self.__amount -= inp
	
