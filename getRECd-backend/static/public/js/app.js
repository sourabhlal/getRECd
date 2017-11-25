//
// BACKEND CALLS
//

/**
 * Makes a call to an endpoint on this server and calls a callback function
 * @param endpoint
 * @param callback
 */
function make_get_request(endpoint, callback) {
    $.get(endpoint, function (data, err) {
        callback(data);
    }).fail(function (data) {
        callback(JSON.parse(data.responseText))
    })
}

/** Gets a set of songs starting with a given character and optionally a genre */
function get_songs_by_character(char, genre, callback) {
    // find the endpoint we have to call
    var endpoint = '/api/character/' + encodeURIComponent(char) + '/';
    if (typeof genre !== 'undefined') {
        endpoint += '/' + encodeURIComponent(genre) + '/';
    }

    // and make the GET request
    return make_get_request(endpoint, callback);
}

/** Gets a set of songs starting with the given sentence and optionally a genre */
function get_songs_by_sentence(char, genre, callback) {
    // find the endpoint we have to call
    var endpoint = '/api/sentence/' + encodeURIComponent(char) + '/';
    if (typeof genre !== 'undefined') {
        endpoint += '/' + encodeURIComponent(genre) + '/';
    }

    // and make the GET request
    return make_get_request(endpoint, callback);
}

//
// RENDERING
//

function render_into_list(items) {
    var results = $("<ul class='collection with-header'>");
    var item;

    for (var i = 0; i < items.length; i++) {
        item = items[i];
        console.log(item['name']);
        results.append(
            $("<li class='collection-item avatar' style='background-color: #000000;'>").append(
                $('<img class="circle">').attr({
                    'src': item['album']['images'][0]['url'],
                    'width': 120,
                    'height': 120
                }),
                $('<span class="title">').text(item['name']),
                $('<p>').append(
                    $('<span>').text(item['artists'][0]['name']).html(),
                    "<br />",
                    $('<span>').text(item['album']['name']).html()
                ),
                $('<a class="secondary-content">').attr({
                    'target': '_blank',
                    'href': item['external_urls']['spotify']
                }).append(
                    $('<i class="material-icons" style="color: #1db954;">').text('play_arrow')
                )
            )
        );
    }

    return results;
}

var is_blocked = false;

function do_search(text){

    // block future searches, and setup the search text
    if(is_blocked){return;}
    is_blocked = true;
    $("#build").attr('disabled', true);
    $('#sentence').val(text);
    location.hash = encodeURIComponent(text);

    // setup the laoding text
    $('#output').text('Retrieving results...');


    get_songs_by_sentence(text, undefined, function(results){
        // save the resulting items
        $("#output").empty().append(render_into_list(results['items']));

        // and unblock
        is_blocked = false;
        $("#build").removeAttr('disabled');
    })
}


$(function () {

    // read the parameter from the URL, and populate the example
    var hash = decodeURIComponent(location.hash.substring(1)) || undefined;

    if(hash){
        do_search(hash);
    }

    $('#search').submit(function(e){
        e.stopImmediatePropagation();
        do_search($('#sentence').val());
    })
});

