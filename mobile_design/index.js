$(function() {
    console.log( "ready!" );

    $('.navbar-nav a').click(function(e){
      e.preventDefault();
      if ( $(this).hasClass('active') ) {
        console.log('ok');
      } else {
        $('.navbar-nav a').removeClass('active');
        $(this).addClass('active');
        $('main').children().hide();

        $($(this).attr('href')).show();

        console.log($(this).attr('href'));

        $('.collapse').collapse('hide')
      }
    });

    $('a[href$="home"]').click(function(e) {
      e.preventDefault();

      $('#page-menu').toggle().toggleClass('active');
    })
});
