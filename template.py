#!/usr/bin/python
# vim: fileencoding=utf8 :

# Copyright 2011 Rémy Sanchez <remy.sanchez (a)_ hyperthese.net>
# Under the terms of the WTFPL

def parse(inp, out, tree, data):
	f = open(inp, "r")
	tpl = f.read()
	f.close()

	f = open(out, "wb")

	f.write('/** ')
	f.write(data)
	f.write(' **/\n')

	f.write('var t=')
	f.write("function(c){return " + tree + ";}")
	f.write('\n\n')

	f.write(tpl)
	f.close()
