import os
import time
import json
import os
import pathlib as ph


# 在Pixyz的环境下执行
# 递归查找每一个Occurrence，然后将其Metadata写入JSON文件
def serializeMetadataToJSON(Part_Occurences, output_folder):
	# prepare
	# make_unique_name, 为每一个Nodename添加ID
	# 将JSON字符串写入文件
	save_path = output_folder / 'user_data'
	if not save_path.exists():
		save_path.mkdir()
	print(save_path)
	# 通过循环，将每一个Occurrence的Metadata写入JSON文件,并且去重
	# 1. 字典推导式和update()避免多次循环构建字典,提高效率。
	# 2. 合并步骤减少,避免创建临时变量。
	# 3. 使用集合set自动去重,减少重复数据。
	# 4. 使用列表转换保留数据顺序。
	json_data = []
	for Target_Occurence in Part_Occurences:

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


def Revit_Process(input_folder, output_folder, export_name, extensions):
	# input_folder = 'F:\PCG\pixyz\RVT_Scenario\_input'
	# output_folder = 'F:\PCG\pixyz\RVT_Scenario\_output'

	input_folder = ph.Path(input_folder)
	output_folder = ph.Path(output_folder)

	get_logo(1)

	try:
		RVT_id, RVT_name, RVT_code = advanced_imported_scene(input_folder)
		print(RVT_id, RVT_name, RVT_code)
		import_status = True
	except PermissionError as e:
		if "Permission denied" in str(e):
			print("Error importing scene. Please check if you have read permission on the input folder.")
		elif "No such file or directory" in str(e):
			print("The input folder does not exist. Please check the file path and try again.")
		else:
			print("Error importing scene. Please check the input folder.")
		print(f"Error details: {e}")
		return
	print('===========importing finished============')

	if not export_name:
		export_name = f'{RVT_name}_{RVT_code}'
		print(export_name)
	# output_folder = RVT_code + '_' + output_folder
	if import_status:
		advanced_export(output_folder, export_name, extensions)
		print('===========exporting finished============')
		get_logo(3)

	core.resetSession()

class gets:
	RVT_deleted_expr = "(Property(\"Name\").Matches(\"^.*dwg.*$\")OR Property(\"Name\").Matches(\"^.*Text.*$\"))"
	# 映射关系
	Category = "Other/Category"
	# wall = scene.findByMetadata(Category, "^.*Wall.*", occs_root)
	RVT_ElementsList_One = ['Wall', 'Floor', 'Rail', 'Site', 'Pipes', 'Pipe Fitting', 'Cable Tray', 'Ducts',
	                        'Duct Fitting']
	RVT_ElementsList_ISM = ['Window', 'Door', 'Equipment', 'Structural Column', 'Structural Framing', 'Sprinkler',
	                        'Accessories', 'Curtain', 'Air Terminals']


def advanced_imported_scene(input_folder):
	global RVT_id, RVT_name, RVT_code
	supported_extensions = [".rvt", ".rfa"]
	input_folder_files_name = [file for file in os.listdir(input_folder) if (
			os.path.isfile(input_folder / file) and os.path.splitext(file)[1] in supported_extensions)]
	elmts = gets.RVT_ElementsList_ISM + gets.RVT_ElementsList_One
	print(input_folder_files_name)
	for file in input_folder_files_name:

		input_file_path = input_folder / file

		print(input_file_path)
		occs = process.guidedImport(
			[str(input_file_path)], pxz.process.CoordinateSystemOptions(
				["automaticOrientation", 0],
				["automaticScale", 0], False,
				False), ["usePreset", 2],
			pxz.process.ImportOptions(
				False, True, True), False, False, False, False, False,
			False)
		t0, n_triangles, n_vertices, n_parts = getStats(occs[0])
		# remove input file incase imported again by watcher
		os.remove(input_file_path)
		removeAllVerbose()
		##########################################
		# prepare and merging
		##########################################
		clean()
		clean_filtered_occurrences(gets.RVT_deleted_expr)
		clean_materials(occs)
		# pre merging
		scene.mergePartsByAssemblies([1], 2)

		# create occs for each element, merged and prepare for instancing, remain generic models
		_count = 0
		for i in elmts:
			_count = _count + 1
			_rex = '^.*' + i + '.*'
			_ism = scene.findByMetadata(gets.Category, _rex, occs)
			if _ism:
				_occ = scene.createOccurrenceFromSelection(
					i, _ism, occs[0], True)
				print(scene.getNodeName(_occ) + ' has been created')
				if _count > len(gets.RVT_ElementsList_ISM):
					scene.mergeParts([_occ], 2)
		##########################################
		# repair and decimate
		##########################################
		FileName = os.path.splitext(file)[0]
		RVT_code = FileName.split("_")[2]
		RVT_id = FileName.split("_")[0]
		RVT_name = FileName.split("_")[1]  # 可能是拼音哦
		# SS为钢结构，E为电气, P为管道, S为结构, M为机电, A为建筑, T为智能化
		if RVT_code in ["S", "GL"]:
			repairing(occs, 3)
			decimating(occs[0], 2)
		if RVT_code in ["M", "A", "SS", "E", "T"]:
			repairing(occs, 2)
			decimating(occs[0], 2)
		if RVT_code in ["P"]:
			decimating(occs[0], 1)
		##########################################
		t1, _n_triangles, _n_vertices, _n_parts = getStats(occs[0])
		addAllVerbose()
		printStats(
			FileName, t1 - t0, n_triangles, _n_triangles,
			n_vertices, _n_vertices, n_parts, _n_parts)
	scene.deleteEmptyOccurrences()
	print(RVT_id, RVT_name, RVT_code)
	print('\n===========importing finished============\n')
	return RVT_id, RVT_name, RVT_code


def advanced_export(output_folder, export_name, extensions):
	print(
		f'output_folder is {output_folder} \r\n export_name is {export_name}\r\n')
	final_optimize()
	# Write metadata
	part_occurrences = scene.getPartOccurrences(scene.getRoot())
	serializeMetadataToJSON(Part_Occurences=part_occurrences, output_folder=output_folder)
	# Export files
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

	core.configureInterfaceLogger(True, True, True)  # reenable logs

	return t, n_triangles, n_vertices, n_parts


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
def get_logo(logoindex: int) -> bool:
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
	return 1


def removeAllVerbose():
	core.removeConsoleVerbose(2)
	core.removeLogFileVerbose(2)
	core.removeSessionLogFileVerbose(2)


def addAllVerbose():
	core.addLogFileVerbose(2)
	core.addSessionLogFileVerbose(2)
	core.addConsoleVerbose(2)
