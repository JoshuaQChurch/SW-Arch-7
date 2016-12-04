<?php

	@session_start();
	class MyDB extends SQLite3 {
		function __construct() {
			$this->open('../Model/database.db');
		}
	}

	$db = new MyDB();
	$query = "SELECT * FROM History WHERE email='" . $_SESSION['email'] . "';";
	$result = $db->query($query);
	$numRows = 0;
	while ($result->fetchArray()) {
		$numRows++;
	}

	if ($numRows > 0) {
			echo "<table class='table table-hover'>";
			echo "<tr>";
			echo "<th class='col-md-1'>Transaction Type</th>";
			echo "<th class='col-md-1'>Company</th>";
			echo "<th class='col-md-1'>Symbol</th>";
			echo "<th class='col-md-1'>Stock Price</th>";
			echo "<th class='col-md-1'>Date</th>";
			echo "<th class='col-md-1'>Time</th>";
			echo "<th class='col-md-1'>Stock Amount</th>";
			echo "</tr>";
			echo "</table>";
	
		while ($row = $result->fetchArray()) {
			echo "<table class='table table-hover' style='overflow: auto;'>";
			echo "<tr>";
			echo "<td class='col-md-1'>" . $row['type'] . "</td>";
			echo "<td class='col-md-1'>" . $row['company'] . "</td>";
			echo "<td class='col-md-1'>" . $row['symbol'] . "</td>";
			echo "<td class='col-md-1'>$" . $row['price'] . "</td>";
			echo "<td class='col-md-1'>" . $row['date'] . "</td>";
			echo "<td class='col-md-1'>" . $row['time'] . "</td>";
			echo "<td class='col-md-1'>" . $row['stock'] . "</td>";
			echo "</tr>";
			echo "</table>";
		}

		echo "</table>";

	} else {
		echo "<h2>You seem to have no past history.</h2> <br><br>";
	}

?>

