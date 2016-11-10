import httplib
import sys
import json
global login 
global count


login = False
count = 3

def checkLogin():
	global count
	global login 

	if login == False:
		print("\n#########################################################################")
		print("\tWelcome to the Trade Net and Financial Services System!")
		print("#########################################################################\n")

		choice = str(raw_input("Please enter (L) to Login | (C) to Create an account | (E) to Exit: ")).lower()
		
		if choice == 'l':
			print(" \nPlease log into your account.")
			print("******************************")
			email = str(raw_input(" EMAIL:  "))
			password = str(raw_input(" PASSWORD:  "))

			if checkCred(email, password) and count > 0:
				login = True

			else: 
				count = count - 1
				print("\n\t##########################################")
				print("\tERROR: Must be logged in to use this system.")
				print("\t############################################\n")

				if (count == 0):
					print("You have exceeded the maximum number of login attempts.")
					createAccount()

				else:
					return

		elif choice == 'c' and login == False:
			createAccount()

		elif choice == 'e':
			exit_sys()

		else:
			comm_err()

	elif login == True:
		menu()

def checkCred(email, password):
	global login
	if email == 'test' and password == 'test':
		login = True
		return True
	
	else:
		login = False
		return False

def createAccount():
	global login
	email = str(raw_input("Please enter your desired email: "))
	r_email = str(raw_input("Please re-enter your email: "))

	if email == r_email:

		# This is where the API check should happen 

		password = str(raw_input("\nPlease enter your password: "))	
		r_password = str(raw_input("Please re-enter your password: "))

		if password == r_password:
			print("SUCCESS! Thank you for creating an account with Trade Net!")
			login = True
			return

		else:
			print("\nERROR: Sorry, those do not match.")
			del password
			del r_password
			createAccount()

	else:
		print("\nERROR: Sorry, those do not match.")
		del email
		del r_email
		createAccount()

def menu():
	print("\n\tCURRENTLY AVAILABLE OPTIONS")
	print("********************************************")
	print("Tradier Stock Prices (T) | Exit (E)\n")
	choice = str(raw_input("Please enter your choice: ")).lower()

	if choice == 't':
		sym_array = []
		
		while (1):
			sym = str(raw_input("Which symbols would you like to check? "))
			sym_array.append(sym)
			add = str(raw_input("Add another? (y) to add another, (n) to currently added: ")).lower()
			print("\n")
			if (add != 'y'):
				for sym in sym_array:
					TradierAPI(sym)
				return

	elif choice == 'e':
		exit_sys()

	else: 
		comm_err()



def TradierAPI(sym): 

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
	  parser(decoded_data, sym)

	except httplib.HTTPException, err:
	  print(err)


def parser(decoded_data, sym):
	try:
		print("Symbol: " + str(decoded_data["quotes"]["quote"]["symbol"]) + " | "
		+ "Current Price: $" + str(decoded_data["quotes"]["quote"]["close"]) + " | "
		+ "Change: " + str(decoded_data["quotes"]["quote"]["change"]) + " | "	 
		+ "Percent Change: " + str(decoded_data["quotes"]["quote"]["change_percentage"]) + "% | "
		+ "Volume: " + str(decoded_data["quotes"]["quote"]["volume"]))
	except KeyError:
		print("ERROR: " + sym + " is not a valid symbol.")

# Function to give user option to return to menu or exit. 
def return_to_menu(): 
	# Once user has seen selection, give them choice to try a different selection
	print("\n\n*******************************************")
	print("Would you like to return to the main menu?")
	print("Enter (y) to return; otherwise, type anything else to exit.")
	return_to_menu = raw_input("Please enter you choice: ")
	
	if (return_to_menu.lower() == 'y'):
		menu()
	else:
		exit_sys()	

def exit_sys():
	print("\n********************************************************************")
	print(" \tThank you for using Trade Net and Financial Services!")
	print(" \tHave a good day!")
	print("********************************************************************")		
	sys.exit(1)

def comm_err():
	print("\n\t####################################")
	print("\tERROR: Please enter a valid command!")
	print("\t####################################\n")

while (1):
	checkLogin()
