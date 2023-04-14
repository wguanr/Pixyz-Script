import os

def Revit_Process(input_folder, output_folder, extensions, ExportName):
	# removeAllVerbose()
	_root_ = advanced_imported_scene(input_folder)
	print('importing finished')

	advanced_export(output_folder, ExportName, extensions)
	print('exporting finished')

def removeAllVerbose():
	core.removeConsoleVerbose(2)
	core.removeLogFileVerbose(2)
	core.removeSessionLogFileVerbose(2)


def getFileNameWithoutExtension(file):
	return os.path.splitext(os.path.basename(file))[0]


class gets:
	RVT_deleted_expr = "(Property(\"Name\").Matches(\"^.*dwg.*$\")OR Property(\"Name\").Matches(\"^.*Text.*$\"))"
	# 映射关系
	Category = "Other/Category"
	# wall = scene.findByMetadata(Category, "^.*Wall.*", occs_root)
	RVT_ElementsList_One = ['Wall', 'Floor', 'Rail', 'Site', 'Pipes', 'Pipe Fitting', 'Cable Tray', 'Ducts', 'Duct Fitting']
	RVT_ElementsList_ISM = ['Window', 'Door', 'Equipment', 'Structural Column', 'Structural Framing', 'Sprinkler', 'Accessories', 'Curtain', 'Air Terminals']


def advanced_imported_scene(input_folder):
	input_folder_files_name = [file for file in os.listdir(input_folder) if (os.path.isfile(input_folder + '/' + file) and os.path.splitext(file)[1] not in ['.xml', ''])]
	elmts = gets.RVT_ElementsList_ISM + gets.RVT_ElementsList_One

	for file in input_folder_files_name:
		input_file_path = input_folder + '/' + file
		occs = process.guidedImport([input_file_path], pxz.process.CoordinateSystemOptions(["automaticOrientation", 0],	["automaticScale", 0], False,False), ["usePreset", 2],pxz.process.ImportOptions(False, True, True), False, False, False, False,False, False)
		##########################################
		# preapre and merging
		##########################################
		clean()
		clean_filtered_occurrences(gets.RVT_deleted_expr)
		# pre merging
		scene.mergePartsByAssemblies([1], 2)

		# create occs for each element, merged and prepare for instancing, remain generic models
		_count = 0
		for i in elmts:
			_count = _count + 1
			_rex = '^.*' + i + '.*'
			_ism = scene.findByMetadata(gets.Category, _rex, occs)
			_occ = scene.createOccurrenceFromSelection(i, _ism, occs[0], True)
			if _ism and _count > len(gets.RVT_ElementsList_ISM):
				scene.mergeParts([_occ], 2)
		##########################################
		# repair and decimate
		##########################################
		FileName = file.split("/")[-1]
		RVTcode = FileName.split("_")[2]
		# SS为钢结构，E为电气, P为管道, S为结构, M为机电, A为建筑
		if RVTcode in ["S", "GL"]:
			repairing(3)
			decimating(occs[0], 2)
		if RVTcode in ["M", "A", "SS", "E"]:
			repairing(2)
			decimating(occs[0], 2)
		if RVTcode in ["P"]:
			decimating(occs[0], 1)
	clean()


def advanced_export(output_folder, ExportName, extensions):
	if ExportName == "":
		ExportName = 'DefaultOutput'
	final_optimize()
	# Export files
	for extension in extensions:
		print(f'##################{extension}##################')
		fileName = f'{output_folder}/{ExportName}{extension}'
		io.exportScene(fileName, 0)

		print(f'exported one {extension} file')
		print(f'#' * 50)


def getStats(root):
	core.configureInterfaceLogger(False, False, False)  # hide next lines from logs

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
	print('{:<20s}{:<3s}\n'.format('triangles ', str(n_triangles) + ' -> ' + str(_n_triangles)))
	print('{:<20s}{:<3s}\n'.format('vertices ', str(n_vertices) + ' -> ' + str(_n_vertices)))
	print('{:<20s}{:<3s}\n'.format('parts ', str(n_parts) + ' -> ' + str(_n_parts)))