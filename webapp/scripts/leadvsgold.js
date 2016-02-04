if (screenfull.enabled) {
    screenfull.request();
}
var flaskServ = 'http:' + window.location.origin.split(':')[1] + ':5000';

$(".infobox").fadeTo(0,0);

$('#mainImg').attr('src', flaskServ + '/image/0')

function changeImage(actionUrl, infoText, infoColor) {
    var numRand = Math.floor(Math.random() * 10001);
    $('#mainImg').fadeTo(350, 0, function() {
        $('#mainImg').attr('src', flaskServ + actionUrl + numRand);
    });
    $('#mainImg').load(function() {
        $('#mainImg').fadeTo(350, 1);      // fade in new
    });
    $('.infobox').html('<p>' + infoText + '</p>');      // change infobox text
    $('.infobox').css('background-color', infoColor);   // change infobox color
    $('.infobox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0); // infobox fade
};

$(function(){
  $( ".ui-page" ).swipe( {
        swipeLeft:function(event, direction, distance, duration, fingerCount) {
            changeImage('/next/skip/', 'skipped', 'grey');
        },
        swipeUp:function(event, direction, distance, duration, fingerCount) {
            changeImage('/next/up/', upfolder, upcolor);
        },
        swipeDown:function(event, direction, distance, duration, fingerCount) {
            changeImage('/next/down/', downfolder, downcolor);
        },
        swipeRight:function(event, direction, distance, duration, fingerCount) {
            changeImage('/prev/', 'back', 'grey');
        },
        pinchIn:function(event, direction, distance, duration, fingerCount,
            pinchZoom) {
                $.get(flaskServ + "/imgtap");
                $('.tapbox').html('<p>' + tapfolder + '</p>');
                $('.tapbox').css('background-color', tapcolor);
                $('.tapbox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0);
        }
  });
});