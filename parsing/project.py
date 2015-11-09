#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# project.py
# Project : unknown
# Contact : info@devolive.be
# Created by olive007 at 31/10/2015 15:10:58
# Last update by olive007 at 09/11/2015 09:07:02

from parsing import Scope

class Project(Scope):
	"""
		Project
	"""

	def __init__(self, projectFolder):
		super(Project, self).__init__()
		self.projectFolder = projectFolder

	### Getter
	@property
	def projectFolder(self):
	    return self.__projectFolder
	
	def getId(self):
		return self.__projectFolder

	### Setter
	@projectFolder.setter
	def projectFolder(self, val):
		if val:
			tmp = val.strip()
			if tmp != "":
				self.__projectFolder = tmp
			else:
				raise ParserException("Wrong argument: projectFolder is not correct")
		else:
			raise ParserException("Wrong argument: projectFolder is null")

	### Method
	def show(self, space=""):
		print("Id (projectFolder):", self._id)
		space = "%s\t" % space
		super(Project, self).show(space)
