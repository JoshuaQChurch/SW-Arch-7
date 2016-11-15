from Mailboxlayer import *

# This function provides means for a user to create an account for the system
def createAccount():
	global login
	email_count = 3

	while (email_count > 0):
		# Provide a valid email address for the system 
		email = str(raw_input("Please enter a valid email address: "))
		r_email = str(raw_input("Please re-enter your email: "))

		# Verify that email attempts match
		if email == r_email:

			# Now verify legitimate email using MailboxLayer API
			if MailboxLayerAPI(email) == False:
				email_count = email_count - 1
				print("ERROR: Invalid Email Address.")
				print(str(email_count) + " attempts remaining.")			

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
						print("\n****************************")
						print("Account Successfully Created.")
						print("******************************\n")
						login = True
						return

					# Display error if passwords do not match.
					else:
						pass_count = pass_count - 1
						print("\nERROR: Sorry, those do not match.")
						print(str(pass_count) + " attempts remaining.")
						del password
						del r_password

		# Display non-matching email error message
		else:
			print("\nERROR: Non-matching email addresses")
			del email
			del r_email
			email_count = email_count - 1