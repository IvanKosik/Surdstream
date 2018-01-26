$(document).ready(function(){

    $(".publication").click(function(){
        $(this).find('.video_placeholder').slideToggle('slow');
    });

    $("#logInButton").click( function(){
        $("#search").removeClass("searchVisibleFromRight").removeClass("searchHiddenToRight");
        $("#logIn").removeClass("logInHidden").addClass("logInVisible");
        $("#search").removeClass("searchVisibleFromLeft").addClass("searchHiddenToLeft");

        $("#menu_login > div:first-child").removeClass("authButonsVisible");
        $("#menu_login > div:last-child").removeClass("authPlaceholderHidden");
        $("#menu_login > div:last-child").text("Авторизация");
        $('#menu_login button').prop('disabled', true);
        $("#menu_login > div:first-child").addClass("authButonsHidden");
        $("#menu_login > div:last-child").addClass("authPlaceholderVisible");
    });

    $("#closeLogInButton").click( function() {
        $("#logIn").removeClass("logInVisible").addClass("logInHidden");
        $("#search").addClass("searchVisibleFromLeft").removeClass("searchHiddenToLeft");

        $("#menu_login > div:first-child").removeClass("authButonsHidden");
        $("#menu_login > div:last-child").removeClass("authPlaceholderVisible");
        $("#menu_login > div:last-child").text("");
        $('#menu_login button').prop('disabled', false);
        $("#menu_login > div:first-child").addClass("authButonsVisible");
        $("#menu_login > div:last-child").addClass("authPlaceholderHidden");
    });

    $("#signInButton").click( function(){
        $("#search").removeClass("searchVisibleFromLeft").removeClass("searchHiddenToLeft");
        $("#signIn").removeClass("signInHidden").addClass("signInVisible");
        $("#search").removeClass("searchVisibleFromRight").addClass("searchHiddenToRight");

        $("#menu_login > div:first-child").removeClass("authButonsVisible");
        $("#menu_login > div:last-child").removeClass("authPlaceholderHidden");
        $("#menu_login > div:last-child").text("Регистрация");
        $('#menu_login button').prop('disabled', true);
        $("#menu_login > div:first-child").addClass("authButonsHidden");
        $("#menu_login > div:last-child").addClass("authPlaceholderVisible");
    });

    $("#closeSignInButton").click( function() {
      $("#signIn").removeClass("signInVisible").addClass("signInHidden");
      $("#search").addClass("searchVisibleFromRight").removeClass("searchHiddenToRight");

      $("#menu_login > div:first-child").removeClass("authButonsHidden");
      $("#menu_login > div:last-child").removeClass("authPlaceholderVisible");
      $("#menu_login > div:last-child").text("");
      $('#menu_login button').prop('disabled', false);
      $("#menu_login > div:first-child").addClass("authButonsVisible");
      $("#menu_login > div:last-child").addClass("authPlaceholderHidden");
    });

});
