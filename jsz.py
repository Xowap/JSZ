#!/usr/bin/python
# vim: fileencoding=utf8 :

# Copyright 2011 Rémy Sanchez <remy.sanchez (a)_ hyperthese.net>
# Under the terms of the WTFPL

import sys

if __name__ != "__main__":
	raise Exception("jsz is not supposed to be loaded by another module")
	sys.exit(1)

##
# Parse options
##

from optparse import OptionParser

parser = OptionParser()

parser.add_option("-i", "--input", dest="input", help="File to compress")
parser.add_option("-o", "--output", dest="output", help="Write compressed file into")
parser.add_option("-c", "--charset", dest="charset", default="utf-8", help="Input file charset")
parser.add_option("-t", "--template", dest="template", default="./template.js", help="Template file that includes decompression code")
parser.add_option("-p", "--print-tree", dest="print_tree", default=True, help="Prints the tree that is written into Javascript", action="store_false")

(o, args) = parser.parse_args()

if o.input is None:
	print "You must specify an input file"
	sys.exit(-1)

if o.output is None:
	print "You must specify an output file"
	sys.exit(-1)

##
# Read file
##

import codecs
f = codecs.open(o.input, "r", o.charset)
in_str = f.read()
f.close()


##
# Do the Huffman stuff
##

from huffman import *
t = tokenize(in_str)
d = stats(t)
tree = mktree(d)
enc = encode(t, tree_to_bin(tree))

##
# Save the template
##

from template import parse
from binhelp import *
parse(o.template, o.output, tree = reptree(tree), data = enc.encode())

if not o.print_tree:
	print reptree(tree)
