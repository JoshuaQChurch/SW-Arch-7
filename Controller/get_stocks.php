<?php

	@session_start();

	$db = new MyDB();
	$query = "SELECT * FROM Stock WHERE email='" . $_SESSION['email'] . "';";
	$result = $db->query($query);
	$numRows = 0;
	while ($result->fetchArray()) {
		$numRows++;
	}

	if ($numRows > 0) {
			echo "<table class='table table-hover'>";
			echo "<tr>";
			echo "<th>Company</th>";
			echo "<th>Symbol</th>";
			echo "<th>Total Owned</th>";
			echo "<th>Amount to Sell</th>";
			echo "</tr>";
			
	
		while ($row = $result->fetchArray()) {
			if ($row['stock'] > 0) {
				echo "<tr>";
				echo "<td>" . $row['company'] . "</td>";
				echo "<td>" . $row['symbol'] . "</td>";
				echo "<td>" . $row['stock'] . "</td>";
				echo "<td><form action='../Controller/sell_stocks.php'><input style='width: 50%' type='number' step='1' min='1' max='" . $row['stock'] . "' name='sold' class='form-control' placeholder='Enter Amount' required></td>";
				echo "<input id='sell-symbol' style='display: none' name='symbol' value='" . $row['symbol'] . "'>";
				echo "<td><input id='sell-button' style='width: 50%; padding-right:15px; padding-left: 15px; text-align: center;' value='Sell' type='submit' class='btn btn-primary'></form></td>";
				echo "</tr>";
			} 
		}

		echo "</table>";

	} else {
		echo "<h2>You currently own no stock.</h2> <br><br>";
	}

?>

