#!/usr/bin/python
# vim: fileencoding=utf8 :

# Copyright 2011 Rémy Sanchez <remy.sanchez (a)_ hyperthese.net>
# Under the terms of the WTFPL

from binhelp import *

def tokenize(string):
	tokens = []
	keywords = ('break', 'continue', 'do', 'for', 'import', 'new', 'this', 'void', 'case', 'default', 'else', 'function', 'in', 'return', 'typeof', 'while', 'comment', 'delete', 'export', 'if', 'label', 'switch', 'var', 'with', 'abstract', 'implements', 'protected', 'boolean', 'instanceOf', 'public', 'byte', 'int', 'short', 'char', 'interface', 'static', 'double', 'long', 'synchronized', 'false', 'native', 'throws', 'final', 'null', 'transient', 'float', 'package', 'true', 'goto', 'private', 'catch', 'enum', 'throw', 'class', 'extends', 'try', 'const', 'finally', 'debugger', 'super', 'alert', 'eval', 'Link', 'outerHeight', 'scrollTo', 'Anchor', 'FileUpload', 'location', 'outerWidth', 'Select', 'Area', 'find', 'Location', 'Packages', 'self', 'arguments', 'focus', 'locationbar', 'pageXoffset', 'setInterval', 'Array', 'Form', 'Math', 'pageYoffset', 'setTimeout', 'assign', 'Frame', 'menubar', 'parent', 'status', 'blur', 'frames', 'MimeType', 'parseFloat', 'statusbar', 'Boolean', 'Function', 'moveBy', 'parseInt', 'stop', 'Button', 'getClass', 'moveTo', 'Password', 'String', 'callee', 'Hidden', 'name', 'personalbar', 'Submit', 'caller', 'history', 'NaN', 'Plugin', 'sun', 'captureEvents', 'History', 'navigate', 'print', 'taint', 'Checkbox', 'home', 'navigator', 'prompt', 'Text', 'clearInterval', 'Image', 'Navigator', 'prototype', 'Textarea', 'clearTimeout', 'Infinity', 'netscape', 'Radio', 'toolbar', 'close', 'innerHeight', 'Number', 'ref', 'top', 'closed', 'innerWidth', 'Object', 'RegExp', 'toString', 'confirm', 'isFinite', 'onBlur', 'releaseEvents', 'unescape', 'constructor', 'isNan', 'onError', 'Reset', 'untaint', 'Date', 'java', 'onFocus', 'resizeBy', 'unwatch', 'defaultStatus', 'JavaArray', 'onLoad', 'resizeTo', 'valueOf', 'document', 'JavaClass', 'onUnload', 'routeEvent', 'watch', 'Document', 'JavaObject', 'open', 'scroll', 'window', 'Element', 'JavaPackage', 'opener', 'scrollbars', 'Window', 'escape', 'length', 'Option', 'scrollBy')
	offset = 0

	i = 0
	while i < len(string):
		cnt = False

		for w in keywords:
			if string[i:i+len(w)] == w:
				i += len(w)
				tokens.append(w)
				cnt = True
				break

		if cnt:
			cnt = False
			continue

		tokens.append(string[i])
		i += 1

	return tokens

def stats(tokens):
	from operator import itemgetter

	dico = {}

	for t in tokens:
		if t in dico:
			dico[t] += 1
		else:
			dico[t] = 1

	return sorted(dico.items(), key = itemgetter(1), reverse = True)

def mktree(distrib, prefix = ""):
	from operator import attrgetter

	class Node:
		def __init__(self, symbol = None, value = 0):
			self.left = None
			self.right = None
			self.symbol = symbol
			self.value = value

	base = [Node(s, v) for (s, v) in distrib]

	while len(base) > 1:
		# Create the new node
		n = Node()

		# We're going to pop smallest nodes into the new node
		try:
			n.left = base.pop()
			n.value += n.left.value

			n.right = base.pop()
			n.value += n.right.value
		except:
			pass

		# Insert and sort again
		# TODO do insertion sorting...
		base.append(n)
		base = sorted(base, key = attrgetter("value"), reverse = True)

	return base[0]

def tree_to_bin(node, prefix = ""):
	out = {}

	if node != None:
		if node.symbol != None:
			out[node.symbol] = prefix
		else:
			out.update(tree_to_bin(node.left, prefix + "0"))
			out.update(tree_to_bin(node.right, prefix + "1"))

	return out

def tree_stats(distrib, tree):
	total = 0

	for (k, v) in distrib:
		total += v * len(tree[k])

	print "Total %d bits / %f octets" %  (total, total/8)

def mkbintree(tree):
	out = BinString()

	# Start with the size of tree
	out += tobinrep(len(tree), 16)

	for (k, v) in tree.items():
		k = k.encode("utf8")

		# key_s
		out += tobinrep(len(k), 4)

		# val_s
		out += tobinrep(len(v), 6)

		# key
		for c in k:
			out += tobinrep(ord(c), 8)

		# val
		out += v

	return out

def reptree(node, charset = 'utf-8'):
	from json import JSONEncoder
	enc = JSONEncoder(encoding = charset)

	if node.symbol is not None:
		return enc.encode(node.symbol)
	else:
		return "c()?" + reptree(node.right) + ":" + reptree(node.left)

def encode(tokens, tree):
	s = BinString()
	for t in tokens:
		s += tree[t]
	return s
