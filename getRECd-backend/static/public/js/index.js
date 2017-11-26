var SPOTIFY_CLIENT_ID = "1c60ef76b2504eb58583af433ab30bfe";
var SPOTIFY_AUTH_TOKEN = "";

//
// UTILS
//
function b64EncodeUnicode(str) {
    // first we use encodeURIComponent to get percent-encoded UTF-8,
    // then we convert the percent encodings into raw bytes which
    // can be fed into btoa.
    return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
        function toSolidBytes(match, p1) {
            return String.fromCharCode('0x' + p1);
    }));
}

function b64DecodeUnicode(str) {
    // Going backwards: from bytestream, to percent-encoding, to original string.
    return decodeURIComponent(atob(str).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
}

// SAVING / LOADING STATE
function _gen_uuid(){
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function saveState(){
    var id = _gen_uuid(); // generate a new UUID
    localStorage.setItem('spotify_save_'+id, JSON.stringify({'songs': songs, 'search': search})); // and save the state in it
    return id; // and return
}

function loadState(id){
    // parse the state from localStorage
    var state = JSON.parse(localStorage.getItem('spotify_save_' +id));

    // set it everywhere
    songs = state['songs'];
    search = state['search'];
    $('#sentence').val(search);
    location.hash = '#' + encodeURIComponent(search);

    // and forget about it
    localStorage.removeItem('spotify_save_' +id);
}

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
        results.append(
            $("<li class='collection-item avatar spotify-collection' style='background-color: #000000;'>").append(
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
                    $('<i class="material-icons spotify-color">').text('play_arrow')
                )
            )
        );
    }

    return results;
}


var is_blocked = false; // is the interface blocked?
var songs = []; // list of songs we have, in case we want to use the API
var search = ""; // the current search we have


//
// HANDLING SEARCH
//

function handle_search(text){
    // block future searches, and setup the search text
    if(is_blocked){return;}
    is_blocked = true;
    $("#build, #save").attr('disabled', true);
    $('#sentence').val(text);
    search = text;
    location.hash = '#'+encodeURIComponent(text);

    // setup the laoding text
    $('#output').text('Retrieving results...');


    get_songs_by_sentence(text, undefined, function(results){
        // save the resulting items
        songs = results['items'];
        $("#output").empty().append(render_into_list(results['items']));

        // and unblock
        is_blocked = false;
        $("#build, #save").removeAttr('disabled');
    })
}

//
// HANDLE CREATE PLAYLIST (Step 1)
//

function handle_create_playlist(){
    // save the current state and get an id for later
    var state = saveState();

    // the URL to redirect to.
    var redirect_uri = location.protocol.concat("//").concat(window.location.host).concat('/');


    var url = "https://accounts.spotify.com/authorize?" +
        "client_id=" + SPOTIFY_CLIENT_ID +
        "&response_type=token" +
        "&redirect_uri=" + redirect_uri +
        "&state=" + encodeURIComponent(state) +
        "&scopes=playlist-modify-private" +
        "&show_dialog=true";

    location.href=url;
}


//
// HANDLE CREATE PLAYLIST (Step 2)
//

function handle_playlist_two(hash){

    // block everything
    is_blocked = true;
    $("#build, #save").attr('disabled', true);
    $('#output').text('Creating your Playlist, please wait ...');


    // set the state based on the hash
    var parts = hash.split('&');
    var part;
    for(var i = 0; i < parts.length; i++){
        part = parts[i].split('=');
        switch(part[0]){
            // store the auth token
            case 'access_token':
                SPOTIFY_AUTH_TOKEN = part[1];
                break;

            // store the state
            case 'state':
                loadState(part[1]); // load the state
                break;
            default:
                break;
        }
    }

    // load state
    $('#output').text(SPOTIFY_AUTH_TOKEN);

}


function handle_hash(hash){
    //
    if(hash.startsWith('access_token=')){
        handle_playlist_two(hash)
    } else {
        handle_search(decodeURIComponent(hash));
    }
}

$(function () {
    // read the parameter from the URL, and populate the example
    var hash = decodeURIComponent(location.hash.substring(1)) || undefined;

    if(hash){ handle_hash(hash)};

    $('#search').submit(function(e){
        e.preventDefault();
        handle_search($('#sentence').val());
    });

    $('#save').click(function(e){
        e.preventDefault();
        handle_create_playlist();
    })
});

