import httplib
import json

def NYTimes(sym): 

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

# Return Tradier stock information to the user in a legible format
def parseData(decoded_data):
	for i in range(5):
		try: 
			if (str(decoded_data["response"]["docs"][i]["snippet"].encode('utf-8')) != ''):
				print("SNIPPET: " + str(decoded_data["response"]["docs"][i]["snippet"].encode('utf-8')))

			elif (str(decoded_data["response"]["docs"][i]["snippet"].encode('utf-8')) == ''):
				print("SNIPPET: Currently unavailable.")

			if (str(decoded_data["response"]["docs"][i]["web_url"].encode('utf-8')) != ''):
				print("URL: " + str(decoded_data["response"]["docs"][i]["web_url"].encode('utf-8')))
			
			elif (str(decoded_data["response"]["docs"][i]["web_url"].encode('utf-8')) == ''):
				print("URL: Currently unavailable.")

			if (str(decoded_data["response"]["docs"][i]["pub_date"].encode('utf-8')) != ''):
				print("PUBLISHED: " + str(decoded_data["response"]["docs"][i]["pub_date"].encode('utf-8')))

			elif (str(decoded_data["response"]["docs"][i]["pub_date"].encode('utf-8')) == ''):
				print("PUBLISHED: Currently unavailable.")
			
			print("\n\n")

		except UnicodeEncodeError, err:
			print(err)
