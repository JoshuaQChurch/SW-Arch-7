<?php
	@session_start();

	$symbol = strtoupper($_REQUEST['symbol']);
	$sold = $_REQUEST['sold'];

	include '../Model/API/REST-Tradier.php';
	$values = TradierAPI($symbol);
	if ($values['quotes']['quote']['prevclose'] == 'null' or $values == False) {
		echo "Error: The Tradier API is experiencing technical difficulties, no transactions can be made at this time!";
		exit(); 

	} else {

		$email = $_SESSION['email'];
		$type = "Sold";
		$company = $values['quotes']['quote']['description'];
		$price = $values['quotes']['quote']['prevclose']; 
		$date = date_default_timezone_set("America/Chicago");
		$date = date("D, m-d-Y");
		$time = date_default_timezone_set("America/Chicago");
		$time = date("H:i");
	}


	class MyDB extends SQLite3 {
		function __construct() {
			$this->open('../Model/database.db');
		}
	}

	$db = new MyDB();


	// Stock Table
	$query = "SELECT * FROM Stock WHERE email='" . $email . "';";
	$result = $db->query($query);
	while ($row = $result->fetchArray()) {
		if (($row['email'] == $email) and ($row['symbol'] == $symbol )) {
			$updated_stock = $row['stock'] - $sold;
			if ($updated_stock >= 0) { 
				$query = "UPDATE Stock 
						  SET stock=" . $updated_stock ." 
						  WHERE email='" . $email . "' AND symbol='" . $symbol . "';";
				$db->query($query);
			} else {
				$db->close();
				?><script type="text/javascript">
				alert("You do not own enough stock for this transaction.");
				window.location.href = "../View/menu.php";
				</script><?php
				exit();
			}
		}
	} 
	
	// Update the balance
	$query = "SELECT balance FROM Users WHERE email='" . $email . "';";
	$result = $db->query($query);
	$row = $result->fetchArray();
	$_SESSION['balance'] = $row['balance'] + $price * $sold;
	$query = "UPDATE Users SET balance=" . $_SESSION['balance'] . " WHERE email='" . $email . "';";
	$result = $db->query($query);

	// Append the new transaction into the History table
	$query = "INSERT INTO History VALUES (
								 '" . $email . "',
								 '" . $type . "', 
								 '" . $company .  "',
								 '" . $symbol .  "', 
								 " . $price .  ", 
								 '" . $date .  "', 
								 '" . $time .  "',
								 " . $sold . ");";
	$db->query($query);
	$db->close();
	?><script type="text/javascript">
	alert("Stock successfully sold!");
	window.location.href = "../View/menu.php";
	</script><?php
	exit();  
	
?>