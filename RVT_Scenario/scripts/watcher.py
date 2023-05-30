import sys
import json
import os
import subprocess
import pathlib as plb
import LocalSuperviser as ls
import argparse as ap

def main(config_file):
	# Read config file
	StandardMode, rvt_code_dict, input_folder, extensions, current_pattern_index, project_name = read_config(
		config_file)
	print('StandardMode: ' + str(StandardMode) + '\n' + 'rvt_code_dict: ' + str(rvt_code_dict) + '\n' + 'input_folder: ' + str(
		input_folder) + '\n' + 'extensions: ' + str(extensions) + '\n' + 'current_pattern_index: ' + str(
		current_pattern_index) + '\n' + 'project_name: ' + str(project_name))

	if StandardMode:
		input_folder = r'E:\CIM_RVT\4403050020063700015_前海法治大厦'
		_input_folder, output_folder, extensions = ls.init_parameters(StandardMode, input_folder, extensions)
		files_to_import, keys_of_files = ls.getALL(False, _input_folder, rvt_code_dict)
		args = []
		for files in files_to_import:
			for _k in keys_of_files:
				import_list = []
				if files.get(_k):
					# get all files and file info
					models_to_import = files.get(_k)
					for _model in models_to_import:
						import_list.append(str(_model))

					print('_k: ' + str(_k))
					# print('import_list: ' + str(import_list))
					print('length is: ' + str(len(import_list)))
					RVT_id, project_name, RVT_code, model_name = ls.getInfoFromFile(models_to_import[0])
					_output_folder = output_folder / f'{RVT_id}_{project_name}' / str(_k)
					_output_folder.mkdir(parents=True, exist_ok=True)
					print('_output_folder: ' + str(_output_folder))
					export_name = f'{project_name}_{model_name}_{RVT_code}'
					print('export_name: ' + str(export_name))
					# def RevitStandardProcess(files_to_import,output_folder,export_name,extensions,key_of_files):
					# _args = [r'C:\Program Files\PiXYZScenarioProcessor\PiXYZScenarioProcessor.exe',
					#         'ScriptLibrary',
					#         'RevitGeneralProcess',
					#         f'"{import_list}"'.replace('\\\\', '\\'),
					#         f'"{_output_folder}"',
					#         f'"{export_name}"',
					#         str(extensions),
					#         str(_k)]
					# args.append(_args)
		# print(args)

	else:
		_input_folder, output_folder, extensions, rvt_id, rvt_code_list = ls.init_parameters(
			StandardMode, input_folder, extensions, project_name, rvt_code_dict)

		files_to_import, keys_of_files = ls.getALL(False, _input_folder, rvt_code_dict)

		args = []
		i = 0
		for files in files_to_import:
			for _k in keys_of_files:
				import_list = []

				if files.get(_k):
					# get all files and file info
					models_to_import = files.get(_k)
					for _model in models_to_import:
						import_list.append(_model.as_posix())

					print('_k: ' + str(_k))
					# print('import_list: ' + str(import_list))
					print('length is: ' + str(len(import_list)))
					print(import_list)
					RVT_id, project_name, RVT_code = rvt_id, project_name, rvt_code_list[i]
					_output_folder = output_folder / f'{rvt_id}' / str(_k)
					_output_folder.mkdir(parents=True, exist_ok=True)
					print('_output_folder: ' + str(_output_folder))
					export_name = f'{project_name}_{RVT_code}'
					print('export_name: ' + str(export_name))
					i = i + 1

					# "\"" + input_file.replace("\\", "\\\\") + "\"", "\"" + output_folder.replace("\\", "\\\\") + "\"" .as_posix()
					excute_subprocess(import_list, _output_folder.as_posix(), export_name, extensions, _k)

	print('\n')
	print('Done: Revit_Process executed')
	print('\n')
	# clean_input_Directory(input_folder)


