import sys
import json
import os
import subprocess
from ctypes import windll
from rename_chinese_advanced import main as rn


def main(config_file):
	# 暂时不输出output_foloder
	input_folder, extensions, export_name = read_config(
		config_file)

	waiting = False
	for root, dirs, files in os.walk(input_folder):
		if dirs:
			rn(dirs)
	print('Renaming finished')

	while (1):
		i = 1
		for root, dirs, files in os.walk(input_folder):
			if not dirs:
				# 有效的输入和输出文件夹路径在这里定义
				target_folder = root
				output_folder = target_folder.replace("input", "output")
				if not os.path.exists(output_folder):
					os.mkdir(output_folder)
					print('Output folder created: %s' % output_folder)
				files_in_root = [f for f in os.listdir(target_folder) if os.path.isfile(
					os.path.join(target_folder, f))]

				if len(files_in_root) == 0:
					if not waiting:
						print('\n')
						print("Press enter to continue...")
						waiting = True
					continue
				elif not isCopyFinished(target_folder + '/' + files_in_root[0]):
					continue
				else:
					waiting = False
				################################
				if waiting == False:
					execute_Revit_Process(
						target_folder, output_folder, export_name=export_name, extensions=str(extensions))
					i += 1
				################################

				print('Done')


def execute_Revit_Process(input_folder, output_folder, export_name, extensions):
	args = ['C:\Program Files\PiXYZScenarioProcessor\PiXYZScenarioProcessor.exe', 'ScriptLibrary', 'Revit_Process',
	        "\"" + input_folder + "\"", "\"" + output_folder + "\"", "\"" + export_name + "\"", str(extensions)]
	# .replace("\\", "\\\\")
	p = subprocess.Popen(
		args, shell=True, stdout=subprocess.PIPE,
		stderr=subprocess.STDOUT, universal_newlines=True, encoding='utf-8')

	# Iterate over the output of the subprocess and print each line
	for line in p.stdout:
		print(line.strip())


def read_config(config_file):
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

	export_name = inputs['output_custom_name']

	print('\n')
	print('Input folder: %s\n' % input_folder)
	# print('Output folder: %s\n' % output_folder)
	print('Extensions: %s\n' % ' '.join(extensions))
	print('Output_custom_name: %s\n' % export_name)
	print('\n')

	return input_folder, extensions, export_name


def isCopyFinished(inputFile):
	"""
	Check if the file that was dropped in the input folder has finished being copied
	"""
	GENERIC_WRITE = 1 << 30
	FILE_SHARE_READ = 0x00000001
	OPEN_EXISTING = 3
	FILE_ATTRIBUTE_NORMAL = 0x80
	handle = windll.Kernel32.CreateFileW(
		inputFile, GENERIC_WRITE, FILE_SHARE_READ, None, OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL, None)
	if handle != -1:
		windll.Kernel32.CloseHandle(handle)
		return True
	return False


if __name__ == "__main__":
	main(sys.argv[1])
