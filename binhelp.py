#!/usr/bin/python
# vim: fileencoding=utf8 :

# Copyright 2011 Rémy Sanchez <remy.sanchez (a)_ hyperthese.net>
# Under the terms of the WTFPL

def tobinrep(val, size):
	return bin(val)[2:].zfill(size)

def totruebin(string):
	from math import ceil
	out = bytearray()

	leftout = len(string) % 8
	out += chr(leftout)

	#print leftout

	for i in range(0, int(ceil(len(string) / 8)) + 1):
		chunk = string[i * 8:(i + 1) * 8]
		#print chunk

		if len(chunk) < 8:
			chunk += "0" * (8 - len(chunk))

		val = int(chunk, 2)
		out += chr(val)

	return out

def fromtruebin(b):
	leftout = b[0]

	out = ""

	for c in b[1:]:
		out += _tobinrep(c, 8)

	if leftout > 0:
		out = out[:-leftout]

	return out
