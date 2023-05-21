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


#	return filelist_from_rootFolder, keys, waiting
def getALL(input_folder):
	# initialize a dictionary list to store the target files
	filelist_from_rootFolder = []
	keys = []
	waiting = False
	for root, dirs, files in os.walk(input_folder):
		if not dirs:
			_key = root.split('\\')[-1]
			keys.append(_key)
			# print(_key)
			filepaths = [root + '/' + file for file in files]
			target_files_dic = {_key: filepaths}
			# 有效的输入和输出文件夹路径在这里定义
			print(root)
			print(files)
			filelist_from_rootFolder.append(target_files_dic)

	return filelist_from_rootFolder, keys, waiting


def isValid(input_folder, pattern_index) -> bool:
	# 1. 检查Pixyz是否安装
	# 2. check file/dir path is valid
	# support extensions right now.
	# valid_extensions: filter list

	valid_extensions = [".rvt", ".rfa"]

	# get all files to import
	fs, ks, bw = getALL(input_folder)
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
		rvt_id = str(system_date).replace('/', ' ').replace('\n', '')
		rvt_name = re_match_obj.group(1)
		rvt_code = re_match_obj.group(2)
	else:
		print('Please input your parameters')

	return rvt_id, rvt_name, rvt_code

# #
# if __name__ == '__main__':
# 	input_folder = 'F:\PCG\pixyz\RVT_Scenario\_input'
# 	fl, k, w = getALL(input_folder)
# 	input_folder = pl.Path(input_folder)
# 	isValid = isValid(input_folder, 1)
# 	print(isValid)
# 	for f in fl:
# 		for _k in k:
# 			if f.get(_k):
# 				print(_k, f.get(_k))
# 				models_to_import = f.get(_k)
# 				for _model in models_to_import:
# 					rvt_id, rvt_name, rvt_code = getInfoFromFile(_model, 1)
# 					print(rvt_id, rvt_name, rvt_code)
