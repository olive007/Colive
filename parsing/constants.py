#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# constante.py
# Project : unknown
# Contact : info@devolive.be
# Created by olive007 at 30/10/2015 10:02:11
# Last update by olive007 at 06/11/2015 17:51:01

from parsing.enum34.enum import Enum

SOURCE_FOLDER = "src"
INCLUDE_FOLDER = "include"

SOURCE_EXTEND = "cpp"
INCLUDE_EXTEND = "hpp"

class Type(Enum):
	source = 1
	include = 2

class Visibility(Enum):
	private = 0
	protected = 1
	public = 2

	@classmethod
	def parse(cls, str):
		return getattr(cls, str.lower(), None)
