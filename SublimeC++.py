#!/usr/bin/env python
# SublimeC++.py encoded in UTF-8
# Project : YamlParser
# Contact : info@devolive.be
# Created by olive007 at 31/07/2015 23:51:03
# Last update by olive007 at 31/07/2015 23:51:15

import sublime, sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.insert(edit, 0, "Hello, World!")
