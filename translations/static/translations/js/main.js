$(document).ready(function(){
    $(".publication").click(function(){
        console.log($(this).find('.video_placeholder'));
        $(this).find('.video_placeholder').slideToggle('slow');
    });
});
