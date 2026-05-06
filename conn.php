<?php
//    __  __                            _                _____                                         
//   |  \/  |                          (_)              / ____|                                        
//   | \  / |  __ _   __ _   __ _  ____ _  _ __    ___ | |  __   ___   _ __ ___   _ __ ___    ___  ____
//   | |\/| | / _` | / _` | / _` ||_  /| || '_ \  / _ \| | |_ | / _ \ | '_ ` _ \ | '_ ` _ \  / _ \|_  /
//   | |  | || (_| || (_| || (_| | / / | || | | ||  __/| |__| || (_) || | | | | || | | | | ||  __/ / / 
//   |_|  |_| \__,_| \__, | \__,_|/___||_||_| |_| \___| \_____| \___/ |_| |_| |_||_| |_| |_| \___|/___|
//                    __/ |                                                                            
//                   |___/                                                                             
  
     /////////////////////////////
    // Dados do Servidor MySQL //
   /////////////////////////////

	$servidor = "localhost"; // IP/HOST MySQL
	$usuario = "admin_usandoappsa"; //Usuário MySQL
	$senha = "Pt_159753"; //Senha MySQL
	$basename = "admin_usandoapp"; //Banco de Dados no MySQL

	 /////////////////////////////
    // Configurações do Script //
   /////////////////////////////
   
    //URL da página inicial do seu site onde está hospedado o Protector System. coloque exatamente assim -> Ex: http://www.meusite.com/
    $site_url_index = 'https://fazercurriculo.online/'; 

    //URL do primeiro site que você usará o Redirecionamento -> Ex: http://www.meusiteredireciona.com/redirecionamento
    //Se você não usa redirecionamentos, deixa-o igual a configuração do link acima ($site_url_index) porém com "/recebe/"
    //Exemplo: http://meuprotetor.com/recebe/
    $site_url_index_redir = 'https://portalmaromba.xyz/nova/campanha/'; 

    //Seu Site é WordPress? Coloque: "1 = Sim" / "0 = Não"
    //ATENÇÃO: esta configuração se for incorreta, o script não irá funcionar!!! Portanto, se você tem um site wordpress coloque "1", caso contrário, o Padrão é "0"
    $site_wordpress = '1'; // "Padrão: 0"
    
    //Coloque aqui a URL do seu Logotipo
	$url_logotipo = "https://fazercurriculo.online/img/logo.png"; 

	//Coloque aqui o nome do seu site
	$nome_do_site = "Caso seja redirecionado clique em voltar"; 

	//Coloque aqui o url do favicon do seu site
	//Caso você queira um favicon externo, Você pode alterar por esta opção -> $favico_site = "https://www.meusite.com/img/favicon.png";
	$favico_site = "".$site_url_index."favicon.ico"; 

	// ID do site de estatísticas, Crie seu ID em -> https://whos.amung.us/
	$id_whos_amung_us = "mhbnjalax7";

	 /////////////////
    // Cronometros //
   /////////////////

    //Tempo para mostrar botão download sem clicar no anúncio (Em Segundos) - "Padrão: 60"
	$tempomostrar = "60"; 

	//Tempo de espera, para aparecer o botão download após clicar no anúncio (Em Segundos) - "Padrão: 15"
	$tempomostrar1 = "0"; 
    
    //Tempo em que o token fica disponível, após este tempo o token expira e o botão de download é inválido (Em Segundos) - "Padrão: 90"
	$tempotoken = "90"; 

	//Tempo para liberar acessos simultêneos (Em Segundos) - "Padrão: 10"
	$tempoip = "10"; 

     /////////////////////
    // Controle de CTR //
   /////////////////////

    // ATENÇÃO, ESTA CONFIGURAÇÃO É MUITO IMPORTANTE, ELA QUEM VAI CONTROLAR O CTR DO GOOGLE ADSENSE E PREVINIR QUE SUA CONTA NÃO SEJA BANIDA!

    // Funciona assim: O Usuário na sua primeira visita, é obrigado a clicar no seu anúncio, que irá gerar um cookie, então ele só será obrigado a clicar novamente no anúncio daqui a 10 dias seguindo o padrão a baixo.
    
    // Para configurar, coloque a quantidade de dias desejado em segundos (calcule no google ele mostra na página inicial), recomendamos Min: 518400 - 6 dias, e Max: 864000 - 10 dias
    // Este será então o Tempo para Bloquear a página novamente, ou seja, tempo para exigir clicks nos anúncios para a mesma pessoa que acessou antes (Em Segundos) - Padrão: 864000 (864000 = 10 dias)
	$session_timeout_cookie = "864000";

    // Porcentagem de chance que o usuário tem, de NÃO ser obrigado a clicar no anúncio na primeira visita em seu site
    // Padrão: 65% = "65"
	$porcentagem_desbloqueio = "100";

	// Tempo em "Segundos", que a página ficará livre para usuário acessar SEM ser obrigado a clicar no anúncio, ou seja, após esse tempo quando acessar novamente ele será obrigado a clicar no anúncio.
	// Padrão: 60 Segundos = "60"
	$session_timeout_cookie_free = "60";

	   // OBS: ESSAS SÃO AS CONFIGURAÇÕES PADRÕES DE CONTROLE DE CTR MAIS SEGURAS E RECOMENDADA POR NÓS, SE VOCÊ DESEJA ALTERAR, LEMBRE-SE, ALTERE AS CONFIGURAÇÕES POR SUA CONTA E RISCO, NÃO NOS RESPONSABILIZAMOS PELO MAL USO DESTE SCRIPT !!!!!!

       // AS CONFIGURAÇÕES PODEM VARIAR DE SITE PARA SITE, E DE TRAFEGO PARA TRAFEGO, PORTANTO FIQUE DE OLHO NO SEU ADSENSE, SE AS TAXAS DE CTR FICAREM ALTAS, RECOMENDAMOS QUE AUMENTE A CONFIGURAÇÃO: "porcentagem_desbloqueio". (QUANTO MAIOR, MAIS SEGURO. PORÉM QUANTO MENOR, MENOS SEGURO!!)

     /////////////////////////////////////////////////
    // Configuração das Páginas a serem camufladas //
   /////////////////////////////////////////////////

	// Aqui, coloque 5 URLs de 5 páginas aleatorias de seu site, tem que ser como neste exemplo "www.meusite.com/minha-pagina"  ou "www.meusite.com/index.php?pagina=1"
	$pagina_site1 = 'https://fazercurriculo.online/?redirect_to=random'; //URL de alguma página do seu site
	$pagina_site2 = 'https://fazercurriculo.online/?redirect_to=random'; //URL de alguma página do seu site
	$pagina_site3 = 'https://fazercurriculo.online/?redirect_to=random'; //URL de alguma página do seu site
	$pagina_site4 = 'https://fazercurriculo.online/?redirect_to=random'; //URL de alguma página do seu site
	$pagina_site5 = 'https://fazercurriculo.online/?redirect_to=random'; //URL de alguma página do seu site


     ///////////////////////////////
    // Configuração dos anúncios //
   ///////////////////////////////
 
    // As configurações de anúncios mudou, agora se encontra no painel administrativo do protetor.
    // Acesse: seusite.com/admin - Menu Lateral Direito, no Canto Superior de cor azul, um menu suspenso onde você encontra opções administrativas, incluindo a configuração dos anúncios. NÃO ESQUEÇA DE DESATIVAR SEU AD-BLOCK PARA TESTES.

	//////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////

	//!!! DE AGORA EM DIANTE, POR FAVOR, NÃO ALTERAR ESSAS CONFIGURAÇÕES, FAZEM PARTE DO SISTEMA !!!!
	$usuariomysql = $usuario; //(NÃO ALTERAR)
	$senhamysql = $senha; //(NÃO ALTERAR)
	$servidormysql = $servidor; //(NÃO ALTERAR)
	$basenamemysql = $basename; //(NÃO ALTERAR)
	$site_url_system = ''.$site_url_index.''; //(NÃO ALTERAR)
	$site['url'] = ''.$site_url_system.'redir.php'; //(NÃO ALTERAR)
	$site2['url'] = ''.$site_url_index_redir.''; //(NÃO ALTERAR)
	$session_timeout_seg = "60"; //(NÃO ALTERAR)
	$vsystem = "MasterV3.0"; //(NÃO ALTERAR)



	global $site;

	$conn = mysqli_connect($servidor, $usuario, $senha, $basename);

	mysqli_set_charset($conn, 'utf8');
	date_default_timezone_set("America/Sao_Paulo");
	setlocale(LC_ALL, 'pt_BR');
?>