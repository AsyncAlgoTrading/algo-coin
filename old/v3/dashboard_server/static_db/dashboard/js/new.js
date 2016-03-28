$(document).ready(function(){

$("#connections div.hide ").hide();
$("#ticker div.hide ").hide();
$("#orderbook div.hide ").hide();
$("#strategies div.hide ").hide();
$("#accounts div.hide ").hide();

$(".section#ticker").click(function(){
    $("#ticker div.hide ").toggle();
});
$(".section#orderbook").click(function(){
    $("#orderbook div.hide ").toggle();
});

$(".section#strategies").click(function(){
    $("#strategies div.hide ").toggle();
});

$(".section#accounts").click(function(){
    $("#accounts div.hide ").toggle();
});

$(".section#connections").click(function(){
    $("#connections div.hide ").toggle();
});

});
