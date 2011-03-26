/**
 * Copyright 2011 Rémy Sanchez <remy.sanchez (a)_ hyperthese.net>
 * Under the terms of WTFPL
 */

function dec(str) {
	var out = [];
	for(var i in str) {
		out.push(str.charCodeAt(i) & 255);
	}
	return out;
}

function CharPointer(str) {
	var ptr = 8, l = str[0], max = str.length * 8 - l;

	var n = (str[2] << 8) | str[1];
	console.log(n);

	ptr += 8 * (4 * n + 2);

	for(var i=3; i < n * 4; i++) {
		var idx = str[i++] | (str[i++] << 8) | (str[i++] << 16) | (str[i] << 24);
		str[4 * n + 3 + idx] = 47;
	}

	return function() {
		if (ptr >= max) throw 0;
		return str[Math.floor(ptr / 8)] & (128 >> (ptr++ % 8));
	}
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

var c = CharPointer(dec(getData()));
str = "";

try {
	while(true) str += t(c);
} catch(ex) {
	eval(str);
}
