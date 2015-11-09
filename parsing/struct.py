#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# struct.py
# Project : unknown
# Contact : info@devolive.be
# Created by olive007 at 04/11/2015 11:45:06
# Last update by olive007 at 09/11/2015 08:52:46

from parsing import CppClass

class Struct(CppClass):
	"""
		Struct
	"""

	def __init__(self, parent, name):
		super(Struct, self).__init__(parent, name)

	### Method
	def show(self, space=""):
		print("%sStruct: %s" % (space, self.name))
		super(Struct, self).showCommon(space)
