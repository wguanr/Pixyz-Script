import sys
import json
import os
import subprocess
from rename_chinese_advanced import main as rn
import pathlib as plb


def main(config_file):
	# Read config file
	with open(config_file) as config:
		inputs = json.load(config)
	input_folder = inputs['input_folder']
	input_folder = os.path.abspath(input_folder)
	extensions = inputs['extensions']
	current_pattern_index = inputs['current_pattern_index']
	# rename chinese
	rn(input_folder)
	print('\n')
	print('Input folder: ' + str(input_folder))
	print('Output extensions: ' + str(extensions))
	print('Current pattern index: ' + str(current_pattern_index))
	print('\n')

	args = [r'C:\Program Files\PiXYZScenarioProcessor\PiXYZScenarioProcessor.exe',
	        'ScriptLibrary',
	        'Revit_Process',
	        f'"{input_folder}"',
	        str(extensions),
	        str(current_pattern_index)]

	# there has to ignite  encoding='utf-8' to avoid error
	p = subprocess.Popen(
		args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')

	# read output line by line
	for line in p.stdout:
		print(line.strip())
	sys.stdout.flush()

	print('\n')
	print('Done: Revit_Process executed')
	print('\n')


#
# #to remove all in input folder
# for root, dirs, files in os.walk(input_folder):
# 	for file in files:
# 		os.remove(os.path.join(root, file))
# 	for dir in dirs:
# 		os.rmdir(os.path.join(root, dir))
# print('Reset: Input folder cleared')


def read_config(config_file):
	"""
	Read config file and return the arguments
	:param config_file: user defined config file
	:return: input_folder, output_folder, extensions, export_name
	"""
	with open(config_file) as config:
		inputs = json.load(config)

	# Get arguments from config json file
	input_folder = inputs['input_folder']
	# convert relative path to absolute path (if needed)
	input_folder = os.path.abspath(input_folder)

	# output_folder = inputs['output_folder']
	# if output_folder == '':
	# 	output_folder = input_folder.replace("input", "output")
	# output_folder = os.path.abspath(output_folder)

	extensions = inputs['extensions']

	# export_name = inputs['output_custom_name']
	current_pattern_index = inputs['current_pattern_index']
	# print('\n')
	# print('Input folder: %s\n' % input_folder)
	# # print('Output folder: %s\n' % output_folder)
	# print('Extensions: %s\n' % ' '.join(extensions))
	# print('Output_custom_name: %s\n' % export_name)
	# print('Current_pattern_index: %s\n' % current_pattern_index)
	# print('\n')

	return input_folder, extensions, current_pattern_index


if __name__ == "__main__":
	main(sys.argv[1])
