import httplib
import json

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

# Return Tradier stock information to the user in a legible format
def parseTradier(decoded_data, sym):
	try:
		print("Symbol: " + str(decoded_data["quotes"]["quote"]["symbol"]) + " | "
		+ "Current Price: $" + str(decoded_data["quotes"]["quote"]["close"]) + " | "
		+ "Change: " + str(decoded_data["quotes"]["quote"]["change"]) + " | "	 
		+ "Percent Change: " + str(decoded_data["quotes"]["quote"]["change_percentage"]) + "% | "
		+ "Volume: " + str(decoded_data["quotes"]["quote"]["volume"]))
	except KeyError:
		print("ERROR: " + sym + " is not a valid symbol.")