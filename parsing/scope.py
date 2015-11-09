#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Scope.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 27/10/2015 15:44:12
# Last update by olive007 at 09/11/2015 09:56:56

import os

class Scope(object):
	"""Scope
		This class contents
		- namespace
		- class
		- struct
		- method
		- variable
	"""

	def __init__(self, parent = None):
		if parent:
			self.parent = parent
		else:
			self.__parent = None
		self.__scopes = {}
		self.__methods = {}
		self.__variables = {}

	### Getter
	@property
	def parent(self):
	    return self.__parent
	
	def getScope(self, id):
		return self.__scopes[id]

	def getMethod(self, id):
		return self.__methods[id]

	def getVariable(self, id):
		return self.__variables[id]

	def __generatePath(self, folder, extend):
		from parsing import CppClass, Struct, Parser, Project

		if not isinstance(self, CppClass) and not isinstance(self, Struct):
			return None
		folders = []
		tmp = self
		while tmp.__parent:
			folders.append(Parser.lowerCase(tmp.name))
			tmp = tmp.__parent
		folders.reverse()
		if not (isinstance(tmp, Project)):
			return None
		path = tmp.projectFolder
		path = os.path.join(path, folder)
		for tmp in folders:
			path = os.path.join(path, tmp)
		path += "."+extend
		return path

	def getSourcePath(self):
		from parsing import SOURCE_FOLDER, SOURCE_EXTEND
		return self.__generatePath(SOURCE_FOLDER, SOURCE_EXTEND)

	def getIncludePath(self):
		from parsing import INCLUDE_FOLDER, INCLUDE_EXTEND
		return self.__generatePath(INCLUDE_FOLDER, INCLUDE_EXTEND)

	### Setter
	@parent.setter
	def parent(self, val):
		from parsing import ParserException

		if not isinstance(val, Scope):
			raise ParserException("Parent is not correct")
		self.__parent = val

	### Method
	def addScope(self, new):
		from parsing import Project, Namespace, CppClass, Struct, ParserException

		if not (isinstance(new, Namespace)) and not (isinstance(new, CppClass)) and not (isinstance(new, Struct)):
			raise ParserException("trying to add wrong scope")
		self.__scopes[new.getId()] = new

	def addInstruction(self, new):
		from parsing import Method, Variable

		if (isinstance(new, Method)):
			if new.getName() in self.__variables:
				raise ParsingException("one variable have already this name: "+new.getName())
			self.__methods[new.getId()] = new
		elif (isinstance(new, Variable)):
			for key in self._methods:
				if self.__methods[key].getName() == new.getName():
					raise ParsingException("one method have already this name: "+new.getName())
			self.__variables[new.getId()] = new
		else:
			raise ParsingException("trying to add wrong instruction")

	def show(self, space=""):
		for key in self.__scopes:
			self.__scopes[key].show(space)

		for key in self.__methods:
			self.__methods[key].show(space)

		for key in self.__variables:
			self.__variables[key].show(space)
