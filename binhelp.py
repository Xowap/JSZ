#!/usr/bin/python
# vim: fileencoding=utf8 :

# Copyright 2011 Rémy Sanchez <remy.sanchez (a)_ hyperthese.net>
# Under the terms of the WTFPL

class BinString(object):
	def __init__(self, value = ""):
		self.bytes = bytearray()
		self.size = 0

		self.append(value)

	def append_bit(self, bit):
		if not isinstance(bit, (int, bool)):
			raise TypeError('Trying to append invalid bit')

		# Shall we extend the byte array ?
		if self.size % 8 == 0:
			self.bytes.append(0)

		octet = int(self.size / 8)
		offset = self.size % 8

		if bit:
			self.bytes[octet] = self.bytes[octet] | (128 >> offset)

		self.size += 1

	def append(self, other):
		if isinstance(other, str):
			for i in other:
				if i != '0' and i != '1':
					raise TypeError("Malformated string, must only contain 0 and 1")
				self.append_bit(i == '1')
		elif isinstance(other, BinString):
			self.bytes += other.bytes
			self.size += other.size
		elif isinstance(other, int):
			self.append_bit(other != 0)
		elif isinstance(other, bool):
			self.append_bit(other)
		else:
			raise TypeError('Unable to add this to the binary string')

	def __add__(self, other):
		out = BinString()
		out.bytes = self.bytes
		out.size = self.size

		out.append(other)

		return out

	def __iadd__(self, other):
		self.append(other)
		return self

	def get_bit(self, idx):
		return self.bytes[int(idx / 8)] & (128 >> (idx % 8)) != 0

	def __len__(self):
		return self.size

	def __getitem__(self, key):
		if not isinstance(key, int):
			raise TypeError("Indice must be int")

		if key >= self.size or key < 0:
			raise IndexError("Out of range")

		return self.get_bit(key)

	def bin(self):
		out = ""
		for i in range(0, len(self)):
			if self[i]:
				out += "1"
			else:
				out += "0"

		return out

	def encode(self):
		from struct import pack
		out = bytearray()

		# number of trailing useless bits
		out.append((8 - len(self) % 8) % 8)

		# escape comment ends
		b = self.bytes
		places = []
		for i in range(1, len(b)):
			if b[i] == 47:
				if b[i - 1] == 42:
					b[i] = 42
					places.append(i)
					print "bad = %d" % i

		print "bad string found %d times" % len(places)
		out += pack("H", len(places))
		for i in range(0, len(places)):
			out += pack("I", places[i])

		out += self.bytes
		return out

def tobinrep(val, size):
	return bin(val)[2:].zfill(size)
