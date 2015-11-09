#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# instruction.py
# Project : unknown
# Contact : info@devolive.be
# Created by olive007 at 02/11/2015 15:28:44
# Last update by olive007 at 08/11/2015 17:16:58

class Instruction(object):
	"""
		Instruction
	"""
	def __init__(self, static):
		super(Instruction, self).__init__()
		self.static = static

	### Getter
	@property
	def static(self):
		return self.__static

	### Setter
	@static.setter
	def static(self, val):
		if not (isinstance(val, bool)):
			self.__static = False
		self.__static = val


	### Method
	def show(self, space=""):
		if (self.__static):
			print("%sstatic " % space, end="")
		else:
			print(space, end="")
