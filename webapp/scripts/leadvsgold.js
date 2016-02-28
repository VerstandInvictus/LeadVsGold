function updateStats(num) {
    $.get(flaskServ + "/info/" + num, function (data) {
        splitinfo = data.split(':')
        $("#curfolder").html(splitinfo[0]);
        $("#curcreator").html(splitinfo[1]);
        $("#curindex").html(splitinfo[2]);
        $("#cursession").html(splitinfo[3]);
        $("#curremain").html(splitinfo[4]);
    });
}

function changeImage(actionUrl, infoText, infoColor) {
    var numRand = Math.floor(Math.random() * 10001);
    $('#mainImg').off("load");
    $('#mainImg').fadeTo(350, 0, function() {
        $('#mainImg').attr('src', flaskServ + actionUrl + numRand);
    });
    $('#mainImg').load(function() {
        $('#mainImg').fadeTo(350, 1, function() {
            updateStats(numRand);
        });      // fade in new
    });
    $('#actionbox').html('<p>' + infoText + '</p>');      // change infobox text
    $('#actionbox').css('background-color', infoColor);   // change infobox color
    $('#actionbox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0);
}

var flaskServ = 'http:' + window.location.origin.split(':')[1] + ':5000';

$( document ).ready(function() {
    $(".floatbox").fadeTo(0,0);
    updateStats(0);
    $('#mainImg').attr('src', flaskServ + '/image/0');
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
    $( document ).keydown(function(e) {
        switch(e.which) {
            case 37:
                changeImage('/next/skip/', 'skipped', 'grey');
                break;
            case 38:
                changeImage('/next/up/', upfolder, upcolor);
                break;
            case 39:
                changeImage('/prev/', 'back', 'grey');
                break;
            case 40:
                changeImage('/next/down/', downfolder, downcolor);
                break;
            default: return;
        }
        e.preventDefault();
        if (screenfull.enabled) {
           screenfull.request();
        };
    });
    $(".ui-page").dblclick(function() {
        $.get(flaskServ + "/imgtap");
        $('#tapbox').html('<p>' + tapfolder + '</p>');
        $('#tapbox').css('background-color', tapcolor);
        $('#tapbox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0);
    });
    $(".cornerbox").click(function() {
        $.get(flaskServ + "/info/reset");
        updateStats(78);
    })
});