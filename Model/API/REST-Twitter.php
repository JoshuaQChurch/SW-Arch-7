<?php
	$symbol = "$";
	$symbol = $symbol . strtoupper($_REQUEST['symbol']);
	require "twitteroauth/autoload.php";
	use Abraham\TwitterOAuth\TwitterOAuth;

	$consumer_key = "0uiAhp4h2LhOcSTczK3yIDbZU"; 
	$consumer_secret = "20YS8SCNQiW2pWGsaiNnRz5MxPBMFzhKIuTg8zsGuEo6CZO8P9"; 
	$access_token = "346694276-Bb2SOpj7vs9l5YIfieQEqebkU4qPq3daBvhMdo91"; 
	$access_token_secret = "nLuSClFcxwDDpQCQz634qaw3lul7fI4UqJDkrXBHynFjn"; 

	function getConnectionWithAccessToken($cons_key, $cons_secret, $oauth_token, $oauth_token_secret) {
	  $connection = new TwitterOAuth($cons_key, $cons_secret, $oauth_token, $oauth_token_secret);
	  return $connection;
	}

	$connection = getConnectionWithAccessToken($consumer_key, $consumer_secret, $access_token, $access_token_secret);

	$tweets = $connection->get("search/tweets", ["q" => $symbol]);
	$tweets = json_encode($tweets);
	echo $tweets;

?>

