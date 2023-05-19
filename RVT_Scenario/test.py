import pathlib as pl
import os


input_folder = 'F:\PCG\pixyz\RVT_Scenario\_input'
input_folder2 = r'E:\CIM_RVT\4403050020063700015_前海法治大厦'

input = pl.Path(input_folder2)

# get directories as tree from the input_folder
def getALL(input_folder):
	"""
	Get all the files from the input_folder
	:param input_folder: the input folder
	:return: files_list, keys_list, warnings_list
	"""
	files_list = []
	keys_list = []
	warnings_list = []
	# get all the files from the input_folder
	for root, dirs, files in os.walk(input_folder):
		for file in files:
			files_list.append(os.path.join(root, file))
	# get all the keys from the input_folder
	for root, dirs, files in os.walk(input_folder):
		for dir in dirs:
			keys_list.append(os.path.join(root, dir))
	# get all the warnings from the input_folder
	for root, dirs, files in os.walk(input_folder):
		for file in files:
			if os.path.splitext(file)[1] == '.txt':
				warnings_list.append(os.path.join(root, file))
	return files_list, keys_list, warnings_list


a,b,c = getALL(input)
print(a[0],b[0],c)