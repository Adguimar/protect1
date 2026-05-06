<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 
include 'conn.php';


if ( isset( $_GET["rti"] )  == '1' ){
  unset($_SESSION['clientip']);
}

if ( isset( $_GET["bt"] )  == '1' ){

setcookie("LiberaFunctionAd", "1", time()+$session_timeout_cookie);
}
?>
