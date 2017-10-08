
"use strict";
var editor;

function initialiseEditor(edId) {
    editor = ace.edit(edId);

    // theme
    editor.setTheme("ace/theme/tomorrow");

    // on change
    editor.getSession().on("change", function(e) {
        document.getElementById("save_message").innerText = "(unsaved)";
    });

    // set mode based on filetype
    let filename = document.getElementById("file_header").innerText;
    let modelist = ace.require("ace/ext/modelist");
    let mode = modelist.getModeForPath(filename).mode
    editor.session.setMode(mode)

    // vim
    editor.setKeyboardHandler("ace/keyboard/vim");

    // wrap
    editor.setOption("wrap", true);

    // fontsize
    editor.setOption("fontSize", 14);

    // get focus
    editor.focus();
}

window.onload = function() {
    initialiseEditor('editor');
    setInterval(save, 1000*60*3); // auto save every 3 minutes
                                  // save function definition is in files.js
};

window.onbeforeunload = function() {
    let saved = document.getElementById("save_message").innerText == "";
    if (!saved) {
        let message = "You have unsaved changes.";
        return message;
    }
};
