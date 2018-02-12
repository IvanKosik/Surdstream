$(function() {

    $(function () {

      $('[data-toggle="tooltip"]').tooltip()

      /* CUSTOMIZED TOOLTIP
      $('[data-toggle="tooltip"]').tooltip({
        'template':'<div class="tooltip" role="tooltip"> \
         <div class="arrow"></div> \
         <div class="tooltip-inner" style="background-color:green;"></div> \
         </div>'})
      */
    })

    $('.carousel').carousel({'interval':false});

    $('.navbar-nav a').click(function(e){
      e.preventDefault();
      if ( $(this).hasClass('active') ) {
      } else {
        $('.navbar-nav a').removeClass('active');
        $(this).addClass('active');
        $('main').children().hide();
        $($(this).attr('href')).show();
        $('.collapse').collapse('hide')
      }
    });


    $('#addVideoBtn').click(function(e) {

      console.log( $(this).html() )

      $(this).children().toggleClass('fa-plus').toggleClass('fa-times');
      $(this).toggleClass('btn-success').toggleClass('btn-danger');
      $(this).blur();

      if ( $(this).attr('data-original-title') !== 'Close') {
        $('[data-toggle="tooltip"]').tooltip('dispose');
        $(this).attr('title','Close');
        $('[data-toggle="tooltip"]').tooltip({
          'template':'<div class="tooltip" role="tooltip"> \
           <div class="arrow red"></div> \
           <div class="tooltip-inner red"></div> \
           </div>'});
      } else {
        $('[data-toggle="tooltip"]').tooltip('dispose');
        $(this).attr('title','Add');
        $('[data-toggle="tooltip"]').tooltip({
          'template':'<div class="tooltip" role="tooltip"> \
           <div class="arrow"></div> \
           <div class="tooltip-inner"></div> \
           </div>'});
      }

      $("button.navbar-toggler").prop('disabled', !$('button.navbar-toggler').prop('disabled') );
      $("main").toggle();
      $("section#addVideo").toggleClass('d-none');

    });

});
