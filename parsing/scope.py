#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Scope.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 27/10/2015 15:44:12
# Last update by olive007 at 02/11/2015 15:20:19

import re
import parsing

class Scope(object):
	"""Scope
		This class is defined by
		- namespace
		- method
		- variable
		- class
	"""

	def __init__(self):
		self._namespaces = []
		self._classs = []
		self._methods = []
		self._variables = []

	### Getter
	def getContents(self):
		self._contents = ""

	### Method
	def addNamespace(self, namespace):
		self._namespaces.append(namespace)

	def addClass(self, classData):
		self._classs.append(classData)

	def addInstruction(self, instruction):
		if (isinstance(instruction, parsing.method.Method)):
			self._methods.append(instruction)
		elif (isinstance(instruction, parsing.method.Variable)):
			self._variables.append(instruction)

	def show(self, space=""):
		for tmp in self._namespaces:
			tmp.show(space)

		for tmp in self._classs:
			tmp.show(space)

		for tmp in self._methods:
			tmp.show(space)

		for tmp in self._variables:
			tmp.show(space)
