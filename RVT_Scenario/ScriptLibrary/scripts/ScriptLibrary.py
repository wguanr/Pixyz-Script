import time
import json
import os
import pathlib as ph
import re


DebugMode = False


class GetParameters:
	################################
	# administration
	# supported_extensions = ['.rvt']

	################################
	# Project settings
	RVT_delete_byName = "(Property(\"Name\").Matches(\"^.*dwg.*$\")OR Property(\"Name\").Matches(\"^.*Text.*$\"))"
	RVT_merge_byName = "(Property(\"Name\").Matches(\"^.*Stairs.*$\")OR Property(\"Name\").Matches(\"^.*Walls.*$\")OR " \
	                   "Property(\"Name\").Matches(\"^.*Floors.*$\")OR Property(\"Name\").Matches(\"^.*Pipes.*$\")OR " \
	                   "Property(\"Name\").Matches(\"^.*Ducts.*$\")OR Property(\"Name\").Matches(\"^.*Fittings.*$\")OR " \
	                   "Property(\"Name\").Matches(\"^.*Railings.*$\")OR Property(\"Name\").Matches(\"^.*Cable " \
	                   "Tray.*$\")OR Property(\"Name\").Matches(\"^.*Structural Framing.*$\"))"
	Category = "Other/Category"
	# wall = scene.findByMetadata(Category, "^.*Wall.*", occs_root)
	RVT_ElementsList_One = ['Wall', 'Floor', 'Rail', 'Site', 'Pipes', 'Cable Tray', 'Fitting', 'Structural Framing',
	                        'Ducts', 'Duct Insulation']
	RVT_ElementsList_ISM = ['Window', 'Door', 'Stairs', 'Equipment', 'Structural Column',
	                        'Sprinkler', 'Accessories', 'Curtain', 'Air Terminals', 'Generic Model']

	# OPTIMIZATION
	ISM_dimensions = 0.98
	ISM_polycount = 0.90


# Todo add commuication with Pixyz:
#  core.askYesNo("question", False)
#  core.choose("message", values, 0)
#  core.setInteractiveMode(True)
#  core.checkLicense()

def RevitGeneralProcess(files_to_import,output_folder,export_name,extensions,key_of_files):
	"""
	Do importing and exporting based on the RVT_uniform_code and pattern_index
	:param files_to_import: list of files to import
	:param output_folder: folder directory to export
	:param export_name: file basename of the export file
	:param extensions: file extension of the export file
	:param key_of_files: string name
	"""
	OptimizeMode = 0

	output_folder = ph.Path(str(output_folder))
	log_path = output_folder / 'pixyz.log'
	core.setLogFile(str(log_path))

	RVT_uniform_code = str(key_of_files)
	import_list = files_to_import
	# debug print


	isImported = advanced_imported_scene(OptimizeMode, import_list, RVT_uniform_code)
	print('===========importing finished============\n')

	# export if imported successfully
	_conditions = [isImported, not DebugMode]
	if all(_conditions):
		# after import then execute to export
		advanced_export(output_folder, export_name, extensions)
		print('===========exporting finished============\n')
		core.resetSession()
	# reset session for next importing
	get_logo(3)


