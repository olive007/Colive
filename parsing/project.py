#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# project.py
# Project : unknown
# Contact : info@devolive.be
# Created by olive007 at 31/10/2015 15:10:58
# Last update by olive007 at 31/10/2015 21:55:34

from parsing import Scope

class Project(Scope):
	"""
		Project
	"""

	def __init__(self, id):
		super(Project, self).__init__()
		self._id = id
		self._namespaces = []
		self._classs = []
		self._methods = []
		self._variables = []

	def getId(self):
		return self._id

	def getNamespace(self, name):
		return self._namespaces[name]

	def getClass(self, name):
		return self._classs[name]

	def getMethod(self, name):
		return self._methods[name]

	def getVariable(self, name):
		return self._variables[name]

	### Method
	def addNamespace(self, namespace):
		self._namespaces.append(namespace)

	def show(self, space=""):
		print("Id (projectFolder):", self._id)
		space = "%s\t" % space
		super(Project, self).show(space)
