import httplib
import sys
import json

# Defining Global Variables
global login 
global attempts

# Defaulting Global Variables
login = False 	# Set the default value to False
attempts = 3		# Number of allowable login attempts by user. 

# Verify that user is logged in before using system. 
def checkLogin():
	global attempts
	global login 

	# If the user is logged in, navigate to menu options
	if login:
		menu()

	# If the user is not logged in, display appropriate choices. 
	else: 
		# Display Welcome Message
		print("\n#########################################################################")
		print("\tWelcome to the Trade Net and Financial Services System!")
		print("#########################################################################\n")

		choice = str(raw_input("Please enter (L) to Login | (C) to Create an account | (E) to Exit: ")).lower()
		
		# If user has exceeded maximum number of attempts, navigate to Account Creation menu.
		if attempts == 0:
			print("ERROR: You have exceeded the maximum number of login attempts.")
			createAccount()


		# If login is chosen, verify that email and password are valid, and stored in the database
		elif choice == 'l' and login == False:
			print(" \nPlease log into your account.")
			print("******************************")
			email = str(raw_input(" EMAIL:  "))
			password = str(raw_input(" PASSWORD:  "))

			# Check user inputted values
			checkCred(email, password)

		# If user enters 'c', navigate to Account Creation menu
		elif choice == 'c' and login == False:
			createAccount()

		# If user enters 'e', exit the system
		elif choice == 'e':
			sys_exit()

		# Display invalid input message
		else:
			command_err()

# Check the user's credentials
def checkCred(email, password):
	global login
	global attempts

	# Verify legitimate email using MailboxLayer API
	# Verify for legitimate password stored in database
	# Verify maximum attempts haven't been exceeded. 
	if MailboxLayerAPI(email) and password == 'test' and attempts > 0:
		login = True
		print("\n\t**************************************")
		print("\t\tLOGIN SUCCESSFUL!")
		print("\t**************************************\n")
	
	# If credential information invalid, return error
	else:
		attempts = attempts - 1
		print("\n\t##########################################")
		print("\t\tERROR: Invalid Credentials.")
		print("\t############################################\n")

# This function provides means for a user to create an account for the system
def createAccount():
	global login
	email_count = 3

	while (email_count > 0):
		# Provide a valid email address for the system 
		email = str(raw_input("Please enter your desired email: "))
		r_email = str(raw_input("Please re-enter your email: "))

		# Verify that email attempts match
		if email == r_email:

			# Now verify legitimate email using MailboxLayer API
			if MailboxLayerAPI(email) == False:
				print("ERROR: The email provided is invalid!")
				print("Please provide a valid email address.\n")

			else:
				# Allow user to enter new password 3 times
				pass_count = 3
				while (pass_count > 0):

					# Obtain password for user's account
					password = str(raw_input("\nPlease enter your password: "))	
					r_password = str(raw_input("Please re-enter your password: "))

					# Verify that the passwords match
					if password == r_password:
						print("SUCCESS! Thank you for creating an account with Trade Net!")
						login = True
						return

					# Display error if passwords do not match.
					else:
						print("\nERROR: Sorry, those do not match.")
						del password
						del r_password
						pass_count = pass_count - 1

		else:
			print("\nERROR: Sorry, those do not match.")
			del email
			del r_email
			email_count = email_count - 1

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
		sys_exit()

	else: 
		command_err()

def MailboxLayerAPI(email):

	# Make request to MailboxLayer API using TCP connection 
	connection = httplib.HTTPSConnection('apilayer.net', 443, timeout = 30)

	access_key = "dec5f1a7aa81ccb685a6527b2fe48835"

	connection.request('GET', '/api/check?access_key=' + access_key + "&email=" + email)

	try:
	  response = connection.getresponse()
	  content = response.read()
	  decoded_data = json.loads(content)
	  connection.close()

	except httplib.HTTPException, err:
	  print(err)

	return (decoded_data["format_valid"] and decoded_data["smtp_check"])

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
	  parseTradier(decoded_data, sym)

	except httplib.HTTPException, err:
	  print(err)


def parseTradier(decoded_data, sym):
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

def sys_exit():
	print("\n********************************************************************")
	print(" \tThank you for using Trade Net and Financial Services!")
	print(" \tHave a good day!")
	print("********************************************************************")		
	sys.exit(1)

def command_err():
	print("\n\t####################################")
	print("\tERROR: Please enter a valid command!")
	print("\t####################################\n")

while (1):
	checkLogin()