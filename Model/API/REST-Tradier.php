<?php

	function TradierAPI($symbol) {
		$curl = curl_init();

		curl_setopt_array($curl, array(
		  CURLOPT_URL => "https://sandbox.tradier.com/v1/markets/quotes?symbols=" . $symbol,
		  CURLOPT_RETURNTRANSFER => true,
		  CURLOPT_SSL_VERIFYPEER => false,
		  CURLOPT_ENCODING => "",
		  CURLOPT_MAXREDIRS => 10,
		  CURLOPT_TIMEOUT => 30,
		  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
		  CURLOPT_CUSTOMREQUEST => "GET",
		  CURLOPT_HTTPHEADER => array(
		    "authorization: Bearer cJKYkXiurqAmDVzAXxWr4A1e28p6",
		    "Content-type: application/json",
		    "Accept: application/json",
		    "cache-control: no-cache"
		  ),
		));

		$response = curl_exec($curl);
		$values = json_decode($response, true);

		$err = curl_error($curl);

		curl_close($curl);

		if ($err) {
		  echo false;
		} else {
		  	return $values;
		}
	}

?>