def advanced_imported_scene(OptimizeMode, files_to_import, RVT_uniform_code):
	"""
	 Do importing and optimizing based on the RVT_uniform_code and pattern_index
	:param files_to_import: list of file paths to import
	:param RVT_uniform_code: RVT_uniform_code
	:param pattern_index: pattern_index
	:return: isImported to know if the importing is successful
	"""

	try:
		process.guidedImport(
			files_to_import, pxz.process.CoordinateSystemOptions(
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
		optimization_RVT(RVT_uniform_code, OptimizeMode)
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


def optimization_RVT(RVT_uniform_code, OptimizeMode):
	"""
	Do merging, repairing, decimating using Pixyz!
	:param RVT_uniform_code: SS为钢结构，E为电气, P为管道, S为结构, M为机电, A为建筑, T为智能化
	:param OptimizeMode: 0 for Standard, 1 for customize
	"""
	# 0: General Optimization
	scene.resetPartTransform(1)
	scene.mergeFinalLevel([1], 2, True)  # so that to make instances
	algo.createInstancesBySimilarity(
		[1], GetParameters.ISM_dimensions, GetParameters.ISM_polycount,
		ignoreSymmetry=True, keepExistingPrototypes=False, createNewOccurrencesForPrototypes=True)

	##########################################
	# create current_RootOccurrence for each element, merged and prepare for instancing, remain generic models
	##########################################
	elmts = GetParameters.RVT_ElementsList_ISM + GetParameters.RVT_ElementsList_One
	TargetOccurrence = scene.getChildren(1)
	for occ in TargetOccurrence:
		if OptimizeMode == 0:
			# find by metadata
			_count = 0
			for i in elmts:
				_count = _count + 1
				_rex = '^.*' + i + '.*'
				_ism = scene.findByMetadata(GetParameters.Category, _rex, [occ])
				if _ism:
					_occ1 = scene.createOccurrenceFromSelection(i, _ism, occ, True)
					if _count > len(GetParameters.RVT_ElementsList_ISM):
						scene.mergeParts([_occ1], 2)

		elif OptimizeMode == 1:
			# find by name property
			occurrence_byFamily = scene.getFilteredOccurrences(GetParameters.RVT_merge_byName, 1)
			for _occ in occurrence_byFamily:
				scene.mergeParts([_occ], 2)

		elif OptimizeMode == 2:
			pass

	scene.deleteEmptyOccurrences()
	##########################################
	# General: repair and decimate
	##########################################
	if RVT_uniform_code in ["结构", "总图", "钢结构", "电气", "市政"]:
		repairing([1], 3)
		decimating(1, 3)
	if RVT_uniform_code in ["机电", "建筑", "智能化", "给排水", "暖通空调", "消防"]:
		repairing([1], 2)
		decimating(1, 2)


def advanced_export(output_folder, export_name, extensions):
	"""
	Export the scene to the specified format.

	"""
	removeAllVerbose()

	# Optimize for rendering
	algo.triangularize([1])
	algo.optimizeForRendering([1])

	# Write metadata and rename nodes
	part_occurrences = scene.getPartOccurrences(scene.getRoot())
	addAllVerbose()
	serializeMetadataToJSON(Part_Occurrences=part_occurrences, output_folder=output_folder)

	get_logo(2)
	print('Start exporting')
	print(f'output_folder is {output_folder} \r\nexport_name is {export_name}\r\n')
	print('\r\n')

	for extension in extensions:
		fileName = output_folder / (export_name + extension)
		io.exportScene(str(fileName))


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
	print('**************')
	print('serializeMetadataToJSON Begin')
	print('**************')

	# 通过循环，将每一个Occurrence的Metadata写入JSON文件,并且去重
	# 1. 字典推导式和update()避免多次循环构建字典,提高效率。
	# 2. 合并步骤减少,避免创建临时变量。
	# 3. 使用集合set自动去重,减少重复数据。
	# 4. 使用列表转换保留数据顺序。
	json_data = []
	for Target_Occurence in Part_Occurrences:
		print('Current_Occurrences is ', scene.getNodeName(Target_Occurence))
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
	# type : ANSI Shadow
	logo1 = (r'''
	
		██╗    ██╗██╗   ██╗██╗  ██╗ ██████╗ ███╗   ██╗ ██████╗ 
		██║    ██║██║   ██║██║ ██╔╝██╔═══██╗████╗  ██║██╔════╝ 
		██║ █╗ ██║██║   ██║█████╔╝ ██║   ██║██╔██╗ ██║██║  ███╗
		██║███╗██║██║   ██║██╔═██╗ ██║   ██║██║╚██╗██║██║   ██║
		╚███╔███╔╝╚██████╔╝██║  ██╗╚██████╔╝██║ ╚████║╚██████╔╝
		 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ 
		
		''')
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
	core.removeLogFileVerbose(5)
	core.removeSessionLogFileVerbose(2)


def addAllVerbose():
	core.addLogFileVerbose(2)
	core.addSessionLogFileVerbose(2)
	core.addConsoleVerbose(2)
