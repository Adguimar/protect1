<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<title>Meu Site</title>
<!--===== Coloque o include a baixo (inc.protetor.php), 1 linha depois da tag </title> ========-->
<?php include("inc.protetor.php"); ?>

<!-- Se seu site for WordPress, coloque no header.php do seu tema, no lugar da function "wp_head();"
include("inc.protetor.wp.php");
-->

<!-- ===== 
Script jQuery Source
Adiciona estes 2 jquerys entre as tags <head> e </head> 
Coloque-os na ordem a baixo:
  ===== -->
<!-- 1° -> Coloque este sempre acima de todos ".js" -->
<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<!-- 2° -> Coloque este por ultimo -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.2/rollups/aes.js"></script>
</head>
<body>

<!-- ===== Alguns Exemplos de links ===== -->


<a href="https://mega.nz/">Mega</a><br>
<a href="https://www.4shared.com/">4shared</a><br>
<a href="https://drive.google.com/">Google Drive</a><br>



<!-- ===== 
Coloque o script a baixo 1 linha antes da tag </body> 

Não esqueça de alterar:

var redirectpage = "http://localhost/recebe/";

Modifique para o endereço do site onde está o protetor de links, ou para o redirecionamento que leve até o site que está o Protetor.

Depois, é só ir colocando e alterando os links predefinidos da lista do script a baixo, conforme os que você usa em seu site e deseja converter automaticamente.

Coloque o URL do site com "HTTP" e com "HTTPS"
===== -->

<!-- =====  INICIO - Script URL-Converter By: MagazineGommez ===== -->
<script type='text/javascript'>
var redirectpage = "http://localhost/recebe/";
(()=> {
const urlsBases=[
  'https://docs.google.com/',
  'http://mega.gratis/',
  'https://uploadbr.com/',
  'https://mega.nz/',
  'https://www.theanonfiles.com/',
  'https://letsupload.co/',
  'https://www.4shared.com/',
  'http://www.4shared.com/',
  'https://1fichier.com/',
  'https://archive.org/',
  'https://oload.tv/',
  'http://www.mediafire.com/',
  'http://uptobox.com/',
  'https://racaty.com/',
  'http://www.turbobit.org/',
  'https://brfiles.com',
  'https://megaup.net/',
  'https://minhateca.com.br/',
  'https://www.zippyshare.com/',
  'http://zippyshare.com/',
  'http://dl.free.fr/',
  'https://drive.google.com/',
  'https://sendit.cloud/',
  'https://rapidgator.net/',
  'https://mega.co.nz/',
  'http://ul.to/',
  'https://www.sendspace.com/',
  'https://www.mediafire.com/',
  'http://uploaded.net/',
  'https://depositfiles.com/',
  'https://www.filefactory.com/',
  'https://www.brupload.net/',
  'http://www.brupload.net/',
  'https://userscloud.com',
  'https://openload.co/',
  'https://usersdrive.com',
  'https://uptobox.com',
  'http://brfiles.com/',
  'http://adf.ly/',
  'magnet:?xt',
  'magnet:?xt=urn:btih:',
  'magnet'
  ];
for (let urlBase of urlsBases){
const anchors=document.querySelectorAll("a[href*='" + urlBase + "']");
anchors.forEach(el=> {

var LinkOriginal = el.getAttribute("href"); 
var linkcr = CryptoJS.AES.encrypt(LinkOriginal, "391si8WU89ghkDB5");
var link64 = btoa(linkcr);

let urlProtegida="" + redirectpage + "?token=" + link64 + ""

el.setAttribute("href", urlProtegida)
el.setAttribute("target","_blank")
console.log(urlProtegida)
});
}})();</script>
<!-- =====  FIM - Script URL-Converter By: MagazineGommez ===== -->
</body>
</html>