def excute_subprocess(import_list, output_folder, export_name, extensions, _k):
	'''
	PiXYZScenarioProcessor ScriptLibrary RevitGeneralProcess "[\"F:/PCG/pixyz/RVT_Scenario/_input/test/sadwd_AR.rvt\"]" "\"F:/PCG/pixyz/RVT_Scenario/_output\"" "\"ssss\"" "[\".fbx\"]" "\"jianzhu\""
					#
					# scriptlibrary.RevitGeneralProcess(
					# 	["F:/PCG/pixyz/RVT_Scenario/_input/2023年最新0302地块revit模型/建筑模型/塔楼/塔楼T1_AR.rvt"],
					# 	"F:/PCG/pixyz/RVT_Scenario/_output", "test", [".fbx"], "jianzhu")
					#
	description = "you should add those parameter"
	parser = ap.ArgumentParser(description=description)
	help = "Default"
	parser.add_argument('--imp', type=str, nargs='+', default=str(import_list), help=help)
	parser.add_argument('--out_f', type=str, nargs='+', default=output_folder, help=help)
	parser.add_argument('--out_n', type=str, nargs='+', default=export_name, help=help)
	parser.add_argument('--ext', type=str, nargs='+', default=str(extensions), help=help)
	parser.add_argument('--k', type=str, nargs='+', default=_k, help=help)

	root_args = parser.parse_args()
	print(root_args)

	arg = [r'PiXYZScenarioProcessor',
	         'ScriptLibrary',
	         'RevitGeneralProcess',
	         root_args.imp,
	         root_args.out_f,
	         root_args.out_n,
	         root_args.ext,
	         root_args.k]
	print(arg)
		arg = [r'PiXYZScenarioProcessor',
	       'ScriptLibrary',
	       'RevitGeneralProcess',
	       "\"" + str(import_list) +"\"",
	       "\"" + (output_folder) +"\"",
	      "\""+(export_name)+"\"",
	       "\""+str(extensions)+"\"",
	      "\""+_k+"\""]
	'''
	arg = [r'PiXYZScenarioProcessor',
	       'ScriptLibrary',
	       'RevitGeneralProcess',
	       str(import_list),
	       "\"" + (output_folder) + "\"",
	       "\"" + (export_name) + "\"",
	       str(extensions),
	      "\""+_k+"\""]
	# encoding='utf-8' to get the same with Pixyz Scenario Processor encoding setting
	# but sometimes it will cause error, so to delete the encoding setting
	p = subprocess.Popen(
		arg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
		)
	# read output line by line
	for line in p.stdout:
		print(line, end='')
	# wait 5 seconds for the subprocess to exit
	p.wait(5)
	p.kill()



	


def clean_input_Directory(input_folder):
	#to remove all in input folder
	for root, dirs, files in os.walk(input_folder):
		for file in files:
			os.remove(os.path.join(root, file))
		for dir in dirs:
			os.rmdir(os.path.join(root, dir))
	print('Reset: Input folder cleared')


def read_config(config_file):
	"""
	Read config file and return the arguments
	:param config_file: user defined config file
	:return: input_folder, output_folder, extensions, export_name
	"""
	# Read config file with utf-8 encoding
	with open(config_file, encoding='utf-8') as config:
		inputs = json.load(config)

	# Basic

	StandardMode = inputs['StandardMode']
	input_folder = inputs['input_folder']
	input_folder = os.path.abspath(input_folder)
	extensions = inputs['extensions']
	# print(type(StandardMode))

	# Standard

	# customize
	current_pattern_index = inputs['current_pattern_index']
	project_name = inputs['project_name']
	rvt_code_dict = inputs['rvt_code_dict']
	if StandardMode:
		# type : ANSI Shadow
		print(
			r'''	

		███████╗████████╗ █████╗ ███╗   ██╗██████╗  █████╗ ██████╗ ██████╗     ███╗   ███╗ ██████╗ ██████╗ ███████╗
		██╔════╝╚══██╔══╝██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
		███████╗   ██║   ███████║██╔██╗ ██║██║  ██║███████║██████╔╝██║  ██║    ██╔████╔██║██║   ██║██║  ██║█████╗  
		╚════██║   ██║   ██╔══██║██║╚██╗██║██║  ██║██╔══██║██╔══██╗██║  ██║    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  
		███████║   ██║   ██║  ██║██║ ╚████║██████╔╝██║  ██║██║  ██║██████╔╝    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗
		╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝     ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

		''')
		rvt_code_dict = {
			"建筑": "A",
			"钢结构": "SS",
			"结构": "S",
			"给排水": "P",
			"电气": "E",
			"暖通空调": "M",
			"智能化": "T",
			"市政": "CE",
			"景观": "L",
			"BIM": "BIM"
			}
		extensions = [".fbx"]
		current_pattern_index = 0
		project_name = "rvt_id"
		return StandardMode, rvt_code_dict, input_folder, extensions, current_pattern_index, project_name
	else:
		print(
			r'''

		 ██████╗██╗   ██╗███████╗████████╗ ██████╗ ███╗   ███╗    ███╗   ███╗ ██████╗ ██████╗ ███████╗
		██╔════╝██║   ██║██╔════╝╚══██╔══╝██╔═══██╗████╗ ████║    ████╗ ████║██╔═══██╗██╔══██╗██╔════╝
		██║     ██║   ██║███████╗   ██║   ██║   ██║██╔████╔██║    ██╔████╔██║██║   ██║██║  ██║█████╗  
		██║     ██║   ██║╚════██║   ██║   ██║   ██║██║╚██╔╝██║    ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  
		╚██████╗╚██████╔╝███████║   ██║   ╚██████╔╝██║ ╚═╝ ██║    ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗
		 ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝    ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

		''')
		return StandardMode, rvt_code_dict, input_folder, extensions, current_pattern_index, project_name


if __name__ == "__main__":
	# pa = ap.ArgumentParser()
	# # set the config file path
	#
	# pa.add_argument('-c', '--config', default='../config.json', help='config file path')
	# p = pa.parse_args()
	#
	# main(p.config)

	# read_config('config.json')
	main(sys.argv[1])
