$(document).ready(function(){
/*
   $(".maystreet").mouseenter(function() {
        $(this).fadeTo('fast',1);
    });
    $(".maystreet").mouseleave(function() {
        $(this).fadeTo('fast',0.3);
    });
*/


$("#courses div.hide ").hide();
$("#projects div.hide ").hide();
$("#awards div.hide ").hide();
$("#precollege div.hide ").hide();
$("#clubs div.hide ").hide();



$(".section#education").click(function(){
    $("#education div.hide ").toggle();
});
$(".section#experience").click(function(){
    $("#experience div.hide ").toggle();
});

$(".section#publications").click(function(){
    $("#publications div.hide ").toggle();
});

$(".section#skills").click(function(){
    $("#skills div.hide ").toggle();
});

$(".section#courses").click(function(){
    $("#courses div.hide ").toggle();
});

$(".section#projects").click(function(){
    $("#projects div.hide ").toggle();
});

$(".section#awards").click(function(){
    $("#awards div.hide ").toggle();
});

$(".section#precollege").click(function(){
    $("#precollege div.hide ").toggle();
});

$(".section#clubs").click(function(){
    $("#clubs div.hide ").toggle();
});


});
