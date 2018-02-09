function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            // TODO: we can cache csrftoken and update it (get from cookie) only
            // TODO: when user login or logout
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


$(document).ready(function() {

});


$(".js-process-vote").click(function(event) {
    event.preventDefault();

    var button = $(this);
    $.post(button.attr("vote-url"), {'vote': button.val()}, function(data) {
            $("#total-votes").text(data.new_total_votes);
            $("#user-vote").text(data.user_vote);
            var voteUpButton = $("#vote-up");
            var voteDownButton = $("#vote-down");
            voteUpButton.prop('disabled', voteUpButton.val() == data.user_vote);
            voteDownButton.prop('disabled', voteDownButton.val() == data.user_vote);
        },
        'json'
    );
});


function updateLoginUi(isLoggedIn) {
    $("#menu-login").attr("hidden", isLoggedIn);
    $("#menu-logout").attr("hidden", !isLoggedIn);
}


$("#signup-form").submit(function(event) {
    event.preventDefault(); // avoid to execute the actual submit of the form.

    var signupForm = $(this);
    $.post(signupForm.attr("action"), signupForm.serialize(), function(data) {
            errors = "";
            let fields_errors = JSON.parse(data.field_errors);
            for (let field_name in fields_errors) {
                for (let field_error of fields_errors[field_name]) {
                    errors += '\n' + field_error.message;
                }
            }
            if (errors) {
                $("#signup-error").text(errors);
                $("#signup-error").attr("hidden", false);
            } else {
                updateLoginUi(data.user_id)
            }
        },
        'json'
    );
});


$("#login-form").submit(function(event) {
    event.preventDefault();

    var loginForm = $(this);
    $.post(loginForm.attr("action"), loginForm.serialize(), function(data) {
            updateLoginUi(data.user_id)
            $("#login-error").attr("hidden", data.user_id);
//            data.field_errors.__all__[0].message
        },
        'json'
    );
});


$("#logout-link").click(function(event) {
    event.preventDefault();

    var logoutLink = $(this);
    $.post(logoutLink.attr("href"), function(data) {
            updateLoginUi(data.user_id)
        },
        'json'
    );
});
