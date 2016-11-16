import httplib
import json
import datetime

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
		print("\n****** TRADIER STOCK INFORMATION **********\n")
		print("Symbol: " + str(decoded_data["quotes"]["quote"]["symbol"]) + " | "
		+ "Current Price: $" + str(decoded_data["quotes"]["quote"]["close"]) + " | "
		+ "Change: " + str(decoded_data["quotes"]["quote"]["change"]) + " | "	 
		+ "Percent Change: " + str(decoded_data["quotes"]["quote"]["change_percentage"]) + "% | "
		+ "Volume: " + str(decoded_data["quotes"]["quote"]["volume"]))
		print("\nInformation Accessed at time: " + str(datetime.datetime.now()))
		print("\n** REMINDER: Remember to always get the current information before purchasing new stock! \n\n")

	# If the symbol passed is invalid, display error to user. 
	except KeyError:
		print("ERROR: " + sym + " is not a valid symbol.") 