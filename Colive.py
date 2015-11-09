#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Colive.py
# Project : Colive
# Contact : info@devolive.be
# Created by olive007 at 27/10/2015 15:40:24
# Last update by olive007 at 09/11/2015 23:35:11

import os
import re
import sys
import sublime
import sublime_plugin

def plugin_loaded():
	global PLUGIN_NAME
	global PLUGIN_PATH
	global SOURCE_EXTEND
	global INCLUDE_EXTEND

	PLUGIN_NAME = "Colive"
	PLUGIN_PATH = os.path.join(sublime.packages_path(), PLUGIN_NAME)

	sys.path.append(PLUGIN_PATH)
	sys.path.append(os.path.join(PLUGIN_PATH, "jinja2"))
	sys.path.append(os.path.join(PLUGIN_PATH, "markupsafe"))

	from jinja2 import Environment, FileSystemLoader
	global Environment
	global FileSystemLoader
	
	SOURCE_EXTEND = "cpp"
	INCLUDE_EXTEND = "hpp"

def getTemplateEngine():
	env = Environment(loader=FileSystemLoader(os.path.join(PLUGIN_PATH, 'templates')))
		# Custom filter method
	def regexReplace(s, find, replace):
		"""A non-optimal implementation of a regex filter"""
		return re.sub(find, replace, s)


	def removeUnderscore(s):
		res = re.match("^_*([a-z])(.+)$", s)
		s = res.group(1).upper() + res.group(2)
		return s

	env.filters['regexReplace'] = regexReplace
	env.filters['removeUnderscore'] = removeUnderscore
	return env

def getParser():
	from parsing import Parser, CppClass

	parser = Parser()
	return parser

def getSettings():
	return sublime.load_settings(PLUGIN_NAME+".sublime-settings")

def underline_error(view, region):
	view.add_regions(("Error_%d_%d" % (region.begin(), region.end())),
		[region],
		"Error",
		"bookmark",
		sublime.DRAW_SQUIGGLY_UNDERLINE|sublime.DRAW_NO_FILL|sublime.DRAW_NO_OUTLINE
		)

def underline_warning(view, region):
	view.add_regions(("Warning_%d_%d" % (region.begin(), region.end())),
		[region],
		"Warning",
		"bookmark",
		sublime.DRAW_STIPPLED_UNDERLINE|sublime.DRAW_NO_FILL|sublime.DRAW_NO_OUTLINE
		)

def remove_underline(view, region):
	view.erase_regions("Error_%d_%d" % (region.begin(), region.end()))
	view.erase_regions("Warning_%d_%d" % (region.begin(), region.end()))

def getSyntax(view):
	return os.path.basename(view.settings().get('syntax'))

def renderTemplate(type, arg, classData):
	sourcePath = os.path.join("source", type+".tmpl")
	includePath = os.path.join("include", type+".tmpl")
	env = getTemplateEngine()

	template = env.get_template(sourcePath)
	sourceRender = template.render(arg=arg, classData=classData)

	template  = env.get_template(includePath)
	includeRender = template.render(arg=arg, classData=classData)
	
	return {"source": sourceRender, "include": includeRender}

def getClass(view):
	parser = getParser()

	filePath = view.file_name()
	project = parser.parse(filePath)
	
	fileContents = view.substr(sublime.Region(0, view.sel()[0].begin()))
	currentScope = parser.getCurrentScope(fileContents)

	tmp = project
	for scope in currentScope:
		tmp = tmp.getScope(scope)

	from parsing import CppClass
	if (isinstance(tmp, CppClass)):
		return tmp
	else:
		return None

# test = cppClass(view.file_name(), view.substr(sublime.Region(0, view.size())))
# test.show()



### Generator

