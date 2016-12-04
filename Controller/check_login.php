<?php
	$email = $_REQUEST['email'];
	$password = $_REQUEST['password'];

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
		$query = "SELECT * FROM Users";
		$result = $db->query($query);

		while($row=$result->fetchArray()){
			if ($row['email'] == $email AND $row['password'] == $password) {
				session_start();
				$_SESSION["first"] = $row['first'];
				$_SESSION['last'] = $row['last'];
				$_SESSION['email'] = $row['email'];
				$_SESSION['balance'] = $row['balance'];
				$db->close();
				?><script type="text/javascript">
				alert("Login Successful!");
				window.location.href = "../View/menu.php";
				</script><?php
			} 
		}

		$db->close();
		?><script type="text/javascript">
		alert("These credentials do not exist in our system. Click OK to return.");
		window.location.href = "../View/index.html";
		</script><?php
		exit();

	// Create the tables and populate. 
	} else {
		$db->exec($create);
		$db->close();
		?><script type="text/javascript">
		alert("These credentials do not exist in our system. Click OK to return.");
		window.location.href = "../View/index.html";
		</script><?php
		exit();
		
	}
