#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Variable.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 29/10/2015 20:38:59
# Last update by olive007 at 04/11/2015 20:11:55

import re

from parsing import Instruction

class Variable(Instruction):
	"""Variable
		This class is defined by
		- name
		- type
	"""

	def __init__(self, type, name, static=False, value=None):
		super(Variable, self).__init__(static)
		self._name = re.sub("\s+", " ", name.strip())
		self._type = re.sub("\s+", " ", type.strip())
		self._value = value

	### Getter
	def getName(self):
		return self._name

	def getType(self):
		return self._type

	def getValue(self):
		return self._value

	### Setter
	def setValue(self, arg):
		if (isinstance(arg, str)):
			self._value = re.sub("\s+", " ", arg)

	### Method
	def show(self, space=""):
		super(Variable, self).show(space)
		if (self._value):
			print("%s %s = %s" % (self._type, self._name, self._value))
		else:
			print(self._type, self._name)


