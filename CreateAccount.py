from Mailboxlayer import *
import database as db

# This function provides means for a user to create an account for the system
def createAccount():
	email_count = 3

	print("\n##########################################")
	print("\tACCOUNT CREATION PAGE")
	print("##########################################\n")

	while (email_count > 0):

		# Provide valid credentials
		email = str(raw_input("Please enter a valid email address: "))
		r_email = str(raw_input("Please re-enter your email: "))

		# Verify that email attempts match
		if email == r_email:

			# Verify that the email doesn't already exist in the system.
			if db.checkDB(email) is None:

				first = str(raw_input("Please enter your first name: "))
				last = str(raw_input("Please enter your last name: "))
				# Now verify legitimate email using MailboxLayer API

				if MailboxlayerAPI(email) == False:
					email_count = email_count - 1
					print("ERROR: Invalid Email Address.")
					print(str(email_count) + " attempts remaining.\n")			

				else:
					# Allow user to enter new password 3 times
					pass_count = 3
					while (pass_count > 0):

						# Obtain password for user's account
						password = str(raw_input("\nPlease enter your password: "))	
						r_password = str(raw_input("Please re-enter your password: "))

						# Verify that the passwords match
						if password == r_password:

							# Display Account Creation Success Message
							print("\n*****************************")
							print("Account Successfully Created.")
							print("*****************************\n")
							values = [first, last, email, password, 0, ""]
							db.update('new', values, None)
							return values

						# Display error if passwords do not match.
						else:
							pass_count = pass_count - 1
							print("\nERROR: Sorry, those do not match.")
							del password
							del r_password
							if pass_count == 0:
								print("ERROR: You must re-enter your e-mail address after 3 failed password attempts.\n")
								email_count = 3
			
			else:
				print("\nERROR: Sorry, that email address is already in our system.\n")


		# Display non-matching email error message
		else:
			print("\nERROR: Non-matching email addresses")
			del email
			del r_email
			email_count = email_count - 1
			print(str(email_count) + " remaining.\n")

	if email_count == 0:
		print("WARNING: Too many fail account creations. Exiting... \n\n")
		exit(-1)
