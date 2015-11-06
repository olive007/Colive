#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# struct.py
# Project : unknown
# Contact : info@devolive.be
# Created by olive007 at 04/11/2015 11:45:06
# Last update by olive007 at 04/11/2015 11:48:19

from parsing import CppClass

class Struct(CppClass):
	"""
		Struct
	"""
	def __init__(self, name):
		super(Struct, self).__init__(name)

	def show(self, space=""):
		print("%sStruct: %s" % (space, self._name))
		super(Struct, self).showCommon(space)
