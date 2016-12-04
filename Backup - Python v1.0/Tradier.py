import httplib
import json
import database as db
import time

def TradierAPI(sym, user, sell): 

	# Make request to Tradier API using TCP connection 
	connection = httplib.HTTPSConnection('sandbox.tradier.com', 443, timeout = 30)

	# Headers
	# Accept information in JSON format
	# Provide proper API key
	headers = {"Accept":"application/json",
	           "Authorization":"Bearer cJKYkXiurqAmDVzAXxWr4A1e28p6"}

	connection.request('GET', '/v1/markets/quotes?symbols='+sym, None, headers)
	
	try:
	  response = connection.getresponse()
	  content = response.read()
	  decoded_data = json.loads(content)
	  connection.close()
	  
	  if sell: 
	  	return parseTradier(decoded_data, sym, user, sell)

	  else: 
	  	parseTradier(decoded_data, sym, user, sell)

	except httplib.HTTPException, err:
	  print(err)

# Return Tradier stock information to the user in a legible format
def parseTradier(decoded_data, sym, user, sell):

	if sell: 
		return [decoded_data["quotes"]["quote"]["close"], decoded_data["quotes"]["quote"]["description"]]

	try:
		print("\n****** TRADIER STOCK INFORMATION **********\n")
		print("\t > Company: " + str(decoded_data["quotes"]["quote"]["description"]) 
		+ "\n\t\t | Symbol: " + str(decoded_data["quotes"]["quote"]["symbol"])
		+ "\n\n\t > Current Stock Information:" 
		+ "\n\t\t | Price per Stock: $" + str(decoded_data["quotes"]["quote"]["close"]) 
		+ "\n\t\t | Change: " + str(decoded_data["quotes"]["quote"]["change"])	 
		+ "\n\t\t | Percent Change: " + str(decoded_data["quotes"]["quote"]["change_percentage"]) + "%" 
		+ "\n\t\t | Volume: " + str(decoded_data["quotes"]["quote"]["volume"]))
		localtime   = time.localtime()
		timeDate  = time.strftime("%m-%d-%Y", localtime) 
		timeTime = time.strftime("%H:%M:%S", localtime)
		print("\n\t > Current Time Information:")
		print("\t\t | Date: " + timeDate)
		print("\t\t | Time: " + timeTime)

		choice = str(raw_input("\nWould you like to purchase stock? (y) - Yes, (n) - No: ")).lower()
		if choice == 'y':
			stock = []
			stock.append(str(decoded_data["quotes"]["quote"]["description"]))
			stock.append(str(decoded_data["quotes"]["quote"]["symbol"]))
			stock.append(decoded_data["quotes"]["quote"]["close"])
			purchaseStock(stock, user)

		else:
			return 

	# If the symbol passed is invalid, display error to user. 
	except KeyError:
		print("\n\t####################################")
		print("\tERROR: " + sym + " is not a valid symbol!")
		print("\t####################################\n")


def purchaseStock(stock, user):
	
	while (1):

		try: 
			amount = int(input("Enter the amount you would like to purchase: "))
		
		except ValueError:
			print("\n\t####################################")
			print("\tERROR: Please enter a numerical value!")
			print("\t####################################\n")

		if str(raw_input("Confirm Purchase? (y) - Yes, (n) - No: ")).lower() == 'y':
			
			try:
				balance = user.getBalance() - (stock[2] * amount)
			
				#test_price = 100
				#balance = user.getBalance() - (test_price * amount)
				if balance > 0:

					user.balance = balance
					print("\n\t > Stock Purchased From: " + stock[0])
					print("\t > Total Amount Spent: $" + str('%.2f' % (stock[2] * amount)))
					#print("\t > Total Amount Spent: $" + str('%.2f' % (test_price * amount)))
					print("\t > Total Stock Purchased: " + str(amount))
					print("\t > Balance remaining: $" + str('%.2f' % (user.balance)))
					localtime   = time.localtime()
					timeDate  = time.strftime("%m-%d-%Y", localtime) 
					timeTime = time.strftime("%H:%M:%S", localtime)
					db_time = "Date: " + timeDate + " | Time: " + timeTime
					print("\n\t > Time Purchased:")
					print("\t\t | Date: " + timeDate)
					print("\t\t | Time: " + timeTime + "\n\n")
					
					
			
				else:
					print("\n\t####################################")
					print("\tERROR: Insufficient Funds!") 
					print("\t####################################\n")
					return

			except TypeError:
				print("\n\t################################################################")
				print("\tERROR: API currently unavailable! Returning...")
				print("\t################################################################\n")
				return

			db.update('balance', user.balance, user.email)
			db.update('history', ['Purchased', stock[0], stock[1], db_time, stock[2], amount], user.email)
			user.saleHistoryCheck(amount, stock[1], 'purchase')
			#db.update('history', ['Purchased', stock[0], stock[1], db_time, test_price, amount], user.email)
			return



		# If user doesn't confirm purchase
		else:
			return







