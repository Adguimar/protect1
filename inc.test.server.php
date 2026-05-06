<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 
    include 'conn.php';
?>

<?php echo $_SESSION['abrirsite']; ?> - abrirsite<br><br>
<?php echo $_SESSION['abrirsitetoken']; ?> - abrirsitetoken<br><br>
<?php echo $_SESSION['apertoubotao']; ?> - apertoubotao<br><br>
<?php echo $_SESSION['timeout']; ?> - timeout<br><br>
<?php echo $_SESSION['clientip']; ?> - clientip<br><br>
<?php echo $_COOKIE['langsite']; ?> - langsite<br><br>
<?php echo time(); ?> - time();<br><br>
<?php echo 'Versão Atual do PHP: ' . phpversion(); ?><br><br>
<?php printf("Versão Atual do MySQL: %s\n", mysqli_get_client_info()); ?>
<br><br>
<br><br>
<?php echo $_COOKIE["LiberaFunctionAd"]; ?> - CookieTimeout<br><br>
