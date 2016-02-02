$(function(){
  $( ".ui-page" ).swipe( {

    swipeLeft:function(event, direction, distance, duration, fingerCount) {
      $.get("http://127.0.0.1:5000/next/skip")
      var numRand = Math.floor(Math.random() * 10001);
      $('#mainImg').attr('src', 'http://127.0.0.1:5000/image/' + numRand.toString() +")")
    },
    swipeRight:function(event, direction, distance, duration, fingerCount) {
      $.get("http://127.0.0.1:5000/prev")
      var numRand = Math.floor(Math.random() * 10001);
      $('#mainImg').attr('src', 'http://127.0.0.1:5000/image/' + numRand.toString() +")")
    }
    })
  });
