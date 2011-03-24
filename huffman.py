#!/usr/bin/python
# vim: fileencoding=utf8 :

def tokenize(string):
	tokens = []
	# http://www.quackit.com/javascript/javascript_reserved_words.cfm (to complete)
	# trier la liste par ordre de longueur
	keywords = ("break", "continue", "do", "for", "import", "new", "this", "void", "case", "default", "else", "function", "return", "typeof", "while", "comment", "delete", "export", "if", "label", "switch", "var", "with", "include", "in")
	keywords = ('break', 'continue', 'do', 'for', 'import', 'new', 'this', 'void', 'case', 'default', 'else', 'function', 'in', 'return', 'typeof', 'while', 'comment', 'delete', 'export', 'if', 'label', 'switch', 'var', 'with', 'abstract', 'implements', 'protected', 'boolean', 'instanceOf', 'public', 'byte', 'int', 'short', 'char', 'interface', 'static', 'double', 'long', 'synchronized', 'false', 'native', 'throws', 'final', 'null', 'transient', 'float', 'package', 'true', 'goto', 'private', 'catch', 'enum', 'throw', 'class', 'extends', 'try', 'const', 'finally', 'debugger', 'super', 'alert', 'eval', 'Link', 'outerHeight', 'scrollTo', 'Anchor', 'FileUpload', 'location', 'outerWidth', 'Select', 'Area', 'find', 'Location', 'Packages', 'self', 'arguments', 'focus', 'locationbar', 'pageXoffset', 'setInterval', 'Array', 'Form', 'Math', 'pageYoffset', 'setTimeout', 'assign', 'Frame', 'menubar', 'parent', 'status', 'blur', 'frames', 'MimeType', 'parseFloat', 'statusbar', 'Boolean', 'Function', 'moveBy', 'parseInt', 'stop', 'Button', 'getClass', 'moveTo', 'Password', 'String', 'callee', 'Hidden', 'name', 'personalbar', 'Submit', 'caller', 'history', 'NaN', 'Plugin', 'sun', 'captureEvents', 'History', 'navigate', 'print', 'taint', 'Checkbox', 'home', 'navigator', 'prompt', 'Text', 'clearInterval', 'Image', 'Navigator', 'prototype', 'Textarea', 'clearTimeout', 'Infinity', 'netscape', 'Radio', 'toolbar', 'close', 'innerHeight', 'Number', 'ref', 'top', 'closed', 'innerWidth', 'Object', 'RegExp', 'toString', 'confirm', 'isFinite', 'onBlur', 'releaseEvents', 'unescape', 'constructor', 'isNan', 'onError', 'Reset', 'untaint', 'Date', 'java', 'onFocus', 'resizeBy', 'unwatch', 'defaultStatus', 'JavaArray', 'onLoad', 'resizeTo', 'valueOf', 'document', 'JavaClass', 'onUnload', 'routeEvent', 'watch', 'Document', 'JavaObject', 'open', 'scroll', 'window', 'Element', 'JavaPackage', 'opener', 'scrollbars', 'Window', 'escape', 'length', 'Option', 'scrollBy')
	offset = 0

	i = 0
	while i < len(string):
		cnt = False

		#if i % 100 == 0:
			#print "offset %d" % i

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

def _tobinrep(val, size):
	return bin(val)[2:].zfill(size)

def _totruebin(string):
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

def _fromtruebin(b):
	leftout = b[0]

	out = ""

	for c in b[1:]:
		out += _tobinrep(c, 8)

	if leftout > 0:
		out = out[:-leftout]

	return out

def mkbintree(tree):
	out = ""

	# Start with the size of tree
	out += _tobinrep(len(tree), 16)

	for (k, v) in tree.items():
		k = k.encode("utf8")

		# key_s
		out += _tobinrep(len(k), 4)

		# val_s
		out += _tobinrep(len(v), 6)

		# key
		for c in k:
			out += _tobinrep(ord(c), 8)

		# val
		out += v

	return out

def reptree(node):
	if node.symbol is not None:
		return "'" + node.symbol.replace("\\", "\\\\").replace("'", "\\'").replace('\n', '\\n') + "'"
	else:
		return "c" + reptree(node.right) + ":" + reptree(node.left)

def reptree_target(node):
	if node.symbol is not None:
		return "'" + node.symbol.replace("\\", "\\\\").replace("'", "\\'") + "'"
	else:
		return "c() ? (" + reptree_target(node.right) + " : " + reptree_target(node.left) + ")"

def encode(tokens, tree):
	s = ""
	for t in tokens:
		s += tree[t]
	return s

if __name__ ==  "__main__":
	import codecs
	t = tokenize(codecs.open("./jquery-1.5.1.min.js", "r", "utf-8").read())
	#t = tokenize(u"Ecrivons autre chose...")
	print "tokenized"
	d = stats(t)
	print "distribution ok"
	tree = mktree(d)
	print "tree ok"

	def print_node(node, indent = ""):
		if node != None:
			print "%s- %d (%s)" % (indent, node.value, node.symbol)
			print_node(node.left, indent + " ")
			print_node(node.right, indent + " ")

	from pprint import pprint
	pprint(tree_to_bin(tree))

	#print mkbintree(tree_to_bin(tree))

	#bintree = _totruebin(mkbintree(tree))
	#print " ".join([hex(v) for v in bintree])
	#print _fromtruebin(bintree)

	enc = encode(t, tree_to_bin(tree))
	#print enc
	#print _totruebin(enc)
	#print _fromtruebin(_totruebin(enc))

	from template import parse
	parse("/tmp/lena.bmp", "/tmp/lena.out.js", tree = reptree(tree), data = _totruebin(enc))
