#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# instruction.py
# Project : unknown
# Contact : info@devolive.be
# Created by olive007 at 02/11/2015 15:28:44
# Last update by olive007 at 04/11/2015 20:00:30

class Instruction(object):
	"""
		Instruction
	"""
	def __init__(self, static):
		super(Instruction, self).__init__()
		self._static = static

	### Getter
	def getStatic(self):
		return self._static


	### Setter
	def setStatic(self, arg):
		if not (isinstance(arg, bool)):
			raise ParserException("Wrong argument")
		self._static = arg


	### Method
	def show(self, space=""):
		res = ""
		if (self._static):
			res += "static "
		print("%s%s" % (space, res), end="")
