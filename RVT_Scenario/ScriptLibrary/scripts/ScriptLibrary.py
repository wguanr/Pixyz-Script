import time
import json
import os
import pathlib as ph

DebugMode = False


class GetParameters:
	################################
	# administration
	# supported_extensions = ['.rvt']
	################################
	# Project settings
	RVT_delete_byName = "(Property(\"Name\").Matches(\"^.*dwg.*$\")OR Property(\"Name\").Matches(\"^.*Text.*$\"))"
	RVT_merge_byName = "(Property(\"Name\").Matches(\"^.*Stairs.*$\")OR Property(\"Name\").Matches(\"^.*Walls.*$\")OR Property(\"Name\").Matches(\"^.*Floors.*$\"))"
	Category = "Other/Category"
	# wall = scene.findByMetadata(Category, "^.*Wall.*", occs_root)
	RVT_ElementsList_One = ['Wall', 'Floor', 'Rail', 'Site', 'Pipes', 'Cable Tray', 'Fitting', 'Ducts',
	                        'Duct Insulation']
	RVT_ElementsList_ISM = ['Window', 'Door', 'Stairs', 'Equipment', 'Structural Column', 'Structural Framing',
	                        'Sprinkler', 'Accessories', 'Curtain', 'Air Terminals', 'Generic Model']


# Todo add commuication with Pixyz:
#  core.askYesNo("question", False)
#  core.choose("message", values, 0)
#  core.setInteractiveMode(True)
#  core.checkLicense()

def Revit_Process(input, extensions, pattern_index):
	# input= r'F:\PCG\pixyz\RVT_Scenario\_input\2023nianzuixin0302dikuairevitmoxing\muqiangmoxing'
	# output = 'F:\PCG\pixyz\RVT_Scenario\_output'
	if not os.path.exists(input):
		print('Revit_Process input is not a valid path')
		return

	input_folder = ph.Path(input)
	output_folder = ph.Path(input).parent / '_output'
	output_folder.mkdir(parents=True, exist_ok=True)
	# print('current input folder is:' + str(input_folder))
	get_logo(1)
	b_isValid = isValid(input_folder, pattern_index)
	print('\n------------------ ')
	print('file check result:')
	print(b_isValid)
	print('------------------ \n')

	# b_isValid = False
	if b_isValid:
		fl, k = getALL(input_folder)
		for f in fl:
			for _k in k:
				if f.get(_k):
					# prepare to import all files in this directory
					models_to_import = f.get(_k)
					print('models  ' + str(models_to_import))
					RVT_id, RVT_name, RVT_code = getInfoFromFile(models_to_import[0], 1)
					# print(rvt_id, rvt_name, rvt_code)
					_output_folder = output_folder / str(RVT_id) / str(_k) / str(RVT_code)
					_output_folder.mkdir(parents=True, exist_ok=True)
					_export_name = f'ID_{RVT_id}_{RVT_code}'
					print('current output folder is:' + str(_output_folder))
					print('current export basename is:' + _export_name)
					# set log file path
					log_path = _output_folder / 'pixyz.log'
					core.setLogFile(str(log_path))

					# import all files in this directory
					print('===========importing now ============\n')
					import_list = []
					for _model in models_to_import:
						import_list.append(str(_model))
					print(import_list)
					isImported = advanced_imported_scene(import_list, RVT_code, pattern_index)
					print('===========importing finished============\n')

					# export if imported successfully
					_conditions = [isImported, not DebugMode]
					if all(_conditions):
						# after import then execute to export
						advanced_export(_output_folder, _export_name, extensions)
						print('===========exporting finished============\n')

					# reset session for next importing
					get_logo(3)
					core.resetSession()
	else:
		print('===========file is in valid============')
		get_logo(2)
		return


# core.message("\n Revit_Process finished \n")


