<?php
    if(!isset($_SESSION)) 
    { 
        session_start(); 
    } 
define('LANG_PORTUGUESE', 'pt');
define('LANG_ENGLISH', 'en');
define('LANG_RUSSIAN', 'ru');
define('LANG_SPANISH', 'es');
define('LANG_INDIAN', 'hi');
// Look for l in query string and set as language.
$language = isset($_COOKIE['langsite']) ? $_COOKIE['langsite'] : LANG_PORTUGUESE;
/**
 * Translate a string
 * Use the $translate variable to define your set of language translations.
 * Note: Based off of Drupal's t() function.
 *
 * @param $string
 *  The string that is to be translated.
 * @param $args
 *  An array of placeholders that will populate the translated string.
 * @param $langcode
 *  The language you wish to translate the string to.
 */
function t($string, $args = array(), $langcode = NULL) {
  global $language, $translation;

  // Set language code.
  $langcode = isset($langcode) ? $langcode : $language;

  // Search for a translated string.
  if ( isset($translation[$langcode][$string]) ) {
    $string = $translation[$langcode][$string];
  }

  // Replace arguments if present.
  if ( empty($args) ) {
    return $string;
  } else {
    foreach ( $args as $key => $value ) {
      switch ( $key[0] ) {
        case '!':
        case '@':
        case '%':
        default: $args[$key] = $value; break;
      }
    }

    return strtr($string, $args);
  }
}

$translation['pt'] = array(
  'Download' => 'Baixar',
  'Tente Novamente' => 'Tente Novamente',
  'Download Bloqueado!' => 'Download Bloqueado!',
  'Para desbloquear, por favor, clique na propaganda abaixo.' => 'Para desbloquear, por favor, clique na propaganda abaixo.',
  'Carregando ...' => 'Carregando ...',
  'ATENÇÃO:' => 'ATENÇÃO:',
  'Se você for redirecionado, basta voltar a página anterior.' => 'Se você for redirecionado, basta voltar a página anterior.',
  'Desenvolvido por' => 'Desenvolvido por',
  'Muito Bem!' => 'Muito Bem!',
  'Download esta Pronto!' => 'Download esta Pronto!',
  'Clique em alguma propaganda,' => 'Clique em alguma propaganda,',
  'Atualize esta página e/ou acesse novamente,(ou faça conforme a imagem a baixo)' => 'Atualize esta página e/ou acesse novamente,(ou faça conforme a imagem a baixo)',
  'Após isso, Todos os outros downloads serão liberados sem propaganda.' => 'Após isso, Todos os outros downloads serão liberados sem propaganda.',
  'Proibido downloads simultâneos! Tente novamente em alguns segundos.' => 'Proibido downloads simultâneos! Tente novamente em alguns segundos.',
);

$translation['en'] = array(
  'Download' => 'Download',
  'Tente Novamente' => 'Try Again',
  'Download Bloqueado!' => 'Download Blocked!',
  'Para desbloquear, por favor, clique na propaganda abaixo.' => 'To unlock, please click on the advertisement below.',
  'Carregando ...' => 'Loading ...',
  'ATENÇÃO:' => 'ATTENTION:',
  'Se você for redirecionado, basta voltar a página anterior.' => 'If you is redirected, just go back to the previous page.',
  'Desenvolvido por' => 'Developed by',
  'Muito Bem!' => 'Very well!',
  'Download esta Pronto!' => 'Download is Ready!',
  'Clique em alguma propaganda,' => 'Click on any advertisement,',
  'Atualize esta página e/ou acesse novamente,(ou faça conforme a imagem a baixo)' => 'Please refresh this page and / or access again, (or make as the image below)',
  'Após isso, Todos os outros downloads serão liberados sem propaganda.' => 'After that, all other downloads were released without any advertisement.',
  'Proibido downloads simultâneos! Tente novamente em alguns segundos.' => 'Prohibited simultaneous downloading! Please try again in a few seconds.',
);

