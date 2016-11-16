

def TwitterAPI(sym):

	# Check to see that the 'tweepy' module is installed
	try: 
		from tweepy import OAuthHandler
		from tweepy import API
		from tweepy import Cursor

	# If module is not installed, instruct user on how to install and return to main menu. 
	except ImportError, err:
		print("\n\t########################################################################")
		print("\tERROR: You must install 'tweepy' in order to utilize this functionality.")
		print("\t########################################################################\n")
		print("\t******************** INSTALLATION INSTRUCTIONS *************************\n")
		print("\tMETHOD 1\n")
		print("\t> sudo pip install tweepy \n")
		print("\tMETHOD 2\n")
		print("\t> git clone https://github.com/tweepy/tweepy.git")
		print("\t> cd tweepy")
		print("\t> python setup.py install\n\n") 
		return 

	# Credentials to utilize Twitter API functionality 
	access_token = "346694276-Bb2SOpj7vs9l5YIfieQEqebkU4qPq3daBvhMdo91"
	access_token_secret = "nLuSClFcxwDDpQCQz634qaw3lul7fI4UqJDkrXBHynFjn"
	consumer_key = "0uiAhp4h2LhOcSTczK3yIDbZU"
	consumer_secret = "20YS8SCNQiW2pWGsaiNnRz5MxPBMFzhKIuTg8zsGuEo6CZO8P9"

	# Authorize the API call using credentials 
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = API(auth)

	# Store search results in 'tweets' variable for easier parsing. 
	tweets = api.search(q="$" + sym)

	# Try to display 10 Tweets 
	try: 
		for i in range(10):
			try: 
				print("********* Tweet #" + str(i + 1) + " **********") 
				print("Tweet: " + str(tweets[i].text))
				print("Posted: " + str(tweets[i].created_at))
				print("Twitter User: " + str(tweets[i].user.screen_name))
			except UnicodeEncodeError:
				print("ERROR: Unable to properly encode this tweet.")

			print("\n")

	# If 10 Tweets are currently unavailable, return to menu
	except IndexError:
		return 
