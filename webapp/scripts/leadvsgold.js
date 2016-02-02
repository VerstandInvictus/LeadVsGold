$(function(){
  $( ".ui-page" ).swipe( {
        swipeLeft:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', window.location.origin.slice(0, -5) +':5000/next/skip/' +
            numRand);
        },
        swipeRight:function(event, direction, distance, duration, fingerCount) {
            var numRand = Math.floor(Math.random() * 10001);
            $('#mainImg').attr('src', window.location.origin.slice(0, -5) +':5000/prev/' +
            numRand);
        }
  });
})
