<?php

	function Mailboxlayer($email) {
		$access_key = 'dec5f1a7aa81ccb685a6527b2fe48835';

		$ch = curl_init("http://apilayer.net/api/check?access_key=". $access_key."&email=" . $email); 

		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

		// Store the data:
		$json = curl_exec($ch);
		curl_close($ch);


		// Decode JSON response:
		$validationResult = json_decode($json, true);

		return $validationResult['smtp_check'];

	}

?>