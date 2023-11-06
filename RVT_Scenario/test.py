import pathlib as pl
import os

input_folder = r'F:\PCG\pixyz\RVT_Scenario\_input\2023nianzuixin0302dikuairevitmoxing'
input_folder2 = r'E:\CIM_RVT\4403050020063700015_前海法治大厦'
input_folder3 = r'E:/CIM_RVT/4403050020063700015_前海法治大厦'
export_name = r'shoiadhso'
extension = r'.fbx'
fileName = os.path.join(input_folder3,export_name+extension)
print(fileName)
input = pl.Path(input_folder)
input = input.parent
output = pl.Path(input)


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


# pathlist = [r"F:\PCG\pixyz\RVT_Scenario\_input\2023nianzuixin0302dikuairevitmoxing\jianzhumoxing\talou\塔楼T1_AR.rvt", r"F:\PCG\pixyz\RVT_Scenario\_input\2023nianzuixin0302dikuairevitmoxing\jianzhumoxing\talou\塔楼T2_AR.rvt"]
# current_RootOccurence = process.guidedImport(
# 	pathlist, pxz.process.CoordinateSystemOptions(
# 		["automaticOrientation", 0],
# 		["automaticScale", 0], False,
# 		False), ["usePreset", 2],
# 	pxz.process.ImportOptions(
# 		False, True, True), False, False, False, False, False,
# 	False)
#
#
# print(len(current_RootOccurence))
# print("current_RootOccurence" + str(current_RootOccurence))

