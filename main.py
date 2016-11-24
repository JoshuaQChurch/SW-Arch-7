import sys
import os
from Tradier import *
from Mailboxlayer import *
from NYTimes import *
from CreateAccount import * 
from Twitter import *
from AccountManagement import *
from database import *
from User import *

# Defining Global Variables
global login 
global attempts
global sym_provided
global sym
global user

# Defaulting Global Variables
login = False 			# Set the default value to False
attempts = 3			# Number of allowable login attempts by user. 
sym_provided = False	# Boolean if user provides a symbol value.


# Verify that user is logged in before using system. 
def checkLogin():
	global attempts
	global login 
	global user

	# If user has exceeded maximum number of attempts, navigate to Account Creation menu.
	if attempts == 0:
		print("\n\t#############################################################")
		print("\tERROR: Unable to login. Directing you to Account Creation.")
		print("\t#############################################################\n")

		attempts = 3

		values = createAccount()
		if values is not None:
			login = True
			user = User(values[0],values[1],values[2],values[3],values[4], values[5])
			resetScreen()
			menu()

	# If the user is not logged in, display appropriate choices. 
	else: 
		# Display Welcome Message
		print("\n#########################################################################")
		print("\tWelcome to the Trade Net and Financial Services System!")
		print("#########################################################################\n")

		print(" Available Choices:")
		print("-------------------")
		print(" > Login\t\t(l)")
		print(" > Account Creation\t(c)")
		print(" > Exit Trade Net\t(e)\n")

		choice = str(raw_input(" Please enter your choice: ")).lower()
		

		# If login is chosen, verify that email and password are valid, and stored in the database
		if choice == 'l' and login == False:
			print(" \n Please log into your account.")
			print("******************************")
			email = str(raw_input(" EMAIL:  "))
			password = str(raw_input(" PASSWORD:  "))

			# Check user inputted values
			values = checkCreds(email, password)
			if values is None:
				attempts = attempts - 1
				creds_err()


			elif values is not None:
				login = True
				user = User(values[0],values[1],values[2],values[3],values[4], values[5])
				resetScreen()
				menu()

		# If user enters 'c', navigate to Account Creation menu
		elif choice == 'c' and login == False:
			resetScreen()
			values = createAccount()
			if values is not None:
				login = True
				user = User(values[0],values[1],values[2],values[3],values[4], values[5])
				resetScreen()
				menu()

		# If user enters 'e', exit the system
		elif choice == 'e':
			sys_exit()

		# Display invalid input message
		else:
			command_err()



def menu():
	global sym_provided
	global sym
	global user

	
	print("\n*******************************")
	print("\tWelcome, " + user.first + "!")
	print("*******************************")
	print("\nCURRENTLY AVAILABLE OPTIONS")
	print("------------------------------")
	
	if sym_provided:
		print(" > Current Symbol: [ " + sym + " ]")
		print(" \t| Change Symbol:\t\t(c)")
		print(" \t| View Stock Information:\t(v)")
		print(" \t| Purchase Stocks:\t\t(p)")
		print(" \t| Stock Tweets:\t\t\t(t)")
		print(" \t| Stock News:\t\t\t(n)")
		print(" > Account Management:\t\t\t(a)")
		print(" > Exit the Program\t\t\t(e)\n")

	else: 
		print(" > Account Management\t(a)") 
		print(" > Access Stock Menu\t(m)") 
		print(" > Exit the Program\t(e)\n")
	
	choice = str(raw_input("Please enter your choice: ")).lower()

	if choice == 'a':
		resetScreen()
		accountManagement(user)

	elif choice == 'c' or choice == 'm':
		sym = str(raw_input("Please provide a symbol: ")).upper()
		sym_provided = True

	elif choice == 'v' or choice == 'p':
		if sym_provided:
			resetScreen()
			TradierAPI(sym, user, False)

		else:
			sym_err()

	elif choice == 't':
		if sym_provided:
			resetScreen()
			TwitterAPI(sym)

		else:
			sym_err()

	elif choice == 'n':
		if sym_provided:
			NYTimesAPI(sym)

		else:
			sym_err()


	elif choice == 'e':
		sys_exit()

	else: 
		command_err()


# Custom exit menu upon system exit
def sys_exit():
	print("\n********************************************************************")
	print(" \tThank you for using Trade Net and Financial Services!")
	print(" \tHave a good day!")
	print("********************************************************************\n\n")		
	sys.exit(1)

# Custom error message when an invalid command is inputted. 
def command_err():
	print("\n\t####################################")
	print("\tERROR: Please enter a valid command!")
	print("\t####################################\n")

# Custom error message when an invalid command is inputted. 
def creds_err():
	print("\n\t####################################")
	print("\tERROR: Invalid Credentials!")
	print("\t####################################\n")

def sym_err():
	print("\n\t####################################")
	print("\tERROR: Must provide a Symbol!")
	print("\t####################################\n")

def resetScreen():
	try: 
		os.system('cls')
	except:
		pass

	try: 
		os.system('clear')

	except: 
		pass

# Loop until user exits. 
while (1):
	if not login: 
		checkLogin()
	else:
		menu()



