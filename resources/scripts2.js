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
    elem.innerHTML += req;
}

function replace_content(id, data) {
    var elem = document.getElementById(id);
    elem.outerHTML = data;
}

function get_rows(rows) {
    var fragment = ""
    rows.forEach(row => {
        fragment += '<div class="box"><a href="things:///show?id=' + row.uuid + '">' + row.title + '</a>' +
                      '<div class="deadline">' + row.due + '</div>' +
                      '<div class="area">' + row.context + '</div>' +
                    '</div>'
        });
    return fragment
}

function setup_html_column(cssclass, header, number) {
    return "<div class='column' id='"+header+"'>" +
               "  <div class=''>" +
               "     <h2 class='" + cssclass + "'>" + header +
               "         <span class='size'>" + number + "</span>" +
               "     </h2>"
    
}

function add(color, title, data) {
    var rows = JSON.parse(data.response)
    var fragment = setup_html_column(color, title, rows.length);
    fragment += get_rows(rows)
    fragment += "</div></div>";
    if (document.getElementById(title) != null) {
        replace_content(title, fragment)   
    } else {
        add_content(fragment)
    }
}

function refresh() {
    xml_http_get("api/backlog", null, data => { add("color1", "Backlog", data); })
    xml_http_get("api/upcoming", null, data => { add("color5", "Upcoming", data); })
    xml_http_get("api/waiting", null, data => { add("color3", "Waiting", data); })
    xml_http_get("api/inbox", null, data => { add("color4", "Inbox", data); })
    xml_http_get("api/mit", null, data => { add("color2", "MIT", data); })
    xml_http_get("api/today", null, data => { add("color6", "Today", data); })
    xml_http_get("api/next", null, data => { add("color7", "Next", data); })
}

window.onfocus = refresh;
window.onload = refresh;