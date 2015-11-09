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
		self.name = name
		self.__const = False
		self.__virtual = False
		self.__returnType = None
		self.__arguments = []

	### Getter
	@property
	def name(self):
		return self.__name

	@property
	def const(self):
		return self.__const
	
	@property
	def virtual(self):
		return self.__virtual
	
	@property
	def returnType(self):
		return self.__returnType

	def getId(self):
		tmp = self.__name
		for arg in self.__arguments:
			tmp += arg.type
		return tmp

	def getConst(self):
		return self._const

	### Setter
	@name.setter
	def name(self, val):
		if val:
			tmp = val.strip()
			if re.match("^[~\w]+$", tmp):
				self.__name = tmp
			else:
				raise ParserException("Wrong argument: name is not correct")
		else:
			raise ParserException("Wrong argument: name is null")


	@const.setter
	def const(self, val):
		if not (isinstance(val, bool)):
			self.__const = False
		self.__const = val

	@virtual.setter
	def virtual(self, val):
		if not (isinstance(val, bool)):
			self.__const = False
		self.__const = val

	@returnType.setter
	def returnType(self, val):
		if val:
			self.__returnType = re.sub("\s+", " ", val.strip())
		if self.__returnType == "":
			self.__returnType = None

	### Method
	def addArgument(self, type, name=None, defaultValue=None):
		if (name == None):
			name = "arg"
		self.__arguments.append(Variable(type, name, value=defaultValue))


	def show(self, space=""):
		super(Method, self).show(space)
		arg = ""
		for tmp in self.__arguments:
			if (self.__arguments.index(tmp) == 0):
				arg += tmp.getType()
			else:
				arg += ", "+tmp.getType()
			if tmp.getValue():
				arg += "(%s)" % tmp.getValue()
		tmp = ""
		if (self.__virtual):
			tmp += "virtual "
		if self.__returnType:
			tmp += self.__returnType+" "
		tmp += self.__name
		print("%s(%s)" % (tmp, arg))
		
		