"use strict";
/*jslint browser: true*/
/*global $*/

function xml_http_get(url, data, callback) {
    var req = new XMLHttpRequest();
    req.open("GET", url, true);
    req.onreadystatechange = function () { if (req.readyState === 4) { callback(req); } };
    req.send(data);
}

function add_content(req) {
    var elem = document.getElementById('content');
    elem.innerHTML = req.responseText;
}

function refresh() {
    xml_http_get('/kanban', null, add_content);
}

window.onfocus = refresh;
window.onload = refresh;