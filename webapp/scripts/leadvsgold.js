var flaskServ = 'http:' + window.location.origin.split(':')[1] + ':5000';

$(".infobox").fadeTo(0,0);

$('#mainImg').attr('src', flaskServ + '/image/0')

$(function(){
  $( ".ui-page" ).swipe( {
        swipeLeft:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', flaskServ + '/next/skip/' +
                    numRand);
            $('.infobox').html('<p>skipped</p>');
            $('.infobox').css('background-color', 'grey');
            $('.infobox').fadeTo(250, 0.7).delay(750).fadeTo(250, 0);
            $('#mainImg').fadeTo(250, 0.3);
            $('#mainImg').load(function() {
                $('#mainImg').fadeTo(250, 1);
            });
        },
        swipeUp:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', flaskServ + '/next/up/' +
            numRand);
            $('.infobox').html('<p>' + upfolder + '</p>');
            $('.infobox').css('background-color', upcolor);
            $('.infobox').fadeTo(250, 0.7).delay(750).fadeTo(250, 0);
            $('#mainImg').fadeTo(250, 0.3);
            $('#mainImg').load(function() {
                $('#mainImg').fadeTo(250, 1);
            });
        },
        swipeDown:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', flaskServ + '/next/down/' +
            numRand);
            $('.infobox').html('<p>' + downfolder + '</p>');
            $('.infobox').css('background-color', downcolor);
            $('.infobox').fadeTo(250, 0.7).delay(750).fadeTo(250, 0);
            $('#mainImg').fadeTo(250, 0.3);
            $('#mainImg').load(function() {
                $('#mainImg').fadeTo(250, 1);
            });
        },
        swipeRight:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', flaskServ + '/prev/' +
            numRand);
            $('.infobox').html('<p>back</p>');
            $('.infobox').css('background-color', 'gray');
            $('.infobox').fadeTo(250, 0.7).delay(750).fadeTo(250, 0);
            $('#mainImg').fadeTo(250, 0.3);
            $('#mainImg').load(function() {
                $('#mainImg').fadeTo(250, 1);
            });
        }
  });
})