def advanced_imported_scene(files_to_import, RVT_code, pattern_index):
	"""
	 Do importing and optimizing based on the RVT_code and pattern_index
	:param files_to_import: list of file paths to import
	:param RVT_code: RVT_code
	:param pattern_index: pattern_index
	:return: isImported to know if the importing is successful
	"""

	try:
		process.guidedImport(files_to_import, pxz.process.CoordinateSystemOptions(
				["automaticOrientation", 0],
				["automaticScale", 0], False,
				False), ["usePreset", 2],
			pxz.process.ImportOptions(
				False, True, True), False, False, False, False, False,
			False)
		t0, n_triangles, n_vertices, n_parts = getStats(1)

		removeAllVerbose()
			##########################################
			# 1. prepare and merging
			##########################################
		clean()
		clean_filtered_occurrences(GetParameters.RVT_delete_byName)
		clean_materials([1])
		scene.mergePartsByAssemblies([1], 2)

		##########################################
		# 2. main optimization
		##########################################
		# ? temperately make merging_mode=pattern_index
		for _occ in scene.getChildren(1):
			optimization_RVT([_occ], RVT_code, merging_mode=pattern_index)
		##########################################

		t1, _n_triangles, _n_vertices, _n_parts = getStats(1)

		scene.deleteEmptyOccurrences()  # default occ = 0
		addAllVerbose()
		title_name = 'Status log : \r\n what we did in this file: \r\n'
		printStats(
			title_name, t1 - t0, n_triangles, _n_triangles,
			n_vertices, _n_vertices, n_parts, _n_parts)
		return True
	except PermissionError as e:
		if "Permission denied" in str(e):
			print(
				"Error importing scene. Please check if you have read permission on the input folder.")
		elif "No such file or directory" in str(e):
			print("The input folder does not exist. Please check the file path and try again.")
		else:
			print("Error importing scene. Please check the input folder.")
		print(f"Error details: {e}")
		return False


def optimization_RVT(current_RootOccurrence, RVT_code, merging_mode):
	"""
	Do merging, repairing, decimating using Pixyz!

	:param current_RootOccurrence: list of guidedImported occurences
	:param RVT_code: SS为钢结构，E为电气, P为管道, S为结构, M为机电, A为建筑, T为智能化
	:param merging_mode: 0: 分层模型, 1: 分栋模型, 2: 多楼栋模型
	"""
	elmts = GetParameters.RVT_ElementsList_ISM + GetParameters.RVT_ElementsList_One
	# create current_RootOccurrence for each element, merged and prepare for instancing, remain generic models
	if merging_mode == 0:

		_count = 0
		for i in elmts:
			_count = _count + 1
			_rex = '^.*' + i + '.*'
			_ism = scene.findByMetadata(GetParameters.Category, _rex, current_RootOccurrence)
			if _ism:
				_occ = scene.createOccurrenceFromSelection(
					i, _ism, current_RootOccurrence[0], True)
				print(scene.getNodeName(_occ) + ' has been created')
				if _count > len(GetParameters.RVT_ElementsList_ISM):
					scene.mergeParts([_occ], 2)

	elif merging_mode == 1:
		occurrence_byFamily = scene.getFilteredOccurrences(GetParameters.RVT_merge_byName, current_RootOccurrence[0])
		for _occ in occurrence_byFamily:
			scene.mergeParts([_occ], 2)
	elif merging_mode == 2:
		pass

	scene.deleteEmptyOccurrences()
	scene.mergeFinalLevel(current_RootOccurrence, 2, True)  # so that to make instances
	scene.resetPartTransform(1)
	##########################################
	# General: repair and decimate
	##########################################
	if RVT_code in ["S", "GL"]:
		repairing(current_RootOccurrence, 3)
		decimating(current_RootOccurrence[0], 2)
	if RVT_code in ["M", "A", "SS", "E", "T", "AR"]:
		repairing(current_RootOccurrence, 2)
		decimating(current_RootOccurrence[0], 2)
	if RVT_code in ["P"]:
		decimating(current_RootOccurrence[0], 1)


def advanced_export(output_folder, export_name, extensions):
	"""
	Export the scene to the specified format.

	"""
	removeAllVerbose()
	final_optimize()
	# Write metadata
	part_occurrences = scene.getPartOccurrences(scene.getRoot())
	serializeMetadataToJSON(Part_Occurrences=part_occurrences, output_folder=output_folder)
	# Export files
	# if not os.path.exists(output_folder):
	# 	os.makedirs(output_folder)
	addAllVerbose()
	print(
		f'output_folder is {output_folder} \r\nexport_name is {export_name}\r\n')
	for extension in extensions:
		fileName = output_folder / (export_name + extension)
		try:
			io.exportScene(str(fileName))
			print('\r\n')
			print(f'export one {extension} file')
			print('\r\n')
		except:
			print('\r\n')
			print('=====exporting failed!=========')
			print('\r\n')


def getStats(root):
	# hide next lines from logs
	core.configureInterfaceLogger(False, False, False)

	t = time.time()
	n_triangles = scene.getPolygonCount([root], True, False, False)
	n_vertices = scene.getVertexCount([root], False, False, False)
	n_parts = len(scene.getPartOccurrences(root))

	core.configureInterfaceLogger(True, True, True)  # reasonable logs

	return t, n_triangles, n_vertices, n_parts


