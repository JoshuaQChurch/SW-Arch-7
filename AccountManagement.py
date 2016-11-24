import User as user
import os
import Tradier as t
import database as db
import time 

def resetScreen():
	try: 
		os.system('cls')
	except:
		pass

	try: 
		os.system('clear')

	except: 
		pass


def accountManagement(user):

	while (1): 
		print("\n Account Information Options")
		print("------------------------------")
		print(" > Sell Owned Stocks\t\t(s)")
		print(" > Update Name\t\t\t(n)")
		print(" > Update Password\t\t(p)")
		print(" > Add Funds\t\t\t(f)")
		print(" > View Balance\t\t\t(b)")
		print(" > View Transaction History\t(h)")
		print(" > Return to Previous Menu\t(m)\n")
		choice = raw_input(str("Please enter your choice: ")).lower()

		if choice == 'n':
			user.updateName()
			print("\nYour name has been updated: ")
			print("First: " + user.first)
			print("Last: " + user.last + "\n")

		elif choice == 'p':
			user.changePassword()
			print("\nPassword Successfully Updated!\n")

		elif choice == 'f':
			user.addFunds()
			print("\nDeposit was successful!\n")

		elif choice == 'b':
			print("\nCurrent Balance: $" + str('%.2f' % (user.balance)))

		elif choice == 's':
			check = user.saleHistoryCheck('amount', 'symbol', 'owned')
			if check is not False:
				print("Currently Owned Stock")
				print("---------------------")
				for i in range(0, len(check)):
					print(str(i+1) + ": " + "Symbol: " + check[i][0] + " | Number Owned: " + str(check[i][1]) + "\n")
				
				sale = False
				symbol = str(raw_input("Provide the stock symbol you would like to sell: ")).upper()
				amount = int(input("How much would you like to sell? "))

				for i in range(0, len(check)):
					if check[i][0] == symbol:
						if check[i][1] >= amount:
							values = t.TradierAPI(symbol, user, True)
							current_price = values[0]
							company = values[1]
							print("\nCurrent Transaction Option")
							print("---------------------------")
							print(" > Symbol: " + symbol)
							print(" > Amount to be sold: " +  str(amount))
							print(" > Current price of each stock: $" + str(current_price))
							sale = True
							confirm = str(raw_input("\nConfirm purchase - Yes (y) or No (n): ")).lower()
							if confirm == 'y':
								stock = check[i][1] - amount 
								localtime   = time.localtime()
								timeDate  = time.strftime("%m-%d-%Y", localtime) 
								timeTime = time.strftime("%H:%M:%S", localtime)
								db_time = "Date: " + timeDate + " | Time: " + timeTime
								user.saleHistoryCheck(amount, symbol, 'sell')
								db.update('history', ['Sold', company, symbol, db_time, current_price, amount], user.email)
								user.balance = user.balance + (amount * current_price)
								db.update('balance', user.balance, user.email)
								print("\n-----------------------")
								print("Transaction Successful!\n")


							else:
								print("\nTransaction Cancelled")
								print("-----------------------\n")


						else: 
							print("\nERROR: You do not own that much stock.")
							return 
					else:
						print("\nERROR: You don't own any stock under symbol: " + symbol)

			else: 
				print("\nYou currently own no stock.\n")

		elif choice =='h':
			user.getHistory()

		elif choice == 'm':
			resetScreen()
			return 

		else:
			print("\n###################################")
			print("ERROR: Please enter a valid choice.")
			print("###################################\n")



