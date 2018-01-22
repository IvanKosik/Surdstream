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
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(".js-process-vote").click(function() {
    var button = $(this);
    $.post(button.attr("vote-url"), {'vote': button.val()},
        function(data) {
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
