document.getElementById('symbol-search').onclick= function() {

	TradierAPI(document.getElementById('symbol').value.toUpperCase(), function(data){
		if (data.quotes.quote) {
			document.getElementById('symbol-container').style.display = "block";
			document.getElementById('tradier').innerHTML = 
			"<img src='../View/src/images/tradier-brokerage-logo.png' alt='<h2>Tradier Stock Information</h2>' style='width:auto; align:center;'><hr style='border-top: 1px solid #000000'>" 
			+ "<table class='table-responsive' style='width: 100%'>"
			+ "<col width='33%'><col width='33%'><col width='33%'>"
			+ "<tr>"
			+ "<th><a href='http://www.investopedia.com/terms/s/stocksymbol.asp?lgl=no-infinite' target='_blank'>Symbol</a></th>"
			+ "<th><a href='http://www.advfn.com/nyse/newyorkstockexchange.asp' target='_blank'>Company</a></th>"
			+ "<th><a href='http://www.investopedia.com/terms/c/closingprice.asp' target='_blank'>Closing Stock Price</a></th>"
			+ "</tr>"
			+ "<tr>"
			+ "<td>" + data.quotes.quote.symbol + "</td>"
			+ "<td>" + data.quotes.quote.description + "</td>"
			+ "<td>$" + data.quotes.quote.prevclose + "</td>"
			+ "</tr><tr></tr>"
			+ "<tr>" 
			+ "<th><a href='http://www.investopedia.com/terms/c/change.asp?lgl=no-infinite' target='_blank'>Stock Change</a></th>"
			+ "<th><a href='http://www.investopedia.com/terms/p/percentage-change.asp?lgl=no-infinite' target='_blank'>Percentage Change</a></th>"
			+ "<th><a href='http://www.investopedia.com/terms/v/volume.asp?lgl=no-infinite' target='_blank'>Volume</a></th>"
			+ "</tr>"
			+ "<tr>"
			+ "<td " + ((data.quotes.quote.change > 0 && data.quotes.quote.change != 0) ? "style='color: green'>+":"style='color: red'>") + data.quotes.quote.change + "</td>"
			+ "<td class='" + ((data.quotes.quote.change_percentage > 0 && data.quotes.quote.change_percentage != 0) ? "glyphicon glyphicon-triangle-top' style='color: green'> ":"glyphicon glyphicon-triangle-bottom' style='color: red'>") + data.quotes.quote.change_percentage + "%</td>"
			+ "<td>" + data.quotes.quote.volume + "</td>"
			+ "</tr>"
			+ "</table><br>"
            + "<input id='purchase_amount' type='number' step='1' min='1' class='form-control' placeholder='Amount' style='width:40%; display:inline; margin-right: 10px;' required>"
            + "<button class='btn btn-primary' id='purchase' style='width:40%; display:inline;'>Purchase</button>";
            
       
            // XML request to obtain 'tweet' object from Model/API/REST-Twitter
			var xhr = new XMLHttpRequest();
			xhr.onreadystatechange = function () {

				// If successful, store parsed data into twitter div
				if (xhr.readyState === 4 && xhr.status === 200) {
					
					// Stores returned 'tweet' object in variable
					var tweet = JSON.parse(xhr.responseText);
					var html = "<img src='../View/src/images/twitter.jpg' alt='<h2>Twitter</h2>' style='width:100%'><hr style='border-top: 1px solid #000000'>"; 
					
					// Displays all 'english-languaged' tweets (assumming non-null values)
					for (var i = 0; i < tweet.statuses.length; i++) {
						if (tweet.statuses[i].lang == "en") {
							if (tweet.statuses[i].user.screen_name) {
								html += "<b>Posted by user: </b>" + tweet.statuses[i].user.screen_name + "<br>";
							}
							if (tweet.statuses[i].user.created_at) {
								html += "<b>Posted at:</b> " + tweet.statuses[i].created_at + "<br>";
							}

							if (tweet.statuses[i].user.description) {
								html += "<b>Tweet:</b> " + tweet.statuses[i].text + "<br>";
							}

							html += "<hr style='border-top: 1px solid #000000'>";
						}
					}	

				// If non-sucessful, log the error
				} else {
			
					if(xhr.readyState === 4 && xhr.status !== 200){
						console.log('Twitter Error');
					}
				}
				
				// Store HTML elements into twitter div
				document.getElementById('twitter').innerHTML = html;
			};

			// Execute the XML request
			xhr.open("POST", "../Model/API/REST-Twitter.php?symbol=" + document.getElementById('symbol').value.toUpperCase(), true);
			xhr.send();
			
			
		
			// Function to handle purchase functionality 
		   	document.getElementById('purchase').onclick = function() {

			   	var xhr = new XMLHttpRequest();
				xhr.onreadystatechange = function () {
			        if (xhr.readyState === 4 && xhr.status === 200) {

			        	// Alert self-made responses and return back to menu screen
			           	alert(JSON.parse(xhr.responseText).response);
			            window.location.href = "menu.php";

			        } else {
			    
			            if(xhr.readyState === 4 && xhr.status !== 200){
			    			console.log('This is an error');
			                }
			        }
			    };

			    // Post and execute commands through the update_database controller class
		    	var d = new Date();
				xhr.open("POST", "../Controller/update_database.php?type=Purchased&company=" + data.quotes.quote.description + "&symbol=" + data.quotes.quote.symbol + "&price=" + data.quotes.quote.prevclose + "&date=" + d.toDateString() + "&time=" + d.toTimeString() + "&stock=" + document.getElementById('purchase_amount').value, true);
				xhr.send();
		   	}			
		
		// If the user provides an invalid symbol, alert and return
		} else {
			document.getElementById('symbol-container').style.display = "none";
			alert("Please provide a valid symbol.");
			document.getElementById('tradier').innerHTML = "Sorry, that is an invalid symbol.";
		}
		// Slight error checking
	}, function(){
		console.log("Error");
	});

	// Function to handle New York Times News functionality
	NYTimesAPI(document.getElementById('symbol').value.toUpperCase(), function(data){

		var news = ""; 

		for (var i = 0; i < data.response.docs.length; i++) {

			if (data.response.docs[i].headline.main) {
				news += "<b>Title:</b> " + data.response.docs[i].headline.main + "<br>";
			}
			if (data.response.docs[i].snippet) {
				news += "<b>Story snippet:</b> " + data.response.docs[i].snippet + "<br>";
			}

			if (data.response.docs[i].pub_date) {
				news += "<b>Date posted:</b> " + data.response.docs[i].pub_date + "<br>";
			}

			if (data.response.docs[i].web_url) {
				news += "<a href='" + data.response.docs[i].web_url + "' target='_blank'>Click here to view the rest of the story</a><br>";
			}

			news += "<hr style='border-top: 1px solid #000000'>"
			
		}

		document.getElementById('nytimes').innerHTML = "<img src='../View/src/images/nytimes-logo.png' alt='<h2>New York Times News</h2>' style='width:95%;'><hr style='border-top: 1px solid #000000'>" + news;
		
	}, function(){
		console.log("Error");
	});
	
};



