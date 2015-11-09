#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Variable.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 29/10/2015 20:38:59
# Last update by olive007 at 08/11/2015 17:47:24

import re

from parsing import Instruction, ParserException

class Variable(Instruction):
	"""Variable
		This class is defined by
		- name
		- type
	"""

	def __init__(self, type, name, static=False, value=None):
		super(Variable, self).__init__(static)
		self.type = type
		self.name = name
		self.value = value

	### Getter
	@property
	def type(self):
		return self.__type

	@property
	def name(self):
		return self.__name

	@property
	def value(self):
		return self.__value
	
	def getId(self):
		return self.__name

	### Setter
	@name.setter
	def name(self, val):
		if val:
			tmp = val.strip()
			if re.match("^\w+$", tmp):
				self.__name = tmp
			else:
				raise ParserException("Wrong argument: name is not correct")
		else:
			raise ParserException("Wrong argument: name is null")

	@type.setter
	def type(self, val):
		if val:
			tmp = re.sub("\s+", " ", val.strip())
			if tmp != "":
				self.__type = tmp
			else:
				raise ParserException("Wrong argument: type is not correct")
		else:
			raise ParserException("Wrong argument: type is null")

	@value.setter
	def value(self, val):
		self.__value = val

	### Method
	def show(self, space=""):
		super(Variable, self).show(space)
		if (self._value):
			print("%s %s = %s" % (self._type, self._name, self._value))
		else:
			print(self._type, self._name)


