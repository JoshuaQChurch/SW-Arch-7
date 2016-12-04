import httplib
import json
import datetime

def RedditAPI(query):

	connection = httplib.HTTPSConnection('www.reddit.com', 443, timeout = 30)

	connection.request('GET', '/r/news/search.json?q=' + query + '&sort=new&restrict_sr=on')
	
	try:
	  response = connection.getresponse()
	  content = response.read()
	  decoded_data = json.loads(content)
	  connection.close()
	  parseNews(decoded_data)

	except httplib.HTTPException, err:
	  print(err)


def parseNews(decoded_data):
	
	for i in range(5):
		print("TITLE: " + str(decoded_data["data"]["children"][i]["data"]["title"]))
		print("TIME-POSTED: " + str(datetime.datetime.fromtimestamp(decoded_data["data"]["children"][i]["data"]["created_utc"]).strftime('%c')))
		print("URL: " + str(decoded_data["data"]["children"][i]["data"]["url"]) + "\n\n")




	
