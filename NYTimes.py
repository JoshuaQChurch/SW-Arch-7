import httplib
import json

def NYTimesAPI(sym): 

	# Make request to New York Times API using TCP connection 
	connection = httplib.HTTPSConnection('api.nytimes.com', 443, timeout = 30)

	api_key = '9b675c451b454088887ab16495dad464'

	connection.request('GET', '/svc/search/v2/articlesearch.json?api-key=' + api_key + '&q=' + sym + '&sort=newest')

	try:
	  response = connection.getresponse()
	  content = response.read()
	  decoded_data = json.loads(content)
	  connection.close()
	  parseData(decoded_data)

	except httplib.HTTPException, err:
	  print(err)

# Return News Data for the user to view.
def parseData(decoded_data):

	# Try to parse data, if data is found. 
	try: 
		for i in range(5):

			# Handles encoding issues.
			try: 
				if (str(decoded_data["response"]["docs"][i]["snippet"].encode('utf-8')) != ''):
					print("Story Snippet: " + str(decoded_data["response"]["docs"][i]["snippet"].encode('utf-8')))

				elif (str(decoded_data["response"]["docs"][i]["snippet"].encode('utf-8')) == ''):
					print("Story Snippet is currently unavailable.")

				if (str(decoded_data["response"]["docs"][i]["web_url"].encode('utf-8')) != ''):
					print("URL: " + str(decoded_data["response"]["docs"][i]["web_url"].encode('utf-8')))
				
				elif (str(decoded_data["response"]["docs"][i]["web_url"].encode('utf-8')) == ''):
					print("URL is currently unavailable.")

				if (str(decoded_data["response"]["docs"][i]["pub_date"].encode('utf-8')) != ''):
					print("Published Time: " + str(decoded_data["response"]["docs"][i]["pub_date"].encode('utf-8')))

				elif (str(decoded_data["response"]["docs"][i]["pub_date"].encode('utf-8')) == ''):
					print("Published Time is currently unavailable.")
				
				print("\n\n")

			except UnicodeEncodeError, err:
				print("ERROR: Unable to properly encode the news reponse.")

	# If no news can be found about the passed symbol, return to menu
	except IndexError:
		return
