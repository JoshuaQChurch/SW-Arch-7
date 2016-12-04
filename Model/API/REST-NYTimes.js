function NYTimesAPI(symbol, cb, err) {
    var api_key = '9b675c451b454088887ab16495dad464';

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

	xhr.open("GET", "https://api.nytimes.com/svc/search/v2/articlesearch.json?api-key=" + api_key + "&q=" + symbol + "&sort=newest", true);
    xhr.send();

}

