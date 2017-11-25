function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}

//    httpGetAsync("http://localhost:8080/api/sentence/".concat(selection).concat("/"),alert)

// A generic onclick callback function.
function genericOnClick(context) {
  text = ""
    chrome.tabs.executeScript( {
      code: "window.getSelection().toString();"
    }, function(selection) {
    var newURL = "http://localhost:8080/#".concat(selection);
    chrome.tabs.create({ url: newURL });
    });
}

// Create one test item for each context type.
var contexts = ["page","selection","link","editable","image","video",
                "audio"];
var context = "selection";
var title = "Spotify this :)";
var id = chrome.contextMenus.create({"title": title, "contexts":[context],
                                     "onclick": genericOnClick.bind(this, context)});
