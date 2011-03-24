#!/usr/bin/python
# vim: fileencoding=utf8 :

# Copyright 2011 Rémy Sanchez <remy.sanchez (a)_ hyperthese.net>
# Under the terms of the WTFPL

def parse(inp, out, tree, data):
	f = open(inp, "r")
	tpl = f.read()
	f.close()

	vb = bytearray()
	for b in data:
		if b == ord('"') or b == ord('\\'):
			vb.append(ord("\\"))
		vb.append(b)

	f = open(out, "wb")

	f.write('/** ')
	f.write(vb)
	f.write(' **/\n')

	f.write('var t="')
	f.write(tree.replace(u'\\', u'\\\\').replace(u'"', u'\\"').encode('utf-8'))
	f.write('";\n\n')

	f.write(tpl)
	f.close()
