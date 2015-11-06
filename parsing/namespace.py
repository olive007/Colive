#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Namespace.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 27/10/2015 12:23:36
# Last update by olive007 at 31/10/2015 21:59:59

from parsing import Scope

class Namespace(Scope):
	"""Namespace
		This class is defined by
		- name
		- class
		- variable
	"""
	def __init__(self, name):
		super(Namespace, self).__init__()
		self._name = name
		self._scope = []
		self._instruction = []

	def show(self, space=""):
		print("%sNamespace: %s" % (space, self._name))
		space = "%s\t" % space
		super(Namespace, self).show(space)