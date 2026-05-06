<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 
	include('inc.language.php');

	if ( isset( $_SESSION["abrirsite"] )  == '1' ){
		include 'conn.php';
		$token = $_SESSION["abrirsitetoken"];
		$ids = $token;
		$sql = "SELECT * FROM urls WHERE i='$ids'";
		$qsl = mysqli_query($conn, $sql);
		$url = mysqli_fetch_assoc($qsl);
		$conta = mysqli_num_rows($qsl);



	}

	if(empty($_COOKIE["PrimeiroAcesso"])) {

    setcookie("PrimeiroAcesso", "1", time()+2592000);
    
    }

$str = $_SESSION['abrirsitetoken'];
?>
<script type="text/javascript">
function atualizar2()
        {
            $.get("<?php echo $site_url_index ?>clicks.php?clicks=1", function( data ) {
            $('#open2').html(data);
            });
        }
</script>
<script type='text/javascript'>
$('div.DivLinkConverter').find('a').addClass('ClassLinkConverter');
$('.ClassLinkConverter').each(
    function(){
    var link64 = atob("<?php echo $_SESSION['abrirsitetoken']; ?>");     
    var linkcr = CryptoJS.AES.decrypt(link64, "391si8WU89ghkDB5");
    var plaintext = linkcr.toString(CryptoJS.enc.Utf8);

    $(this).attr("href", plaintext ); 

    $(this).attr("target","_blank");
    }
    

)
</script>
<!-- Sucess -->
<div class="download">

<div id="DivLinkConverter" Class="DivLinkConverter">
<p><font class="alert3" role="alert"><?php print t('Download esta Pronto!'); ?> <i class="fas fa-check"></i></font></p>
<p><a href="#" class="DownloadButOn" onclick="atualizar2();"><?php print t('Download'); ?> <i class="fa fa-download"></i></a></p>
</div>

</div>
<?php
session_destroy();
?>