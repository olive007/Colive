#!/usr/bin/env python
# Colive.py encoded in UTF-8
# Project : unknown
# Contact : example@domain.com
# Created by olive007 at 27/10/2015 12:30:26
# Last update by olive007 at 27/10/2015 12:30:27

import sublime, sublime_plugin

from Parsing import *

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")