class InsertRender():
	"""
		Class used by generator
		This class allow to insert the render of template in right place
		the order of placement is defined into the settings
	"""

	def insertRender(self, typeOfAdding, render):
		from parsing import Parser, Type

		def readFile(path):
			file = open(path, "r")
			lines = file.readlines()
			file.close()
			return lines

		def writeFile(path, contents):
			if contents:
				file = open(path, "w")
				file.write(contents)
				file.close()

		def saveView(views):
			for view in views:
				view.run_command('save')

		def getInterval(classData, contents):

			def findMaxIndex(contents):
				matched = 0
				for i in range(0, len(contents)):
					res = re.search("{", contents[i])
					if res:
						matched += 1
					res = re.search("}\s*;", contents[i])
					if res:
						matched -= 1
						if matched == 0:
							return i
				return len(contents)

			minIndex = 0
			for i in range(0, len(contents)):
				res = re.match("^\s*class\s*(\w+)", contents[i])
				if res and res.group(1) == self.classData.name:
					minIndex = i
					break
			maxIndex = minIndex + findMaxIndex(contents[minIndex:])
			return minIndex, maxIndex


		sourcePath = self.classData.getSourcePath()
		includePath = self.classData.getIncludePath()

		# if getSettings().get("saveBeforeGenerated"):
		# 	viewOfFileUpdated = []
		# 	views = self.window.views()
		# 	for view in views:
		# 		if view.file_name() in [sourcePath, includePath]:
		# 			viewOfFileUpdated.append(view)
		# 	saveView(viewOfFileUpdated);

		# contents = readFile(sourcePath)
		# index = 0
		# linesToAdd = render["source"].split("\n")
		# for i in range(0, len(contents)):
		# 	res = re.match("^(\s*)// (\w+)", contents[i])
		# 	if res:
		# 		comment = res.group(2)
		# 		if (comment == typeOfAdding):
		# 			for j in range(0, len(linesToAdd)):
		# 				linesToAdd[j] = res.group(1)+linesToAdd[j]
		# 			index = i + 1
		# 			break
		# contents.insert(index, "\n".join(linesToAdd)+"\n")
		# writeFile(sourcePath, "".join(contents))

		contents = readFile(includePath)
		minIndex, maxIndex = getInterval(self.classData, contents)

		print("".join(contents[minIndex:maxIndex]))
		index = 0
		linesToAdd = render["include"].split("\n")
		added = False

		for i in range(minIndex, maxIndex):
			res = re.match("^(\s*)// (\w+)", contents[i])
			if res:
				if (res.group(2) == typeOfAdding):
					added = True
					index = i + 1
					lastIndex = index
					space = res.group(1)
					while lastIndex < maxIndex:
						if (re.match("^(\s*)//", contents[lastIndex])):
							break
						lastIndex += 1
					print("index", index, "lastIndex", lastIndex)
					res = re.match("^(\s*)(\w+):", contents[index])
					while res and res.group(2) != "public" and index < lastIndex:
						index += 1
						res = re.match("^(\s*)(\w+):", contents[index])
					for j in range(0, len(linesToAdd)):
						linesToAdd[j] = "\t"+space+linesToAdd[j]
					if res == None:
						linesToAdd.insert(0, space+"public:")
					else:
						index += 1					
					break
		if not added:
			space = ""
			orderOfClass = getSettings().get("orderOfClass")
			for i in range(0, len(orderOfClass)):
				if orderOfClass[i] == typeOfAdding:
					orderOfClass = orderOfClass[i+1:]
					break
			print (orderOfClass)
			for index in range(minIndex, maxIndex):
				res = re.match("^(\s*)// (\w+)", contents[i])
				if res:
					space = res.group(1)
					if res.group(2) in orderOfClass:
						break
			for i in range(0, len(linesToAdd)):
				linesToAdd[i] = space+"\t"+linesToAdd[i]
			linesToAdd.insert(0, space+"// "+typeOfAdding)
			linesToAdd.insert(1, space+"public:")
			linesToAdd.append("")

		contents.insert(index, "\n".join(linesToAdd)+"\n")
		writeFile(includePath, "".join(contents))


class ColiveGenerateGetterCommand(sublime_plugin.WindowCommand, InsertRender):

	def generator(self, itemSelected):
		if (itemSelected >= 0):
			attributes = self.classData.getAllPrivateAttributeName()
			render = renderTemplate("Getter", attributes[itemSelected], self.classData)
			self.insertRender("Getter", render)

	def run(self):
		view = self.window.active_view()

		if getSyntax(view) == "C++.tmLanguage":
			classData = getClass(view)
			if classData:
				self.classData = classData
				attributes = classData.getAllPrivateAttributeName();
				self.window.show_quick_panel(attributes, self.generator)

class ColiveGenerateSetterCommand(sublime_plugin.WindowCommand, InsertRender):

	def generator(self, itemSelected):
		if (itemSelected >= 0):
			attributes = self.classData.getAllPrivateAttributeName()
			render = renderTemplate("Setter", attributes[itemSelected], self.classData)
			self.scope = self.classData
			self.insertRender("Setter", render)

	def run(self):
		window = self.window
		view = window.active_view()

		if getSyntax(view) == "C++.tmLanguage":
			classData = getClass(view)
			if classData:
				self.classData = classData
				attributes = classData.getAllPrivateAttributeName();
				window.show_quick_panel(attributes, self.generator)




### Attribute

class ColiveAddAttributeCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		view = sublime.active_window().active_view()
		syntax = os.path.basename(view.settings().get('syntax'))
		
		if syntax == "C++.tmLanguage":
			test = cppClass(view.file_name(), view.substr(sublime.Region(0, view.size())))
			test.show()

class ColiveRemaneAttributeCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		view = sublime.active_window().active_view()
		syntax = os.path.basename(view.settings().get('syntax'))
		
		if syntax == "C++.tmLanguage":
			test = cppClass(view.file_name(), view.substr(sublime.Region(0, view.size())))
			test.show()

class ColiveRemoveAttributeCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		view = sublime.active_window().active_view()
		syntax = os.path.basename(view.settings().get('syntax'))
		
		if syntax == "C++.tmLanguage":
			test = cppClass(view.file_name(), view.substr(sublime.Region(0, view.size())))
			test.show()


class ColiveEvent(sublime_plugin.EventListener):
	
	def on_pre_save(self, view):
		if False: #view.is_dirty():
			file_name = sublime.active_window().active_view().file_name()

			view.run_command('colive_update_header')

	def on_modified(self, view):
		if False:
			print ("test")
	
			file_extend = os.path.splitext(view.file_name())[1][1:]

			if file_extend == SRC_EXTEND:
				view.run_command("colive_update_include")
			elif file_extend == HEADER_EXTEND:
				view.run_command("colive_update_source")
