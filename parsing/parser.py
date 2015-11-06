#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# factory.py
# Project : unknown
# Contact : info@devolive.be
# Created by olive007 at 30/10/2015 12:05:00
# Last update by olive007 at 06/11/2015 12:59:41

import re
import os
### Testing
import time

from parsing import *

class Parser:
	"""
		Parser C++
	"""
	__shared_state = {}

	def __init__(self):
		self.__dict__ = self.__shared_state
		self._project = {}
		print("Parser C++ created");

	def getProject(self, id):
		if (id in self._project):
			return self._project[id]
		return None

	def parse(self, filePath):
		location, projectFolder = getLocation(filePath)
		typeFile = getType(filePath)

		id = projectFolder
		if (id not in self._project):
			self._project[id] = Project(id)

		file = open(filePath, 'r')
		fileContents = file.read()
		file.close()
		fileContents = removeComments(fileContents)
		fileContents = removePreprocessing(fileContents)
		""
		def parsing(scope, fileContents, visibility = None):
			
			def doNamespace():
				nonlocal fileContents
				res = re.search("\w+", fileContents)
				if res:
					fileContents = fileContents[res.end(0):]
					namespace = Namespace(res.group(0))
					body, cursor = getBracketBody(fileContents, "{}")
					fileContents = fileContents[cursor:]
					parsing(namespace, body)
					return namespace
				raise ParserException("wrong syntax namespace")

			def doClass():
				nonlocal fileContents
				res = re.search("\w+", fileContents)
				if res:
					fileContents = fileContents[res.end(0):]
					cppClass = CppClass(res.group(0))
					body, cursor = getBracketBody(fileContents, "{}")
					fileContents = fileContents[cursor:]
					parsing(cppClass, body, Visibility.private)
					return cppClass
				raise ParserException("wrong syntax class")

			def doStruct():
				nonlocal fileContents
				res = re.search("\w+", fileContents)
				if res:
					fileContents = fileContents[res.end(0):]
					struct = Struct(res.group(0))
					body, cursor = getBracketBody(fileContents, "{}")
					fileContents = fileContents[cursor:]
					parsing(struct, body, Visibility.public)
					return struct
				raise ParserException("wrong syntax class")

			def doInstruction(word):
				"""

				"""
				nonlocal fileContents
				res = re.search(";", fileContents)
				if (res):
					instruction = word + fileContents[:res.end(0)]
					fileContents = fileContents[res.end(0):]
					bracketBody, cursor = getBracketBody(instruction)
					#print(instruction)
					if bracketBody is not None:
						res = re.search("([~\w]+)\s*\(", instruction)
						method = Method(res.group(1))
						afterBracket = instruction[cursor:]
						if (re.search("const\s*", afterBracket)):
							method.setConst(True)
						type = instruction[:res.start(0)]
						res = re.search("virtual\s+", type)
						if (res):
							type = type.replace("virtual", "")
							method.setVirtual(True)
						if type != "":
							method.setReturnType(type)
						arguments = bracketBody.split(',')
						for argument in arguments:
							#res = re.search("(\w+[\w\s\*&]*)((\s+(\w+))\s*=\s*([\"\w']+))?$", argument)
							name = value = None
							res = re.search("(\w+)\s*=\s*([-\w\"']+)\s*$", argument)
							if (res):
								name = res.group(1)
								value = res.group(2)
								argument = argument[:res.start(0)]
								res = re.search("([\w\s\*&]+)", argument)
								if (res):
									method.addArgument(res.group(1), name, value)
							else:
								res = re.search("\w+$", argument)
								if (res):
									name = res.group(0)
									type = argument[:res.start(0)]
									tmp = type
									res = re.search("const", tmp)
									if (res):
										tmp = re.sub("const", "", tmp)
									res = re.search("&", tmp)
									if (res):
										tmp = re.sub("&", "", tmp)
									res = re.search("\*", tmp)
									if (res):
										tmp = re.sub("\*", "", tmp)
									if (re.match("^\s*$", tmp)):
										type = "%s %s" % (type, name)
										name = None
									method.addArgument(type, name)
								else:
									method.addArgument(argument)

						return method
					else:
						res = re.search("(\w+)(\s*\=\s*([\"a-zA-Z0-9']+))?\s*;", instruction)
						if (res):
							name = res.group(1)
							type = instruction[:res.start(0)]
							isStatic = re.search("(const\s+)?static\s+", type)
							if (isStatic):
								type = type.replace("static", "", 1)
								variable = Variable(type, name, True)
							else:
								variable = Variable(type, name)
							if (res.group(3)):
								variable.setValue(res.group(3))
							return variable
					return None
				raise ParserException("wrong syntax instruction")


			i = 0
			while (True):
				res = re.search("\w+", fileContents)
				if (res == None):
					break
				#print(i)
				#print(fileContents)
				fileContents = fileContents[res.end(0):]
				word = res.group(0)
				if word == "namespace":
					scope.addNamespace(doNamespace())
				elif word == "class":
					scope.addClass(doClass())
				elif word == "struct":
					scope.addClass(doStruct())
				elif word == "public" or word == "protected" or word == "private":
					tmp = re.search("^:", fileContents)
					if tmp:
						fileContents = fileContents[tmp.end(0):]
					visibility = Visibility.parse(word)
				elif word == "using":
					tmp = re.search(";", fileContents)
					if tmp:
						fileContents = fileContents[tmp.end(0):]
				else:
					scope.addInstruction(doInstruction(word), visibility)
				
				#time.sleep(1)
				i += 1
			
		parsing(self._project[id], fileContents)
		self._project[id].show()
		return self._project[id]




