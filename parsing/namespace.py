#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Namespace.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 27/10/2015 12:23:36
# Last update by olive007 at 09/11/2015 08:52:34

import re

from parsing import Scope

class Namespace(Scope):
	"""
		Namespace
		This class is defined by name
	"""
	def __init__(self, parent, name):
		super(Namespace, self).__init__(parent)
		self.name = name
		
	### Getter
	@property
	def name(self):
	    return self.__name
	
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

	### Method
	def show(self, space=""):
		print("%sNamespace: %s" % (space, self._name))
		space = "%s\t" % space
		super(Namespace, self).show(space)