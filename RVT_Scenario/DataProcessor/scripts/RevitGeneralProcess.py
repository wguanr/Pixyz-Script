import time

import pathlib as ph
import re

DebugMode = True


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
	RVT_ElementsList_One = ['Wall', 'Floor','Roof', 'Rail', 'Site', 'Pipes', 'Cable Tray', 'Fitting', 'Structural Framing',
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
def RevitInFME(input_path, output_dir, output_filename, DimensionsSimilarity, PolycountSimilarity):

	output_path = ph.Path(str(output_path))
	output_folder = output_path.parent
	output_extension = output_path.suffix
	export_name = output_path.stem
	log_path = output_folder / 'pixyz.log'
	core.setLogFile(str(log_path))

	model_name = ph.Path(str(input_path)).stem.split("_")[1]
	# RVT_uniform_code = export_name.split('_')[2]
	import_list = input_path
	# debug print : print all the parameters
	print('===========importing parameters============\n')
	# print(f'output_folder is {output_folder} \r\nexport_name is {export_name}\r\n')
	# print(f'output_extension is {output_extension}\r\n')
	# print(f'export_name is {export_name}\r\n')
	# print(f'model_name is {model_name}\r\n')
	# print(f'RVT_uniform_code is {RVT_uniform_code}\r\n')
	print(f'import_list is {import_list}\r\n')

	isImported = advanced_imported_scene_FME(import_list, DimensionsSimilarity, PolycountSimilarity)

	# export if imported successfully
	_conditions = [isImported, not DebugMode]
	if all(_conditions):
		# after import then execute to export
		advanced_export(output_folder, export_name, output_extension)
		core.resetSession()
	# reset session for next importing
	get_logo(3)


def RevitGeneralProcess(files_to_import, output_folder, export_name, extensions, key_of_files):

	OptimizeMode = 1

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


def advanced_imported_scene_FME(import_list, DimensionsSimilarity, PolycountSimilarity):

	try:
		process.guidedImport(
			import_list, pxz.process.CoordinateSystemOptions(
				["automaticOrientation", 0],
				["automaticScale", 0], False,
				False), ["usePreset", 2],
			pxz.process.ImportOptions(
				False, True, True), False, False, False, False, False,
			False)
		t0, n_triangles, n_vertices, n_parts = getStats(1)

		removeAllVerbose()
		optimization_Preparation()

		##########################################
		# 2. main optimization and resorting
		##########################################
		scene.resetPartTransform(1)
		scene.mergeFinalLevel([1], 2, True)  # so that to make instances
		algo.createInstancesBySimilarity(
			[1], DimensionsSimilarity, PolycountSimilarity,
			ignoreSymmetry=True, keepExistingPrototypes=False, createNewOccurrencesForPrototypes=True)

		elmts = GetParameters.RVT_ElementsList_ISM + GetParameters.RVT_ElementsList_One
		TargetOccurrence = scene.getChildren(1)
		for occ in TargetOccurrence:
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

		scene.deleteEmptyOccurrences()

		general_repair_and_decimate(RVT_uniform_code)

		t1, _n_triangles, _n_vertices, _n_parts = getStats(1)

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


def advanced_imported_scene(OptimizeMode, files_to_import, RVT_uniform_code):

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
		optimization_Preparation()

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


def optimization_Preparation():
	##########################################
	# 1. prepare and merging
	##########################################
	clean()
	clean_filtered_occurrences(GetParameters.RVT_delete_byName)
	clean_materials([1])
	scene.mergePartsByAssemblies([1], 2)


def optimization_RVT(RVT_uniform_code, OptimizeMode):

	# 0: General Optimization
	scene.resetPartTransform(1)
	scene.mergeFinalLevel([1], 2, True)  # so that to make instances
	algo.createInstancesBySimilarity(
		[1], GetParameters.ISM_dimensions, GetParameters.ISM_polycount,
		ignoreSymmetry=True, keepExistingPrototypes=False, createNewOccurrencesForPrototypes=True)


	elmts = GetParameters.RVT_ElementsList_ISM + GetParameters.RVT_ElementsList_One
	TargetOccurrence = scene.getChildren(1)
	for occ in TargetOccurrence:
		if OptimizeMode == 0:
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
			occurrence_byFamily = scene.getFilteredOccurrences(GetParameters.RVT_merge_byName, 1)
			for _occ in occurrence_byFamily:
				scene.mergeParts([_occ], 2)

		elif OptimizeMode == 2:
			pass

	scene.deleteEmptyOccurrences()

	general_repair_and_decimate(RVT_uniform_code)


def general_repair_and_decimate(RVT_uniform_code):

	if RVT_uniform_code in ["结构", "总图", "钢结构", "电气", "市政"]:
		repairing([1], 3)
		decimating(1, 3)
	if RVT_uniform_code in ["机电", "建筑", "智能化", "给排水", "暖通空调", "消防"]:
		repairing([1], 2)
		decimating(1, 2)


def advanced_export(output_folder, export_name, extensions):

	removeAllVerbose()

	algo.triangularize([1])
	algo.optimizeForRendering([1])

	# Write metadata and rename nodes
	addAllVerbose()
	StandardSerialization(output_folder)

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
	logo3 = (r'''
		    ____ _    ________   ____        __        ______           __           
		   / __ \ |  / /_  __/  / __ \____ _/ /_____ _/ ____/__  ____  / /____  _____
		  / /_/ / | / / / /    / / / / __ `/ __/ __ `/ /   / _ \/ __ \/ __/ _ \/ ___/
		 / _, _/| |/ / / /    / /_/ / /_/ / /_/ /_/ / /___/  __/ / / / /_/  __/ /    
		/_/ |_| |___/ /_/____/_____/\__,_/\__/\__,_/\____/\___/_/ /_/\__/\___/_/     
		               /_____/                                                       
			''')
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
