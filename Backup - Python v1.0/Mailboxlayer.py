import httplib
import json

# Check the validity of the email address using MailboxLayer API
def MailboxlayerAPI(email):

	# Make request to MailboxLayer API using TCP connection 
	connection = httplib.HTTPSConnection('apilayer.net', 443, timeout = 30)

	# Custom Access (API) Key
	access_key = "dec5f1a7aa81ccb685a6527b2fe48835"

	# Make connection using GET request
	connection.request('GET', '/api/check?access_key=' + access_key + "&email=" + email)

	# Try the connection and getting response. 
	try:
	  response = connection.getresponse()
	  content = response.read()
	  decoded_data = json.loads(content)
	  connection.close()

	# Return error message upon failure
	except httplib.HTTPException, err:
	  print(err)

	# If the format is valid and passes the smtp check, then
	# a True will be returned, showing a valid email address. 
	return (decoded_data["format_valid"] and decoded_data["smtp_check"])
