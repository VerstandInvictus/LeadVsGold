var flaskServ = 'http:' + window.location.origin.split(':')[1] + ':5000'

$('#mainImg').attr('src', flaskServ + '/image/0')

$(function(){
  $( ".ui-page" ).swipe( {
        swipeLeft:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', flaskServ + '/next/skip/' +
                    numRand);
            $('#mainImg').fadeTo(250, 0.3);
            $('#mainImg').load(function() {
                $('#mainImg').fadeTo(250, 1);
            });
        },
        swipeUp:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', flaskServ + '/next/up/' +
            numRand);
            $('#mainImg').fadeTo(250, 0.3);
            $('#mainImg').load(function() {
                $('#mainImg').fadeTo(250, 1);
            });
        },
        swipeDown:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', flaskServ + '/next/down/' +
            numRand);
            $('#mainImg').fadeTo(250, 0.3);
            $('#mainImg').load(function() {
                $('#mainImg').fadeTo(250, 1);
            });
        },
        swipeRight:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', flaskServ + '/prev/' +
            numRand);
            $('#mainImg').fadeTo(250, 0.3);
            $('#mainImg').load(function() {
                $('#mainImg').fadeTo(250, 1);
            });
        }
  });
})
