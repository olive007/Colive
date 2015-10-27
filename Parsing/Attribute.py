#!/usr/bin/env python
# Attribute.py encoded in UTF-8
# Project : unknown
# Contact : example@domain.com
# Created by olive007 at 27/10/2015 12:19:14
# Last update by olive007 at 27/10/2015 12:35:50

class Attribute:

	"""Attribute
		This class is defined by
		- name
		- type
		- const or not
		- static or not
	"""
	
	def __init__(self):
		self._name = ""
		self._const = False
		self._static = False
		self._type = ""
		