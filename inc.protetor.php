<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 

 if ( isset( $_SESSION["abrirsite"] )  == '1' ){

 include 'div.php';

?>
<script type='text/javascript'>
document.write('<style type="text/undefined">');
</script>
<?php
}

?>