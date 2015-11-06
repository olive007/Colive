#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Class.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 27/10/2015 12:22:20
# Last update by olive007 at 04/11/2015 18:59:39

from parsing import Scope
from parsing import Visibility
from parsing import Method
from parsing import Variable

class CppClass(Scope):
	"""Class
		This class is defined by
		- name
		- Attributes
		- Methods
	"""
	def __init__(self, name):
		super(CppClass, self).__init__()
		self._name = name
		self._attributes = {}
		self._attributes[Visibility.private] = []
		self._attributes[Visibility.protected] = []
		self._attributes[Visibility.public] = []
		self._methods = {}
		self._methods[Visibility.private] = []
		self._methods[Visibility.protected] = []
		self._methods[Visibility.public] = []
		
	### Method
	def addInstruction(self, instruction, visibility):
		if isinstance(visibility, Visibility):
			if (isinstance(instruction, Method)):
				self._methods[visibility].append(instruction)
			elif (isinstance(instruction, Variable)):
				self._attributes[visibility].append(instruction)


	def show(self, space=""):
		print("%sClass: %s" % (space, self._name))
		self.showCommon(space)

	def showCommon(self, space):
		"""
			Used by Struct too
		"""
		space = "%s\t" % space
		for data in [["Attribute", self._attributes], ["Method", self._methods]]:
			if (len(data[1][Visibility.private]) +
				len(data[1][Visibility.protected]) +
				len(data[1][Visibility.public]) > 0):
				print("%s%s" % (space, data[0]))
				for vis in {Visibility.private, Visibility.protected, Visibility.public}:
					if (len(data[1][vis])):
						print("%s%s:" % (space, vis.name))
						for tmp in data[1][vis]:
							tmp.show("\t%s" % space)
