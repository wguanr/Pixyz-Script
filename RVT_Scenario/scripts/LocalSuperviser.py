import re
from ctypes import windll
import os
import random
import pathlib as pl


# e.g. 40012334_建筑_A_F01
def init_parameters(StandardMode:bool, input, extensions, project_name=None, rvt_code_dict=None):
	# input= r'F:\PCG\pixyz\RVT_Scenario\_input\2023nianzuixin0302dikuairevitmoxing\muqiangmoxing'
	# output = 'F:\PCG\pixyz\RVT_Scenario\_output'

	if rvt_code_dict is None:
		rvt_code_dict = {}
	if not os.path.exists(input):
		print('Revit_Process input is not a valid path')
		return

	if extensions == '':
		ini_extensions = ['.fbx']
	else:
		ini_extensions = extensions

	ini_input_folder = pl.Path(input)
	ini_output_folder = pl.Path(input).parent / '_output'
	ini_output_folder.mkdir(parents=True, exist_ok=True)

	if StandardMode == True:
		return ini_input_folder, ini_output_folder, ini_extensions
	else:
		# get  ini_rvt_id, rvt_code_list
		rvt_code_list = []
		for key in rvt_code_dict:
			rvt_code_list.append(rvt_code_dict[key])

		system_date = os.popen('date /t').read()
		_suffix = str(system_date).replace('/', '').replace('\n', '')
		ini_rvt_id = f'{project_name}_{_suffix[:-4]}'

		return ini_input_folder, ini_output_folder, ini_extensions, ini_rvt_id, rvt_code_list


#	return filelist_from_rootFolder, keys, waiting
def getALL(GetMode, input_folder, rvt_code_dict=None):
	'''
	:param GetMode: True: return pure file hierarchy in the input_folder
					False: return hierarchy by json RVT code in the input_folder
	'''
	if GetMode:
		# initialize a dictionary list to store the target files
		filelist_from_rootFolder = []
		keys = []
		for root, dirs, files in os.walk(input_folder):
			if not dirs:
				root = pl.Path(root)
				_key = root.relative_to(input_folder)
				_key = str(_key)
				keys.append(_key)
				filepaths = [root / file for file in files]
				target_files_dic = {_key: filepaths}
				# 有效的输入和输出文件夹路径在这里定义
				filelist_from_rootFolder.append(target_files_dic)
		return filelist_from_rootFolder, keys
	else:
		if rvt_code_dict is None:
			print('rvt_code_dict Need to be set')
			return
		# get all files by rvt_code_dict
		filelist_from_rootFolder = []
		keys = []
		filepaths = []
		for root, dirs, files in os.walk(input_folder):
			if not dirs:
				root = pl.Path(root)
				for file in files:
					filepath = root / file
					if filepath.suffix in ['.rvt', '.rfa']:
						filepaths.append(filepath)

		for key in rvt_code_dict:
			keys.append(key)
			target_files_dic = {key: []}
			for file in filepaths:
				check_code = '_' + rvt_code_dict.get(key)
				if check_code in file.name:
					target_files_dic[key].append(file)
			filelist_from_rootFolder.append(target_files_dic)
		return filelist_from_rootFolder, keys


# cd = {
# 	"建筑": "AR",
# 	"结构": "ST",
# 	"幕墙": "A",
# 	"机电": "MEP"
# 	}
# f, k =getALL(True,r'E:\CIM_RVT\4403050020063700015_前海法治大厦')
# for ks in k:
# 	for i in range(len(f)):
# 		if f[i].get(ks):
# 			print(ks)
# 			print(f[i].get(ks))


# deprecated
def isValid(input_folder, pattern_index) -> bool:
	# 1. 检查Pixyz是否安装
	# 2. check file/dir path is valid
	# support extensions right now.
	# valid_extensions: filter list

	valid_extensions = [".rvt", ".rfa"]

	# get all files to import
	fs, ks = getALL(input_folder)
	for f in fs:
		for mdoel_group in ks:
			target_models_to_import = []
			if f.get(mdoel_group):
				target_models_to_import = f.get(mdoel_group)
				# check, if not in support extensions, delete the item
				for _model in target_models_to_import:
					if os.path.splitext(_model)[1] not in valid_extensions:
						target_models_to_import.remove(_model)

			# print(target_models_to_import)
			######################
			#  checking name
			######################
			# random checking for 25% files
			i = int(len(target_models_to_import) / 4)

			while i > 0:
				i -= 1
				random_num = random.randint(0, len(target_models_to_import) - 1)
				FileName = os.path.splitext(os.path.basename(target_models_to_import[random_num]))[0]
				match = re.search(pattern_0.get(pattern_index), FileName)

				if not bool(match):
					print("Error file is : " + FileName + " , please check the file name.")
					return False

	return True

def getInfoFromFile(file_path):
	"""
	just for standard mode
	:param file_path: the file path to get the info
	:return: rvt_id, rvt_name, rvt_code
	"""
	FileName = os.path.splitext(os.path.basename(file_path))[0]
	# extension = os.path.splitext(os.path.basename(file_path))[1]
	# get the rex to match file names as : 36727186_filename23_AR.rvt
	_rex = r'^(\d+)_([^_]+?)_([A-Z]+)_([^_]+)'
	re_match_obj = re.search(_rex, FileName)
	if re_match_obj:
		rvt_id = re_match_obj.group(1)
		rvt_project_name = re_match_obj.group(2)
		rvt_code = re_match_obj.group(3)
		rvt_model_name = re_match_obj.group(4)
		return rvt_id, rvt_project_name, rvt_code, rvt_model_name
	else:
		print("Error file is : " + FileName + " , please check the file name.")
		return

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