def getType(fileName):
	fileExtend = os.path.splitext(fileName)[1][1:]

	if (fileExtend == INCLUDE_EXTEND):
		return Type.include
	elif (fileExtend == SOURCE_EXTEND):
		return Type.source
	return None

def getLocation(filePath):
	path, fileName = os.path.split(filePath)

	namespace = []
	while 1:
		path, folder = os.path.split(path)
		if folder == "src" or folder == "include":
			break
		elif folder != "":
			namespace.append(folder)
		else:
			break
	namespace.reverse()
	projectFolder = path

	return namespace, projectFolder

def getInstruction(data):
	res = re.search(";", data)
	if (res):
		return data[res.start(0):]
	res = re.search("{", data)
	if (res):
		return data[res.start(0):]
	return data

def getBracketBody(fileContents, bracket="()"):
	tmp = bracket[0]
	if (tmp == "("):
		tmp = "\("
	elif (tmp == "["):
		tmp = "\["
	openBracket = list(re.finditer(tmp, fileContents))
	tmp = bracket[1]
	if (tmp == ")"):
		tmp = "\)"
	elif (tmp == "]"):
		tmp = "\]"
	closeBracket = list(re.finditer(tmp, fileContents))

	if (len(openBracket) == 0 or len(closeBracket) == 0 or len(openBracket) != len(closeBracket)):
		return None, 0
	begin = openBracket[0].end(0)
	last = closeBracket[-1].start(0)
	i = 0
	for i in range(0, len(openBracket) - 1):
		if (openBracket[i + 1].end(0) > closeBracket[i].end(0)):
			last = closeBracket[i].start(0)
			break

	return fileContents[begin:last], last

def removePreprocessing(fileContents):
	"""
		Remove preprocessing operation:
		- ifndef
		- define
		- endif
	"""
	res = re.search("#", fileContents)
	while (res):
		begin = res.start(0)
		tmp = fileContents[begin:]
		lineIgnored = 1
		lines = tmp.split('\n')
		i = 0
		while (re.search("\\\\(\s)*$", lines[i])):
			lineIgnored += 1
			i += 1
		lines = lines[lineIgnored:]
		tmp = '\n'.join(lines)
		fileContents = fileContents[:begin] + tmp
		res = re.search("#", fileContents)

	return fileContents

def removeComments(fileContents):
	"""
		Remove cpp comment:
		- //
		- /*
	"""
	res = re.search("//", fileContents)
	while (res):
		begin = res.start(0)
		tmp = fileContents[begin:]
		lines = tmp.split('\n')[1:]
		tmp = '\n'.join(lines)
		fileContents = fileContents[:begin] + tmp
		res = re.search("//", fileContents)

	res = re.search("/\*", fileContents)
	while (res):
		begin = res.start(0)
		last = len(fileContents)
		res = re.search("\*/", fileContents)
		if (res):
			last = res.end(0)
		tmp = fileContents[:begin]+fileContents[last:]
		fileContents = tmp
		res = re.search("/\*", fileContents)

	return fileContents