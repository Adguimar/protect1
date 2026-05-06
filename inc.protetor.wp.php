<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 

 if ( isset( $_SESSION["abrirsite"] )  == '1' ){

 include 'div.php';

}else{

 wp_head();
 
}
?>