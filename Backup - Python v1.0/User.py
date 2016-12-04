import database as db
from Mailboxlayer import *
import sqlite3

class User(): 
	def __init__(self, first, last, email, password, balance, history):
		self.first = first
		self.last = last
		self.email = email
		self.password = password
		self.balance = balance
		self.transactionHistory = []

	def updateName(self):
		self.first = str(raw_input("Firstname: "))
		self.last = str(raw_input("Lastname: "))
		db.update('name', [self.first, self.last], self.email)

	def changePassword(self):
		pass_attempts = 3
		new_pass_attempts = 3
		old_password = self.password

		while (pass_attempts > 0):
			password = raw_input(str("Please enter your old password: "))
			if password == old_password:
				while (new_pass_attempts > 0):

					password = raw_input(str("Please enter your new password: "))
					r_password = raw_input(str("Please enter your new password again: "))
					
					if password == r_password:
						print("Password successfully updated!")
						db.update('pass', password, self.email)
						self.password = password
						return
					
					else: 
						new_pass_attempts = new_pass_attempts - 1
						print("\nERROR: Non-matching passwords.")
						print(str(new_pass_attempts) + " attempts remaining.\n")
						if (new_pass_attempts == 0):
							print("ERROR: You have exceeding the maximum attempts. System exiting...\n")
							sys.exit(-1)
						

			else:
				pass_attempts = pass_attempts - 1
				print("ERROR: Non-matching passwords.")
				print(str(pass_attempts) + " attempts remaining.\n")

		print("ERROR: You have exceeding the maximum attempts. System exiting...\n")
		sys.exit(-1)

	def addFunds(self):
		attempts = 3
		
		while (attempts > 0):
			try: 
				funds = float(raw_input("Add funds: "))
				self.balance = self.balance + funds
				db.update('balance', self.balance, self.email)
				return 
			
			except ValueError:
				attempts = attempts - 1
				print("ERROR: Please enter a numerical value.")
				print(str(attempts) + " attempts remaining.\n")
			
			if attempts == 0: 
				print("You have failed too many times.")
				print("Now exiting...\n")
				exit(-1)

	def getBalance(self):
		return float(self.balance)


	def getHistory(self):
		
		row = db.getHistory(self.email)
		
		if row == False:
			print("\n\nThere is no past transaction history.\n")

		else:
			row = row.split(';')
			for i in range(len(row) - 1):
				row[i] = row[i].split(',')
				print("\nTransaction")
				print("-----------")
				print(" > Transaction Type: " + row[i][0])
				print(" > Company: " + row[i][1])
				print(" > Symbol: " + row[i][2])
				print(" > Timestamp: " + row[i][3])
				print(" > Stock Price: $" + row[i][4])
				print(" > Amount: " + row[i][5])


	def saleHistoryCheck(self, amount, symbol, option):

		if option == 'owned':
			return db.saleHistoryCheck(self.email, amount, symbol, option)

		else: 
			db.saleHistoryCheck(self.email, amount, symbol, option)
		


