<?php
  session_start();
  if ($_SESSION['email'] == '') {
    ?><script type="text/javascript">
    alert("You must login to access this page. Click OK to return to main menu.");
    window.location.href = "index.html";
    </script><?php

  } else if (isset($_SESSION['LAST_ACTIVITY']) && (time() - $_SESSION['LAST_ACTIVITY'] > 1800)) {
      session_unset();     
      session_destroy();  
      ?><script type="text/javascript">
      alert("Due to inactivity, you have been logged out. Please log back in to access this page.");
      window.location.href = "index.html";
      </script><?php
  }

  $_SESSION['LAST_ACTIVITY'] = time(); 

?>

<!DOCTYPE html>
<html lang="en" style="height:100%; min-height: 50vh; min-width: 50vh;">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" type="text/javascript"></script>
    <link rel="stylesheet" type="text/css" href="src/css/menu_style.css" media="screen" />
  </head>

  <body style="height: 100%">
    <nav class="navbar navbar-inverse" >
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#collapse-1" aria-expanded="false">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">Welcome to the Trade Net Brokerage Service, <?php echo $_SESSION['first'];?>!</a>
        </div>

        <div class="collapse navbar-collapse" id="collapse-1">
          <ul class="nav navbar-nav">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Account Management<span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a href="#" onclick="document.getElementById('balance').style.display='block'" style="width:auto;">View Balance / Deposit Funds</a></li>
                <li role="separator" class="divider"></li>
                <li><a href="#" onclick="document.getElementById('transaction').style.display='block'" style="width:auto;">View Transaction History</a></li>
                <li role="separator" class="divider"></li>
                <li><a href="#" onclick="document.getElementById('get-stocks').style.display='block'" style="width:auto;">View / Sell Currently Owned Stocks</a></li>
              </ul>
            </li>
            </ul>
          
          <form class="navbar-form navbar-right" onsubmit="return false">
            <div class="form-group">
              <input id='symbol' type="text" class="form-control" placeholder="Search for Symbol">
            </div>
            <button id="symbol-search" type="submit" class="btn btn-default">Search</button>
          </form>
          <ul class="nav navbar-nav navbar-right">
            <li><a href="../Controller/logout.php">Logout</a></li>
            <li><a href="http://www.advfn.com/nyse/newyorkstockexchange.asp" target='_blank'>List of Available Symbols</a></li>
          </ul>
        </div>
      </div>
    </nav>

      <div id="balance" class="modal">  
        <form class="modal-content animate" method="POST" action="../Controller/update_balance.php" style="display:table; width:0%;">
          <div class="popup">
            <span onclick="document.getElementById('balance').style.display='none'" class="close" title="Close Modal">&times;</span>
          </div>
          <div style="padding: 10px;">
            <label><h2><b>Balance:</b> $<?php echo $_SESSION['balance'];?></h2></label><br>
            <label style="display: block-inline"><h2><b>Add Funds</b></h2><input type="number" step="0.01" min="0" name="value" class="form-control" placeholder="Enter your amount" required></h2></label> 
            <button type="submit" class="btn btn-primary">Deposit</button>
            <button type="button" class="btn btn-danger" onclick="document.getElementById('balance').style.display='none'" class="cancelbtn">Cancel</button>
          </div>
        </form>
      </div>

      <div id="transaction" class="modal">  
        <div class="modal-content animate">
          <div style="padding: 10px">
            <?php include '../Controller/get_history.php';?>
            <button type="button" class="btn btn-danger" onclick="document.getElementById('transaction').style.display='none'" class="cancelbtn">Close</button>
          </div>
        </div>
      </div>

      <div id="get-stocks" class="modal">  
        <div class="modal-content animate">
          <div style="padding: 10px">
            <?php include '../Controller/get_stocks.php';?>
            <button type="button" class="btn btn-danger" onclick="document.getElementById('get-stocks').style.display='none'" class="cancelbtn">Cancel</button>
          </div>
        </div>
      </div>

      <div id='symbol-container' class="container-fluid" style="height:90%; display:none;">
        <div class="row" style="height:100%;">
          <div class="col-md-4 col-sm-6" style="height:100%;">
            <div id='tradier' style="background-color:#e3eaf4; height: 45%; margin-bottom:15px; overflow:auto; padding-left: 15px; padding-right: 15px; padding-bottom: 15px; box-shadow: 5px 5px 5px #505050; border-radius: 6px;"></div>  
            <div id='twitter' style="background-color:#e3eaf4; height: 50%; margin-bottom:15px; overflow:auto; padding: 15px; box-shadow: 5px 5px 5px #505050; border-radius: 6px"></div>
          </div>
          <div class="col-md-8 col-sm-6" style="height:100%">
            <div id='nytimes' style="background-color:#e3eaf4; height:100%; margin-bottom:15px; overflow:auto; padding: 15px; box-shadow: 5px 5px 5px #505050; border-radius: 6px"></div>
          </div>
        </div>
      </div>


    <script type="text/javascript" src="../Controller/api_handler.js"></script>
    <script type="text/javascript" src="../Controller/get_current_price.js"></script>
    <script type="text/javascript" src="../Model/API/REST-Tradier.js"></script>
    <script type="text/javascript" src="../Model/API/REST-NYTimes.js"></script>

  </body>

</html>
