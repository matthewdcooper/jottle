
function postRequest(url, params) {
    /* Send a POST request to url with params, return the xhr. */
    let xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(params)
    return xhr;
}

function hardConfirm(message) {
    /* Confirm that the user really wants to do 'message' by asking them
     * to enter a randomly generated number of 4 digits */
    let s = Math.random().toString();
    let nums = s.substring(s.length-4, s.length);
    message += "\n To confirm enter these digits: " + nums;
    let confNums = prompt(message);
    return confNums == nums;
}

function del(type) {
    let conf = hardConfirm("Are you sure you want to delete this " + type + "?");
    if (!conf) return;
    let params = "command=delete_" + type;
    let url = window.location.href;
    let xhr = postRequest(url, params);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {

            let i = window.location.pathname.lastIndexOf("/");
            if (i == 0) {
                window.location = "/";
            } else {
                let path = window.location.pathname.substring(0, i);
                window.location = path;
            }

        }
    };
}

function make(type) {
    let name = prompt("Enter a name for new " + type + ".");
    if (!name) return;
    let params = "command=make_" + type;
    params += "&name=" + name;
    let url = window.location.href;
    return  postRequest(url, params);
}

function makeDir() {
    let xhr = make("dir");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            window.location.reload();
        }
    };

}

function makeFile() {
    let xhr = make("file");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let path = window.location.pathname
            if (path.length > 1) path += "/";
            path += name + "?edit";
            window.location = path;
        }
    };
}

function rename() {
    let new_name = prompt("Enter a new name.");
    if (!new_name) return;
    let params = "command=rename";
    params += "&new_name=" + new_name;
    let url = window.location.href;
    let xhr = postRequest(url, params);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            let i = window.location.pathname.lastIndexOf("/");
            if (i == 0) {
                window.location = "/" + new_name;
            } else {
                let path = window.location.pathname.substring(0, i+1);
                window.location = path + new_name;
            }

        }
    };
}

function save() {
    let text = encodeURIComponent(editor.getValue());
    let params = "command=save";
    params += "&text=" + text;
    let url = window.location.href.split('?')[0]; // remove parameters
    let xhr = postRequest(url, params, false);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById("save_message").innerText = "";
        }
    };

}

