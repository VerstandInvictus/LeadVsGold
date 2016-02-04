var flaskServ = 'http:' + window.location.origin.split(':')[1] + ':5000';

$(".infobox").fadeTo(0,0);

$('#mainImg').attr('src', flaskServ + '/image/0')

function changeImage(actionUrl, infoText, infoColor) {
    var numRand = Math.floor(Math.random() * 10001);
    $('#mainImg').fadeTo(350, 0);
    $('#mainImg').attr('src', '');
    $('#mainImg').attr('src', flaskServ + actionUrl +
            numRand);
    $('#mainImg').fadeTo(350, 1);
    $('.infobox').html('<p>' + infoText + '</p>');
    $('.infobox').css('background-color', infoColor);
    $('.infobox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0);
}

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
        }
  });
})
