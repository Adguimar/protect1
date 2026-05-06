<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 
include('inc.language.php');

 include 'conn.php';

?>
<?php
if ( isset( $_SERVER['REMOTE_ADDR'] )  == $_SESSION["clientip"] ){
unset($_SESSION['clientip']);
?>

<body style="background: rgba(27, 51, 15, 0.75);">
<div class="alert alert-danger" role="alert" style="width: 100%;text-align: center;margin-top: 10%;"><i class="fa fa-exclamation-triangle fa-2x pull-center"></i>
<b><?php print t('ATENÇÃO:'); ?></b> <?php print t('Proibido downloads simultâneos! Tente novamente em alguns segundos.'); ?>
</div>
<div class="main" style="display: none;">
<?php
}else if ( isset( $_SESSION["abrirsite"] )  == '1' ){
  $_SESSION['clientip'] = $_SERVER['REMOTE_ADDR'];
	header("Location: ".$site_url_system."campanha.php?token=".$_SESSION['abrirsitetoken']."");
} else {
  header("Location: ".$site_url_system."");
}
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title><?php echo $nome_do_site ?></title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="robots" content="noindex, nofollow">
<meta content="width=device-width, initial-scale=0.8" name="viewport">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<link href='//netdna.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css' rel='stylesheet'/>
</head>
<body>

</body>
</html>