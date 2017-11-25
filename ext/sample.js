



// A generic onclick callback function.
function genericOnClick(context) {
  chrome.tabs.executeScript( {
    code: "window.getSelection().toString();"
  }, function(selection) {
    text = selection;
    alert(selection);
  });
}



// Create one test item for each context type.
var contexts = ["page","selection","link","editable","image","video",
                "audio"];
var context = "selection";
var title = "Spotify this :)";
var id = chrome.contextMenus.create({"title": title, "contexts":[context],
                                     "onclick": genericOnClick.bind(this, context)});
