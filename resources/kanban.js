"use strict";
/*jslint browser: true*/
/*global $*/

function add_content(req) {
    var elem = document.getElementById('content');
    elem.innerHTML += req;
}

function replace_content(id, data) {
    var elem = document.getElementById(id);
    elem.outerHTML = data;
}

function get_rows(rows) {
    var fragment = "", row = "";
    rows.forEach(row => {
        var css_class = 'hasNoProject'
        var task = row.title
        var context = row.context

        if (row.uuid != null) { task = '<a href="things:///show?id=' + row.uuid + '">' + row.title + '</a>'}
        if (row.context_uuid != null) { context = '<a href="things:///show?id=' + row.context_uuid + '">' + row.context + '</a>'}
        if (row.context != null) { css_class = 'hasProject' } else { row.context = 'No Context' }
        if (row.due != null) { css_class = 'hasDeadline' } else { row.due = '' }

        fragment += '<div class="box">' + task +
                      '<div class="deadline">' + row.due + '</div>' +
                      '<div class="area ' + css_class + '">' + context + '</div>' +
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

var makeRequest = function (url, method) {

	// Create the XHR request
	var request = new XMLHttpRequest();

	// Return it as a Promise
	return new Promise(function (resolve, reject) {

		// Setup our listener to process compeleted requests
		request.onreadystatechange = function () {

			// Only run if the request is complete
			if (request.readyState !== 4) return;

			// Process the response
			if (request.status >= 200 && request.status < 300) {
				// If successful
				resolve(request);
			} else {
				// If failed
				reject({
					status: request.status,
					statusText: request.statusText
				});
			}

		};

		// Setup our HTTP request
		request.open(method || 'GET', url, true);

		// Send the request
		request.send();

	});
};

function refresh() {
    //todo: fix promises to make sure the order is correct
    makeRequest('api/backlog').then(function (data) {add("color1", "Backlog", data)})
    .then(makeRequest('api/upcoming').then(function (data) {add("color5", "Upcoming", data)}))
    .then(makeRequest("api/waiting").then(function (data) {add("color3", "Waiting", data)}))
    .then(makeRequest("api/inbox").then(function (data) {add("color4", "Inbox", data)}))
    .then(makeRequest("api/mit").then(function (data) {add("color2", "MIT", data)}))
    .then(makeRequest("api/today").then(function (data) {add("color6", "Today", data)}))
    .then(makeRequest("api/next").then(function (data) {add("color7", "Next", data)}))
}

window.onfocus = refresh;
window.onload = refresh;