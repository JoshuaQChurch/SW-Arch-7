import sqlite3
import os
import User as user


def databaseExists():

	if os.path.isfile('./TradeNet_Database.db'):
		return True
		
	else: 

		conn = sqlite3.connect('TradeNet_Database.db')
		c = conn.cursor()

		# Create table
		c.execute('''CREATE TABLE Users
		             (firstname TEXT, lastname TEXT, email TEXT, password TEXT, balance REAL, history VARCHAR)''')

		c.execute('''CREATE TABLE Trans 
					 (email TEXT, symbol TEXT, stock INTEGER)''')

		# Save the data to the database file. 
		conn.commit()
		conn.close()
		return True
	

# Check the user's credentials
def checkCreds(email, password):
	
	if databaseExists():
		conn = sqlite3.connect('TradeNet_Database.db')
		c = conn.cursor()
		for row in c.execute("SELECT * FROM Users WHERE email=? AND password=?", (email, password, )):
			return row

		conn.close()

def test():
	
	if databaseExists():

		conn = sqlite3.connect('TradeNet_Database.db')
		c = conn.cursor()

		print("USERS TABLE")
		for row in c.execute("SELECT * FROM Users"):
			print row

		print("\nTRANS TABLES")
		for row in c.execute("SELECT * FROM Trans"):
			print row


		conn.close()

# Function to make sure that e-mail doesn't already exist in system. 
def checkDB(email):

	if databaseExists():

		conn = sqlite3.connect('TradeNet_Database.db')
		c = conn.cursor()
		for row in c.execute("SELECT * FROM Users WHERE email=?", (email,)):
			return row

def update(option, value, email):

	# Verify that the database exists before performing any commands. 
	if databaseExists():

		# Connect to SQLite database file
		conn = sqlite3.connect('TradeNet_Database.db')
		c = conn.cursor()

		if option == 'name':
			c.execute("UPDATE Users SET firstname=?, lastname=? WHERE email=?", (value[0], value[1], email))
			conn.commit()
			conn.close()
		

		elif option == 'pass':
			c.execute("UPDATE Users SET password=? WHERE email=?", (value, email))
			conn.commit()
			conn.close()

		elif option == 'balance':
			c.execute("UPDATE Users SET balance=? WHERE email=?", (value, email))
			conn.commit()
			conn.close()

		elif option == 'history':

			temp = ""
			for row in c.execute("SELECT history FROM Users WHERE email=?", email):
				temp = temp + row[0]
			
			for each in value:
				temp = temp + str(each) + ','

			temp = temp + ';'

			c.execute("UPDATE Users SET history=? WHERE email=?", (temp, email))
			conn.commit()
			conn.close()


		elif option == 'new':
			c.execute("INSERT INTO Users VALUES (?,?,?,?,?,?)", (value[0], value[1], value[2], value[3], value[4], value[5]))
			conn.commit()
			conn.close()

def getHistory(email):

	conn = sqlite3.connect('TradeNet_Database.db')
	c = conn.cursor()

	for row in c.execute("SELECT history FROM Users WHERE email=?", (email,)):
		if not row[0]:
			return False

		else:
			return row[0]


	conn.close()

def saleHistoryCheck(email, amount, symbol, option):

	#for row in c.execute("SELECT symbol, stock FROM Trans WHERE email=?", (email, )):
	conn = sqlite3.connect('TradeNet_Database.db')
	c = conn.cursor()
	
	if option == 'purchase':

		c.execute("SELECT * FROM Trans")
		check = c.fetchall()
		updated = False

		if len(check) == 0:
			c.execute("INSERT INTO Trans VALUES (?,?,?)", (email, symbol, amount))
			conn.commit()
			return 

		for i in range(0, len(check)):
			if check[i][0] == email:
				if check[i][1] == symbol:
					stock = check[i][2] + amount
					c.execute("UPDATE Trans SET stock=? WHERE email=? AND symbol=?", (stock, email, symbol))
					conn.commit()
					update = True
					return 

		if not updated: 
			c.execute("INSERT INTO Trans VALUES (?,?,?)", (email, symbol, amount))
			conn.commit()

	elif option == 'owned':

		c.execute("SELECT symbol, stock FROM Trans WHERE email=?", (email, ))
		check = c.fetchall()

		if len(check) == 0:
			return False

		else: 
			return check

	elif option == 'sell':

		c.execute("SELECT * FROM Trans WHERE email=?", (email, ))
		check = c.fetchall()

		if len(check) == 0:
			return 0

		else: 
			for i in range(0, len(check)):
				if check[i][0] == email:
					if check[i][1] == symbol:
						stock = check[i][2] - amount
						if stock > 0:
							c.execute("UPDATE Trans SET stock=? WHERE email=? AND symbol=?", (stock, email, symbol))
							conn.commit()
							return 
						else:
							c.execute("DELETE FROM Trans WHERE email=? AND symbol=?", (email, symbol))
							conn.commit() 
							return 

