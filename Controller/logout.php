<?php
	session_start();
	session_unset();  
	session_destroy(); 
	?><script type="text/javascript">
	alert("You have successfully logged out. Click close to return main menu.");
	window.location.href = "../View/index.html";
	</script><?php
	exit();

?>
