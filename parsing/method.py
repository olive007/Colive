# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Method.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 27/10/2015 12:22:02
# Last update by olive007 at 29/10/2015 20:42:49

import re

from parsing import Instruction
from parsing import Variable
from parsing import ParserException

class Argument(Variable):
	"""
		Argument
	"""

	def __init(self, type, name="arg"):
		super(Argument, self).__init__(type, "arg")


class Method(Instruction):
	"""Method
		This class is defined by
		- name
		- returnType
		- arguments
		- const or not
		- static or not
	"""
	def __init__(self, name, static=False):
		super(Method, self).__init__(static)
		self._name = re.sub("\s+", " ", name.strip())
		self._const = False
		self._virtual = False
		self._returnType = None
		self._arguments = []

	### Getter
	def getConst(self):
		return self._const

	### Setter
	def setConst(self, arg):
		if not (isinstance(arg, bool)):
			raise ParserException("Wrong argument")
		self._const = arg

	def setReturnType(self, arg):
		self._returnType = re.sub("\s+", " ", arg.strip())

	def setVirtual(self, arg):
		if not (isinstance(arg, bool)):
			raise ParserException("Wrong argument")
		self._virtual = arg

	def addArgument(self, type, name=None, defaultValue=None):
		if (name == None):
			name = "arg"
		self._arguments.append(Variable(type, name, value=defaultValue))


	### Method
	def show(self, space=""):
		super(Method, self).show(space)
		arg = ""
		for tmp in self._arguments:
			if (self._arguments.index(tmp) == 0):
				arg += tmp.getType()
			else:
				arg += ", "+tmp.getType()
			if tmp.getValue():
				arg += "(%s)" % tmp.getValue()
		tmp = ""
		if (self._virtual):
			tmp += "virtual "
		if self._returnType:
			tmp += self._returnType+" "
		tmp += self._name
		print("%s(%s)" % (tmp, arg))
		
		