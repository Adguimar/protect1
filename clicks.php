<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 
    
	if (isset($_GET['clicks'])) {
		include 'conn.php';
		$date = date('Y-m-d');
		$token = $_SESSION["abrirsitetoken"];

		$con2 = mysqli_connect($servidor, $usuario, $senha, $basename);
	  $sqlverific = mysqli_query($con2, "SELECT * FROM visitantes_clicks_total WHERE data = '{$date}' AND token = '{$token}'") or print mysql_error();

		if(mysqli_num_rows($sqlverific)>0) {
			$sqlcount = "UPDATE `urls` SET  `clicks`=`clicks`+1, `data` =  '$date' WHERE i='$token'";
		  $qsl = mysqli_query($conn, $sqlcount);

			$sqlcount1 = "UPDATE `visitantes_clicks_total` SET  `downloads`=`downloads`+1 WHERE token='$token' AND data = '$date'";
		 $qsl1 = mysqli_query($conn, $sqlcount1);

		} else if (isset($_GET['clicks'])) {
	    $sqlcount = "UPDATE `urls` SET  `clicks`=`clicks`+1, `data` =  '$date' WHERE i='$token'";
			$qsl = mysqli_query($conn, $sqlcount);
	    $sqlcount1 = "INSERT INTO `visitantes_clicks_total`(`downloads`, `data`, `token`) VALUES (1,'$date','$token')";
	    $qsl1 = mysqli_query($conn, $sqlcount1);

	}

	}
	session_destroy();
?>
