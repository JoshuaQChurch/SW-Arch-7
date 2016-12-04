
function TradierAPI(symbol, cb, err) {
    var api_key = "Bearer cJKYkXiurqAmDVzAXxWr4A1e28p6";

    var xhr = new XMLHttpRequest();

 	xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var postData = JSON.parse(xhr.responseText);
            cb(postData);
        } else {
    
            if(xhr.readyState === 4 && xhr.status !== 200){
    
                if(errcb !== null){
                    err();
                }
    
            }
    
        }
    };

    xhr.open("GET", "https://sandbox.tradier.com/v1/markets/quotes?symbols=" + symbol, true);
    xhr.setRequestHeader("Authorization", api_key);
    xhr.setRequestHeader("Accept", "application/json");
    xhr.send();
}

