function updateStats() {
    var numRand = Math.floor(Math.random() * 10001);
    $.get(flaskServ + "/folder/" + numRand, function (data) {
        $("#curfolder").html(data);
    });
    $.get(flaskServ + "/index/" + numRand, function (data) {
        $("#curindex").html(data);
    });
}

function changeImage(actionUrl, infoText, infoColor) {
    var numRand = Math.floor(Math.random() * 10001);
    $('#mainImg').fadeTo(350, 0, function() {
        $('#mainImg').attr('src', flaskServ + actionUrl + numRand);
    });
    $('#mainImg').load(function() {
        $('#mainImg').fadeTo(350, 1);      // fade in new
    });
    $('#actionbox').html('<p>' + infoText + '</p>');      // change infobox text
    $('#actionbox').css('background-color', infoColor);   // change infobox color
    $('#actionbox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0); // infobox fade
    updateStats();
}

var flaskServ = 'http:' + window.location.origin.split(':')[1] + ':5000';

$(".floatbox").fadeTo(0,0);
$('#mainImg').attr('src', flaskServ + '/image/0');
updateStats();

$(function(){
  $( ".ui-page" ).swipe( {
        swipeLeft:function(event, direction, distance, duration, fingerCount) {
            changeImage('/next/skip/', 'skipped', 'grey');
            if (screenfull.enabled) {
               screenfull.request();
            };
        },
        swipeUp:function(event, direction, distance, duration, fingerCount) {
            changeImage('/next/up/', upfolder, upcolor);
            if (screenfull.enabled) {
               screenfull.request();
            };
        },
        swipeDown:function(event, direction, distance, duration, fingerCount) {
            changeImage('/next/down/', downfolder, downcolor);
            if (screenfull.enabled) {
               screenfull.request();
            };
        },
        swipeRight:function(event, direction, distance, duration, fingerCount) {
            changeImage('/prev/', 'back', 'grey');
            if (screenfull.enabled) {
               screenfull.request();
            };
        },
  });
  $(".ui-page").dblclick(function() {
        $.get(flaskServ + "/imgtap");
        $('#tapbox').html('<p>' + tapfolder + '</p>');
        $('#tapbox').css('background-color', tapcolor);
        $('#tapbox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0);
  });
});
