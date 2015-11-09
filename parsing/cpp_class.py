#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Class.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 27/10/2015 12:22:20
# Last update by olive007 at 09/11/2015 08:52:22

from parsing import Scope
from parsing import Visibility
from parsing import Method
from parsing import Variable

class CppClass(Scope):
	"""
		Class
		This class is defined by name
		- Attributes
		- Methods
	"""
	def __init__(self, parent, name):
		super(CppClass, self).__init__(parent)
		self.__name = name
		self.__attributes = {}
		self.__methods = {}

	### Getter
	@property
	def name(self):
	    return self.__name
	
	def getId(self):
		return self.__name

	def getMethod(self, id):
		try:
			return self.__attributes[id]
		except KeyError:
			pass
		return None

	def getAttribute(self, id):
		try:
			return self.__attributes[id][0]
		except KeyError:
			pass
		return None

	def getAllAttributeName(self):
		tab = []
		for tmp in self.__attributes:
			tab.append(tmp)
		return tab;

	def getAllPrivateAttributeName(self):
		tab = []
		for tmp in self.__attributes:
			if self.__attributes[tmp][1] == Visibility.private:
				tab.append(tmp)
		return tab;


	### Method
	def addInstruction(self, instruction, visibility):
		if isinstance(visibility, Visibility):
			if (isinstance(instruction, Method)):
				self.__methods[instruction.getId()] = [instruction, visibility]
			elif (isinstance(instruction, Variable)):
				self.__attributes[instruction.getId()] = [instruction, visibility]


	def show(self, space=""):
		print("%sClass: %s" % (space, self.__name))
		self.showCommon(space)

	def showCommon(self, space):
		"""
			Used by Struct too
		"""
		space = "%s\t" % space
		for data in [self.__attributes, self.__methods]:
			private = protected = public = 0
			for key in data:
				if data[key][1] == Visibility.private:
					if (private == 0):
						print("%s%s" % (space, Visibility.private.name))
					data[key][0].show("\t%s" % space)
					private += 1
				elif data[key][1] == Visibility.protected:
					if (protected == 0):
						print("%s%s" % (space, Visibility.protected.name))
					data[key][0].show("\t%s" % space)
					protected += 1
				else:
					if (public == 0):
						print("%s%s" % (space, Visibility.public.name))
					data[key][0].show("\t%s" % space)
					public += 1