# 在Pixyz的环境下执行
# 递归查找每一个Occurrence，然后将其Metadata写入JSON文件
def serializeMetadataToJSON(Part_Occurrences, output_folder):
	# prepare
	# make_unique_name, 为每一个Nodename添加ID
	# 将JSON字符串写入文件
	save_path = output_folder / 'Local_Metadata'
	if not save_path.exists():
		save_path.mkdir()
	print(save_path)
	# 通过循环，将每一个Occurrence的Metadata写入JSON文件,并且去重
	# 1. 字典推导式和update()避免多次循环构建字典,提高效率。
	# 2. 合并步骤减少,避免创建临时变量。
	# 3. 使用集合set自动去重,减少重复数据。
	# 4. 使用列表转换保留数据顺序。
	json_data = []
	for Target_Occurence in Part_Occurrences:

		Metadata_Comp = scene.getComponentByOccurrence([Target_Occurence], 5, True)
		Metadata_Defis = scene.getMetadatasDefinitions(Metadata_Comp)

		json_data_metadata = {}
		for Metadata_KeyValue in Metadata_Defis:
			if not Metadata_KeyValue:
				continue
			_name = scene.getActivePropertyValue(Target_Occurence, "Name", True)
			name_value = f'{_name}_{Target_Occurence}'
			_NodeName = core.setProperty(Target_Occurence, "Name", name_value)
			json_data_metadata.update({Metadata.name: Metadata.value for Metadata in Metadata_KeyValue})

		NodeName = scene.getNodeName(Target_Occurence)
		json_data.append(
			{
				'NodeName': NodeName,
				**json_data_metadata
				})

	json_data = list(json_data)
	json_str = json.dumps(json_data, ensure_ascii=False, indent=4)
	# print(json_str)
	with open(save_path / 'Metadata.json', 'w', encoding='utf-8') as f:
		f.write(json_str)
		f.write('\n')

	return save_path


def printStats(fileName, t, n_triangles, _n_triangles, n_vertices, _n_vertices, n_parts, _n_parts):
	print('\n')
	print('{:<20s}{:<3s}\n'.format('file ', fileName))
	print('{:<20s}{:<8.3f}{:<3s}\n'.format('optimization ', t, ' s'))
	print(
		'{:<20s}{:<3s}\n'.format(
			'triangles ', str(
				n_triangles) + ' -> ' + str(_n_triangles)))
	print(
		'{:<20s}{:<3s}\n'.format(
			'vertices ', str(
				n_vertices) + ' -> ' + str(_n_vertices)))
	print(
		'{:<20s}{:<3s}\n'.format(
			'parts ', str(n_parts) + ' -> ' + str(_n_parts)))


# Get logo based on logoindex
def get_logo(logoindex: int):
	logo1 = (r'' '\n'
	         r' _       __ __  __ __ __ ____   _   __ ______' '\n'
	         r'| |     / // / / // //_// __ \ / | / // ____/' '\n'
	         r'| | /| / // / / // ,<  / / / //  |/ // / __  ' '\n'
	         r'| |/ |/ // /_/ // /| |/ /_/ // /|  // /_/ /  ' '\n'
	         r'|__/|__/ \____//_/ |_|\____//_/ |_/ \____/   ' '\n'
	         r'                                             ' '\n'
	         r'    ')
	logo2 = (r'' '\n'
	         r'                                          ' '\n'
	         r' _ _ _  _____  _____  _____  _____  _____ ' '\n'
	         r'| | | ||  |  ||  |  ||     ||   | ||   __|' '\n'
	         r'| | | ||  |  ||    -||  |  || | | ||  |  |' '\n'
	         r'|_____||_____||__|__||_____||_|___||_____|' '\n'
	         r'                                        ' '\n'
	         r'    ')
	logo3 = (r'' '\n'
	         r'    ' '\n'
	         r'    ___      ___      ___      ___      ___      ___   ' '\n'
	         r'   /\__\    /\__\    /\__\    /\  \    /\__\    /\  \  ' '\n'
	         r'  /:/\__\  /:/ _/_  /:/ _/_  /::\  \  /:| _|_  /::\  \ ' '\n'
	         r' /:/:/\__\/:/_/\__\/::-"\__\/:/\:\__\/::|/\__\/:/\:\__\ ' '\n'
	         r' \::/:/  /\:\/:/  /\;:;-",-"\:\/:/  /\/|::/  /\:\:\/__/' '\n'
	         r'  \::/  /  \::/  /  |:|  |   \::/  /   |:/  /  \::/  / ' '\n'
	         r'   \/__/    \/__/    \|__|    \/__/    \/__/    \/__/  ' '\n'
	         r'' '\n'
	         r'    ')
	logos = [logo1, logo2, logo3]

	print(logos[logoindex - 1])
	return True


def removeAllVerbose():
	core.removeConsoleVerbose(2)
	core.removeLogFileVerbose(2)
	core.removeSessionLogFileVerbose(2)


def addAllVerbose():
	core.addLogFileVerbose(2)
	core.addSessionLogFileVerbose(2)
	core.addConsoleVerbose(2)
