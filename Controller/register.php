<?php
	$first = $_REQUEST['first'];
	$last = $_REQUEST['last'];
	$email = $_REQUEST['email'];
	$password = $_REQUEST['password'];
	$balance = 0;

	class MyDB extends SQLite3
	{
		function __construct()
		{
			$this->open('../Model/database.db');
		}
	}
	
	$db = new MyDB();


	$exists = <<<EOF
		SELECT * FROM Users;
EOF;


	$sql =<<<EOF
		INSERT INTO Users 
		VALUES ('$first','$last','$email','$password','$balance');
EOF;

	$create =<<<EOF
		CREATE TABLE Users(
			first TEXT,
			last TEXT,
			email TEXT,
			password PASSWORD,
			balance REAL
		);

		CREATE TABLE History(
			email TEXT,
			type TEXT,
			company TEXT,
			symbol TEXT,
			price REAL, 
			date TEXT,
			time TEXT,
			stock INTEGER
		); 

		CREATE TABLE Stock(
			email TEXT,
			company TEXT,
			symbol TEXT,
			stock INTEGER
		); 
EOF;


	// Ensure Database Exist
	if (@$db->exec($exists)) {

		if (doesNotExist($email, $db)) {
			include ('../Model/API/REST-Mailboxlayer.php');
			if (@Mailboxlayer($email)) {
				addEntry($db, $sql, $first, $last, $email, $password, $balance);
			} else {
				$db->close();
				?><script type="text/javascript">
				alert("ERROR: The email provided is invalid.");
				window.location.href = "../View/index.html";
				</script><?php
				exit();
			}
		
		} else {
					
			$db->close();
			?><script type="text/javascript">
			alert("ERROR: This email already exists within our system.");
			window.location.href = "../View/index.html";
			</script><?php
			exit();
		}

	// Create the tables and populate. 
	} else {
		$db->exec($create);
		addEntry($db, $sql, $first, $last, $email, $password, $balance);
		
	}
	
	function addEntry($db, $sql, $first, $last, $email, $password, $balance) {
		$db->exec($sql);
		$db->close();
		?><script type="text/javascript">
		alert("Account Successfully Created! Click close to go back and log in.");
		window.location.href = "../View/index.html";
		</script><?php
		exit();
	}

	// Verify email doesn't alread exist in database
	function doesNotExist($email, $db) {
		$value = TRUE;
		$query = "SELECT email FROM Users WHERE email='" . $email . "'";

		$result = $db->query($query) or die('Query failed');
		while ($row = $result->fetchArray()) {
			if ($email == $row['email']) {
  				$value = FALSE;
			}

		}
		return $value;
	}
?>