$translation['ru'] = array(
  'Download' => 'Скачать',
  'Tente Novamente' => 'Попробуйте еще раз',
  'Download Bloqueado!' => 'Скачать заблокирован!',
  'Para desbloquear, por favor, clique na propaganda abaixo.' => 'Чтобы разблокировать, пожалуйста, нажмите на объявление ниже.',
  'Carregando ...' => 'Загрузка ...',
  'ATENÇÃO:' => 'ВНИМАНИЕ:',
  'Se você for redirecionado, basta voltar a página anterior.' => 'Если вы перенаправлены, просто вернитесь на предыдущую страницу.',
  'Desenvolvido por' => 'Разработано',
  'Muito Bem!' => 'Отлично!',
  'Download esta Pronto!' => 'Загрузка готова!',
  'Clique em alguma propaganda,' => 'Нажмите на любую рекламу,',
  'Atualize esta página e/ou acesse novamente,(ou faça conforme a imagem a baixo)' => 'Пожалуйста, обновите эту страницу и / или получите доступ снова (или сделайте изображение ниже)',
  'Após isso, Todos os outros downloads serão liberados sem propaganda.' => 'После этого все остальные загрузки были выпущены без рекламы.',
  'Proibido downloads simultâneos! Tente novamente em alguns segundos.' => 'Запрещено одновременное скачивание! Пожалуйста, попробуйте снова через несколько секунд.',
);

$translation['es'] = array(
  'Download' => 'Descargar',
  'Tente Novamente' => 'Intentar Nuevamente',
  'Download Bloqueado!' => 'Descargar Bloqueado!',
  'Para desbloquear, por favor, clique na propaganda abaixo.' => 'Para desbloquear, por favor haga clic en el anuncio abajo.',
  'Carregando ...' => 'Cargando ...',
  'ATENÇÃO:' => '¡ATENCIÓN!:',
  'Se você for redirecionado, basta voltar a página anterior.' => 'Si está redirigido, vuelva a la página anterior.',
  'Desenvolvido por' => 'Desarrollado por',
  'Muito Bem!' => '¡Muy bien!',
  'Download esta Pronto!' => '¡La descarga está lista!',
  'Clique em alguma propaganda,' => 'Haga clic en alguna propaganda,',
  'Atualize esta página e/ou acesse novamente,(ou faça conforme a imagem a baixo)' => 'Actualiza esta página y / o accede de nuevo, (o haz según la imagen abajo)',
  'Após isso, Todos os outros downloads serão liberados sem propaganda.' => 'Después de eso, Todas las demás descargas se liberaron sin publicidad.',
  'Proibido downloads simultâneos! Tente novamente em alguns segundos.' => '¡Prohibido descargas simultáneas! Intente de nuevo en unos segundos.',
);

$translation['hi'] = array(
  'Download' => 'डाउनलोड',
  'Tente Novamente' => 'फिर से कोशिश करें',
  'Download Bloqueado!' => 'डाउनलोड अवरुद्ध!',
  'Para desbloquear, por favor, clique na propaganda abaixo.' => 'अनलॉक करने के लिए, कृपया नीचे दिए गए विज्ञापन पर क्लिक करें।',
  'Carregando ...' => 'लोड हो रहा है ...',
  'ATENÇÃO:' => 'ध्यान:',
  'Se você for redirecionado, basta voltar a página anterior.' => 'यदि आपको पुनर्निर्देशित किया गया है, तो पिछले पृष्ठ पर वापस जाएं।',
  'Desenvolvido por' => 'द्वारा विकसित',
  'Muito Bem!' => 'बहुत अच्छा!',
  'Download esta Pronto!' => 'डाउनलोड तैयार है!',
  'Clique em alguma propaganda,' => 'किसी भी विज्ञापन पर क्लिक करें,',
  'Atualize esta página e/ou acesse novamente,(ou faça conforme a imagem a baixo)' => 'कृपया इस पृष्ठ को ताज़ा करें और / या फिर से एक्सेस करें, (या नीचे की छवि बनाएं)',
  'Após isso, Todos os outros downloads serão liberados sem propaganda.' => 'उसके बाद, अन्य सभी डाउनलोड बिना किसी विज्ञापन के जारी किए गए।',
  'Proibido downloads simultâneos! Tente novamente em alguns segundos.' => 'एक साथ डाउनलोड निषिद्ध! कृपया कुछ सेकंड में पुनः प्रयास करें।',
);

?>
