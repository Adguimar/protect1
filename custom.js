// LOADER
$(document).ready(function () {
    "use strict";

    setTimeout(function () {
        $('body').addClass('loaded')
    }, 1000);

    /**    add image o the elemenet via data atribute and class="tile-item" or class="bg-image"
     *  example used in breadcrumbs
     *****************************************************/
    $(".tile-item, .bg-image").css('background', function () {
        var bg = ('url(' + $(this).data("image-src") + ') no-repeat center center');
        return bg;
    });

    // cover data image
    $(".tile-item, .bg-image").css("background-size", "cover");
});

// Function Fechar Alert
function fecharalert() {
    $('#alertinfo').delay(100).fadeOut('slow');
}

function fecharalert1() {
    $('#alertinfo1').delay(100).fadeOut('slow');
}

// Function Chamar SESSION - bt
function divca1() {
	$.get(estesite, function( data ) {
	});
}

// ResetIp, Esconder SpinLoad, Mostrar AD
$(document).ready(function() {
  setTimeout(function(){
  	$.get(estesite2, function( data ) {
  	});
  }, tempo1*1000)
});


// Abrir dl se a SESSION for ok
$(document).ready(function() {
  setTimeout(function atualizar()
          {
              $.get(estesite3, function( data ) {
  							  $('#instagramshow2').delay(350).fadeOut('slow');
  							  $('#open').html(data);
              });
          }, tempo2*1000)
});

// Descer Página
function descer(obj)
{
 $("html, body").animate({
    scrollTop: $('#desceraqui').offset().top
  }, 1000);
}

/**    Desabilitado
* Cronometro
$(document).ready(function() {
  var downloadTimer = setInterval(function(){
    document.getElementById("progressBar").value = timeleft2 - timeleft;
  	document.getElementById("countdown").innerHTML = timeleft + " s";
    timeleft -= 1;
    if(timeleft <= 0)
      clearInterval(downloadTimer);
  }, 1000);
});
*****************************************************/