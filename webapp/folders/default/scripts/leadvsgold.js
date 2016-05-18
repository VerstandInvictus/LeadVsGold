function updateStats(num) {
    $.get(flaskServ + '/' + dbname + "/info/" + num, function (data) {
        splitinfo = data.split(':')
        $("#curfolder").html(splitinfo[0]);
        $("#curcreator").html(splitinfo[1]);
        $("#curindex").html(splitinfo[2]);
        $("#cursession").html(splitinfo[3]);
        $("#curremain").html(splitinfo[4]);
        $("#curdate").html(splitinfo[5]);
    });
}

function changeImage(argsobj) {
    var actionUrl = argsobj[0]
    var infoText = argsobj[1]
    var infoColor = argsobj[2]
    var numRand = Math.floor(Math.random() * 100001);
    $('#mainImg').off("load");
    $('#mainImg').fadeTo(350, 0, function() {
        $('#mainImg').attr('src', flaskServ + '/' + dbname + actionUrl + numRand);
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

upact = '/next/up/', upfolder, upcolor;
downact = '/next/down/', downfolder, downcolor;
leftact = '/next/skip/', 'skipped', 'grey';
rightact = '/prev/', 'back', 'grey';

// the gear VR's touchpad is logically flipped from UDLR on a screen
// if we detect Samsung Internet, flip axes for input
if ((navigator.userAgent.indexOf('SamsungBrowser') != -1)) {
    upaction = downact;
    downaction = upact;
    leftaction = rightact;
    rightaction = leftact;
    // cataction = dogact;
    // eastaction = westact;
    // ukaction = anarchy;
    console.log('detected Gear VR');
}
else {
    upaction = upact;
    downaction = downact;
    leftaction = leftact;
    rightaction = rightact;
}

$( document ).ready(function() {
    $(".floatbox").fadeTo(0,0);
    var numRand = Math.floor(Math.random() * 100001);
    updateStats(numRand);
    $('#mainImg').attr('src', flaskServ + '/' + dbname + '/image/' + numRand);
    $( ".ui-page" ).swipe( {
        swipeLeft:function(event, direction, distance, duration, fingerCount) {
            changeImage(leftaction);
            if (screenfull.enabled) {
               screenfull.request();
            };
        },
        swipeUp:function(event, direction, distance, duration, fingerCount) {
            changeImage(upaction);
            if (screenfull.enabled) {
               screenfull.request();
            };
        },
        swipeDown:function(event, direction, distance, duration, fingerCount) {
            changeImage(downaction);
            if (screenfull.enabled) {
               screenfull.request();
            };
        },
        swipeRight:function(event, direction, distance, duration, fingerCount) {
            changeImage(rightaction);
            if (screenfull.enabled) {
               screenfull.request();
            };
        },
    });
    $( document ).keydown(function(e) {
        switch(e.which) {
            case 37:
                changeImage(rightaction);
                break;
            case 38:
                changeImage(upaction);
                break;
            case 39:
                changeImage(leftaction);
                break;
            case 40:
                changeImage(downaction);
                break;
            case 32:
            case 35:
                $.get(flaskServ + '/' + dbname + "/imgtap");
                $('#tapbox').html('<p>' + tapfolder + '</p>');
                $('#tapbox').css('background-color', tapcolor);
                $('#tapbox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0);
            default: return;
        }
        e.preventDefault();
    });
    $(".ui-page").dblclick(function() {
        $.get(flaskServ + '/' + dbname + "/imgtap");
        $('#tapbox').html('<p>' + tapfolder + '</p>');
        $('#tapbox').css('background-color', tapcolor);
        $('#tapbox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0);
    });
    $(".cornerbox").click(function() {
        $.get(flaskServ + '/' + dbname + "/info/reset");
        updateStats(78);
    });
    $("#rightcornerbox").click(function() {
        $.get(flaskServ + '/' + dbname + "/imgtap");
        $('#tapbox').html('<p>' + tapfolder + '</p>');
        $('#tapbox').css('background-color', tapcolor);
        $('#tapbox').fadeTo(250, 0.7).delay(1000).fadeTo(250, 0);
    });
});