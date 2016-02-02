$(function(){
  $( ".ui-page" ).swipe( {
        swipeLeft:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', 'http' + window.location.origin.split(':')[1] +':5000/next/skip/' +
            numRand);
        },
        swipeRight:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', 'http' + window.location.origin.split(':')[1] +':5000/prev/' +
            numRand);
        }
  });
})
