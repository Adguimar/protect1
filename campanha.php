<?php

    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 

include 'conn.php';


// Links Random
$a = [
  "$pagina_site1",
  "$pagina_site2",
  "$pagina_site3",
  "$pagina_site4",
  "$pagina_site5"
];
$website = $a[mt_rand(0, count($a) - 1)];

// Sorteio Protetor de CTR Porcentagem
$random = rand(1,100);
if(empty($_COOKIE["PrimeiroAcesso"])) {
  if ($random <= $porcentagem_desbloqueio)
    {
        setcookie("LiberaFunctionAd", "1", time()+$session_timeout_cookie_free);
    } 
else 
    {
      
    }
    }

 if(!empty($_GET["token"])) {

  $_SESSION['abrirsite'] = '1';
  $_SESSION['apertoubotao'] = '0';
  $_SESSION['clientip'] = $_SERVER['REMOTE_ADDR'];
  $_SESSION['abrirsitetoken'] = $_GET['token'];

//Verificar se existe cookie
//Se o cookie existir, pegar o idioma do cookie
if(isset($_COOKIE['langsite'])) {
header("Location: $website");
}
//Se não, verificar o idioma
else {
//Qual é a sua língua?
$idioma = substr($_SERVER['HTTP_ACCEPT_LANGUAGE'],0,2);
//Se não houver nenhuma lingua pre-definida, definir inglês como padrão
if($idioma != "pt" && $idioma != "en" && $idioma != "es") { 

setcookie("langsite", "pt", time()+31536000);
header("Location: $website");
}

setcookie("langsite", $idioma, time()+31536000);
header("Location: $website");
}


} else {

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
<?php
}
?>