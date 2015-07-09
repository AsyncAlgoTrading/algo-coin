$(document).ready(function(){
    $("img.png").mouseenter(function() {
        $(this).fadeTo('fast',1);
    });
    $("img.png").mouseleave(function() {
        $(this).fadeTo('fast',0.3);
    });
});
