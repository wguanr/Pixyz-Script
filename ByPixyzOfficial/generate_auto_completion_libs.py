import json
import os
import shutil
from os import listdir, path

def createDirectory(folder):
    """If a folder does not exists, creates it. Returns the folder path."""
    if not os.path.isdir(folder):
        os.makedirs(folder)
    return folder

def listFilesInFolder(folder):
	files = [folder + f for f in listdir(folder) if path.isfile(path.join(folder, f)) and f[-4:] == 'html']
	return files

def cleanParameters(parameters):
	new_parameters = ''
	get = True
	for c in parameters:
		if c == '<':
			get = False
		elif get:
			new_parameters += c
		elif c == '>':
			get = True
	return new_parameters

def parseHtml(htmlFile):
	with open(htmlFile) as html:
		for line in html:
			if "class=\'function_name\'>" in line:
				line = line.split("class=\'function_name\'>", 1)[1]
				name = line.split("</b>", 1)[0]
				parameters = line.split("</b>", 1)[1]
				parameters = parameters.split("<h4>", 1)[0]
				parameters = cleanParameters(parameters)
				parameters = parameters.split("->", 1)[0]
				if name != '' and parameters != '':
					return name, parameters
	return None, None



def createFunctionsDict(htmlFiles):
	functions = list()
	for html in htmlFiles:
		name, parameters = parseHtml(html)
		if name is not None:
			functions.append({'name':name, 'parameters':parameters})
	return functions



def generateSublimeJSON(functions, folder, file):
	createDirectory(folder)
	sublime_completions = dict()
	sublime_completions['scope'] = 'source.python'
	sublime_functions = [{'trigger':function['name'], 'contents':function['name']+function['parameters']}\
							 for function in functions]
	sublime_completions['completions'] = sublime_functions
	with open(folder + file, 'w+') as out:
		json.dump(sublime_completions, out)



def generateVisualCodeJSON(functions, folder, file):
	createDirectory(folder)
	vs_snippets = dict()
	for function in functions:
		name = function['name']
		parameters = function['parameters']
		vs_snippets[name] = {'prefix':name, 'body':name+parameters, 'description':''}
	with open(folder + file, 'w+') as out:
		json.dump(vs_snippets, out)



def generatePyCharmTemplate(functions, folder):
	try:
		os.makedirs(folder + '/templates/')
	except:
		pass
	with open(folder + '/templates/Python.xml', 'w') as xml:
		writeLineXML(xml, 'templateSet', 0, {'group':'Python'})
		for dic in functions:
			writeLineXML(xml, 'template', 1, {'name':dic['name'], 'value':dic['name']+dic['parameters'], 'description':'', 'toReformat':'false', 'toShortenFQNames':'true'}, True)
		writeLineXML(xml, '/templateSet')
	with open(folder + '/templates/pixyz.xml', 'w+') as xml:
		writeLineXML(xml, 'templateSet', 0, {'group':'pixyz'})
		for dic in functions:
			writeLineXML(xml, 'template', 1, {'name':dic['name'], 'value':dic['name']+dic['parameters'], 'description':'', 'toReformat':'false', 'toShortenFQNames':'true'}, False)
			writeLineXML(xml, 'context', 2)
			writeLineXML(xml, 'option', 3, {'name':'Python', 'value':'true'}, True)
			writeLineXML(xml, '/context', 2)
			writeLineXML(xml, '/template')
		writeLineXML(xml, '/templateSet')
	open(folder + '/IntelliJ IDEA Global Settings', 'w')
	shutil.make_archive(folder, 'zip', folder)
	shutil.rmtree(folder)

def writeLineXML(file, type, indent=0, parameters={}, close=False):
	"""Writes a line of xml into file: <type key_1:"value_1" key_2:"value2">"""
	line = ('  ' * indent) + '<' + type
	nParameters = len(parameters)
	for parameter, value in parameters.items():
		line = line + ' ' + str(parameter) + '=\"' + str(value) + '\"'
	if close:
		line = line + '/>\n'
	else: 
		line = line + '>\n'
	file.write(str(line))

def generate(doc_folder):
	htmlFiles = listFilesInFolder(doc_folder)
	functions = createFunctionsDict(htmlFiles)
	generateSublimeJSON(functions, os.getenv('APPDATA')+ '/PiXYZStudio/PiXYZ-SublimeText3/', 'pixyz.sublime-completions')
	generateVisualCodeJSON(functions, os.getenv('APPDATA') + '/PiXYZStudio/PiXYZ-VisualCode/', 'python.json')
	generatePyCharmTemplate(functions, os.getenv('APPDATA') + '/PiXYZStudio/PiXYZ-PyCharm-AutoCompletion')
	print('Files generated at: ' + str(os.getenv('APPDATA')) + '\\PiXYZStudio\\')

pxz_doc_folder = os.getenv('APPDATA') + '/PiXYZStudio/doc/'
generate(pxz_doc_folder)
