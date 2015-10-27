#!/usr/bin/env python
# Method.py encoded in UTF-8
# Project : unknown
# Contact : example@domain.com
# Created by olive007 at 27/10/2015 12:22:02
# Last update by olive007 at 27/10/2015 12:38:58

import Argument

class Method:
	"""Method
		This class is defined by
		- name
		- returnType
		- arguments
		- const or not
		- static or not
	"""
	def __init__(self, arg):
		self._name = ""
		self._const = False
		self._static = False
		self._returnType = ""
		self._arguments = []
		