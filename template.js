/**
 * Copyright 2011 Rémy Sanchez <remy.sanchez (a)_ hyperthese.net>
 * Under the terms of WTFPL
 */

function CharPointer(str) {
	var ptr = 8, l = str.charCodeAt(0), max = str.length * 8 - l;
	return function() {
		if (ptr >= max) throw 0;
		return str.charCodeAt(Math.floor(ptr / 8)) & (128 >> (ptr++ % 8));
	}
}

function tobin(str) {
	c = CharPointer(str);

	str = ""
	try {
		var i = 0;
		while(true) {
			str += c() ? "1" : "0";
			if(++i % 8 == 0) {
				str += "<br />";
			}
		}
	} catch(ex) {
		// pass
	}

	return str;
}

String.prototype.r = function() {
	return this.split("").reverse().join("")
}

function huffval(tree) {
	eval("r = function(c) { return " + tree.r().replace(/c(?!')/g, "?)(c").r() + "; }");
	return r;
}

/**
 * Alright, Javascript is not very cooperative with binary data. Too bad.
 */

function getData() {
	var url = document.getElementById('jsz').getAttribute('src');
	var req = new XMLHttpRequest();
	req.open('GET', url, false);
	req.overrideMimeType('text/plain; charset=x-user-defined');
	req.send(null);
	if (req.status != 200) return '';

	var f = req.responseText;

	return f.substring(4, f.search(/ \*\*\//));
}

// Inputs
var huf = huffval(t);
var d = getData();

c = CharPointer(d);

start = (new Date()).getTime();
str = "";
try {
	while(true) str += huf(c);
} catch(ex) {
	stop = (new Date()).getTime();
	//console.log(ex);
	document.write(str);
}
//console.log(stop - start);
