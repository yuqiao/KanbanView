function xml_http_post(url, data, callback) {
    var req = false;
    try {
        // Firefox, Opera 8.0+, Safari
        req = new XMLHttpRequest();
    }
    catch (e) {
        // Internet Explorer
        try {
            req = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e) {
            try {
                req = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e) {
                alert("Your browser does not support AJAX!");
                return false;
            }
        }
    }
    req.open("POST", url, true);
    req.onreadystatechange = function() {
        if (req.readyState == 4) {
            callback(req);
        }
    }
    req.send(data);
}

function refresh() {
    var elem = document.getElementById('content')
    elem.innerHTML = ""
    xml_http_post("kanban.html", 99, add_content)
}

function add_content(req) {
    var elem = document.getElementById('content')
    elem.innerHTML =  req.responseText
}

xml_http_post("kanban.html", 99, add_content)