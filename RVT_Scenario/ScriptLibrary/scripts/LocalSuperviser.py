import re
from ctypes import windll
import os
import random
import pathlib as pl

# file name would be all with '_' and no space
pattern_hasID = r"^(\d+)_([^_]+?)_([A-Z]+)"
pattern_noID = r"([^_]+?)_([A-Z]+)"
pattern_pureName = r"^([^_]+?)"
# review: to use lambda map to optimize
pattern_0 = {
	0: pattern_hasID,
	1: pattern_noID,
	2: pattern_pureName
	}


# e.g. 40012334_建筑_A_F01


#	return filelist_from_rootFolder, keys, waiting
def getALL(input_folder):
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


# 	return RVTid, RVTname, RVTcode, extension
def getInfoFromFile(file_path, pattern_index):
	"""
	Get info from the file
	:param file_path: the file path to get the info
	:param pattern_index: the pattern index to get the info
	:return: RVTid, RVTname, RVTcode, extension
	"""
	global rvt_id, rvt_name, rvt_code
	FileName = os.path.splitext(os.path.basename(file_path))[0]
	# extension = os.path.splitext(os.path.basename(file_path))[1]
	re_match_obj = re.search(pattern_0.get(pattern_index), FileName)
	#
	if pattern_index == 0:
		rvt_id = re_match_obj.group(1)
		rvt_name = re_match_obj.group(2)
		rvt_code = re_match_obj.group(3)
	elif pattern_index == 1:
		# set id to current system date
		system_date = os.popen('date /t').read()
		rvt_id = str(system_date).replace('/', '_').replace('\n', '')
		# delete last 2 chars
		rvt_id = rvt_id[:-4]
		rvt_name = re_match_obj.group(1)
		rvt_code = re_match_obj.group(2)
	else:
		print('Please input your parameters')

	return rvt_id, rvt_name, rvt_code



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

#
# # # #
# if __name__ == '__main__':
# 	input_folder = r'F:\PCG\pixyz\RVT_Scenario\_input'
# 	fl, k = getALL(input_folder)
# 	input_folder = pl.Path(input_folder)
# 	isValid = isValid(input_folder, 1)
# 	output_folder = pl.Path(r'F:\PCG\pixyz\RVT_Scenario\_output')
# 	print(isValid)
# 	print(k)
# 	for f in fl:
# 		for _k in k:
# 			if f.get(_k):
# 				print(_k, f.get(_k))
# 				models_to_import = f.get(_k)
# 				rvt_id, rvt_name, rvt_code = getInfoFromFile(models_to_import[0], 1)
# 				# print(rvt_id, rvt_name, rvt_code)
# 				_output_folder = output_folder / str(rvt_id) /str(_k)/str(rvt_code)
# 				_output_folder.mkdir(parents=True, exist_ok=True)
# 				_export_name = f'ID_{rvt_id}_{rvt_code}'
# 				print('current output folder is:' + str(_output_folder))
# 				print('current export basename is:' + _export_name)
# 				for _model in models_to_import:
# 					pass
