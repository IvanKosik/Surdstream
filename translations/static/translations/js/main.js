$(document).ready(function(){

    $(".publication").click(function(){
        $(this).find('.video_placeholder').slideToggle('slow');
    });

    $("#logInButton").click( function(){
        $("#search").removeClass("searchVisibleFromRight").removeClass("searchHiddenToRight");
        $("#logIn").removeClass("logInHidden").addClass("logInVisible");
        $("#search").removeClass("searchVisibleFromLeft").addClass("searchHiddenToLeft");
    });

    $("#closeLogInButton").click( function() {
        $("#logIn").removeClass("logInVisible").addClass("logInHidden");
        $("#search").addClass("searchVisibleFromLeft").removeClass("searchHiddenToLeft");
    });

    $("#closeSignInButton").click( function() {
      $("#signIn").removeClass("signInVisible").addClass("signInHidden");
      $("#search").addClass("searchVisibleFromRight").removeClass("searchHiddenToRight");
    });

    $("#signInButton").click( function(){
        $("#search").removeClass("searchVisibleFromLeft").removeClass("searchHiddenToLeft");
        $("#signIn").removeClass("signInHidden").addClass("signInVisible");
        $("#search").removeClass("searchVisibleFromRight").addClass("searchHiddenToRight");
    });

});
