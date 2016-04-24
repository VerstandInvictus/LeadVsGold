var colors = ['#104060','#125b94','#1f7fc1','#67add8']
var flaskServ = 'http:' + window.location.origin.split(':')[1] + ':5000';

$get(flaskServ + '/folders', function(data) {
    $.each(data, function (index, value) {
        var string = '<p class="submit purple"><a href="folders/' +
        value + '">' + value + '</a></p><br>';
        $("#selections").append(string);
    }
})