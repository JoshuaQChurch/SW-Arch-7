<?php

	session_start();
	class MyDB extends SQLite3 {
		function __construct() {
			$this->open('../Model/database.db');
		}
	}

	$db = new MyDB();

	if ($_REQUEST['price'] == 'null') {
		echo "{\"response\":\"Error: The Tradier API is experiencing technical difficulties, no transactions can be made at this time!\"}";
		exit();  
	}

	if ($_REQUEST['type'] == 'Purchased') {

		$balance = $_SESSION['balance'] - $_REQUEST['price'] * $_REQUEST['stock'];

		// If user has enough funds, perform transaction
		if ($balance >= 0) { 

			// Update the user's balance
			$query = "SELECT balance FROM Users WHERE email='" . $_SESSION['email'] . "';";
			$result = $db->query($query);
			$row = $result->fetchArray();

			$_SESSION['balance'] = $balance;
			$query = "UPDATE Users SET balance=" . $_SESSION['balance'] . " WHERE email='" . $_SESSION['email'] . "';";
			$db->query($query);

			// Append the new transaction into the History table
			$query = "INSERT INTO History VALUES (
										 '" . $_SESSION['email'] . "',
										 '" . $_REQUEST['type'] . "', 
										 '" . $_REQUEST['company'] .  "',
										 '" . $_REQUEST['symbol'] .  "', 
										 " . $_REQUEST['price'] .  ", 
										 '" . $_REQUEST['date'] .  "', 
										 '" . $_REQUEST['time'] .  "',
										 " . $_REQUEST['stock'] . ");";
			$db->query($query);

			// Update owned stocks
			$query = "SELECT * FROM Stock WHERE email='" . $_SESSION['email'] . "';";
			$result = $db->query($query);

			while ($row = $result->fetchArray()) {
				if (($row['email'] == $_SESSION['email']) and ($row['company'] == $_REQUEST['company'])) {
					$updated_stock = $_REQUEST['stock'] + $row['stock'];
					$query = "UPDATE Stock 
							  SET stock=" . $updated_stock ." 
							  WHERE email='" . $_SESSION['email'] . "' AND company='" . $_REQUEST['company'] . "';";
					$db->query($query);
					$db->close();
					echo "{\"response\":\"Purchase Successful!\"}";
					exit();

				} 
			} 

			$query = "INSERT INTO Stock VALUES (
								 '" . $_SESSION['email'] . "',
								 '" . $_REQUEST['company'] . "', 
								 '" . $_REQUEST['symbol'] .  "',
								 " . $_REQUEST['stock'] .  ");";
			$db->query($query);
			$db->close();

			

			echo "{\"response\":\"Purchase Successful!\"}";
			exit();  

		} else {

			// Alert that transaction was not successful. 
			$db->close();
			echo "{\"response\":\"Insufficient Account Funds!\"}";
			exit();
		}
	} 						 

?>

