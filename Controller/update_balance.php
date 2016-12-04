<?php

	session_start();
	$value = $_REQUEST['value'];
	class MyDB extends SQLite3 {
		function __construct() {
			$this->open('../Model/database.db');
		}
	}

	$db = new MyDB();
	$query = "SELECT balance FROM Users WHERE email='" . $_SESSION['email'] . "';";
	$result = $db->query($query);
	$row = $result->fetchArray();
	$_SESSION['balance'] = $row['balance'] + $value;
	$query = "UPDATE Users SET balance=" . $_SESSION['balance'] . " WHERE email='" . $_SESSION['email'] . "';";
	$result = $db->query($query);
	?><script type="text/javascript">
	alert("Deposit was successful!");
	window.location.href = "../View/menu.php";
	</script><?php
	exit();

?>

