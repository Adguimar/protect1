<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 

if(!empty($_GET["token"])) {
  if(isset($_SESSION['abrirsite'])){
    $_SESSION['abrirsite'] = '1';
    $_SESSION['abrirsitetoken'] = $_GET['token'];
    unset($_SESSION['apertoubotao']);
  }else {
    $_SESSION['abrirsite'] = '1';
    $_SESSION['abrirsitetoken'] = $_GET['token'];
    unset($_SESSION['apertoubotao']);
  }
  }
?>
<a id="link_ir" href="https://fazercurriculo.online/instagram/" title="Ir para o artigo!" rel="dofollow">link</a>
<script type="text/javascript">
document.getElementById("link_ir").click();
</script>