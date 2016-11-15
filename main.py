import sys
from Tradier import *
from Mailboxlayer import *
from NYTimes import *
from CreateAccount import * 

# Defining Global Variables
global login 
global attempts
global sym_provided
global sym

# Defaulting Global Variables
login = False 			# Set the default value to False
attempts = 3			# Number of allowable login attempts by user. 
sym_provided = False	# Boolean if user provides a symbol value.

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



def menu():
	global sym_provided
	global sym

	print("\n\tCURRENTLY AVAILABLE OPTIONS")
	print("********************************************")
	if sym_provided:
		print("Change Symbol (p) | Tradier API (tr) | Twitter API (tw) | NYTimes API (n) | Exit the Program (e)\n")

	else: 
		print("Provide a Symbol (p) | Exit the Program (e)\n")
	
	choice = str(raw_input("Please enter your choice: ")).lower()

	if choice == 'p':
		sym = str(raw_input("Please provide a symbol: "))
		sym_provided = True

	elif choice == 'tr':
		if sym_provided:
			TradierAPI(sym)

		else:
			sym_err()

	elif choice == 'tw':
		if sym_provided:
			print("Sorry, that option is currently under development.")

		else:
			sym_err()

	elif choice == 'n':
		if sym_provided:
			NYTimes(sym)

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
	print("********************************************************************")		
	sys.exit(1)

# Custom error message when an invalid command is inputted. 
def command_err():
	print("\n\t####################################")
	print("\tERROR: Please enter a valid command!")
	print("\t####################################\n")

def sym_err():
	print("\n\t####################################")
	print("\tERROR: Must provide a Symbol!")
	print("\t####################################\n")
# Loop until user exits. 
while (1):
	checkLogin()



