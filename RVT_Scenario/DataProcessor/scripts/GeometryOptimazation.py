# main fuc
def model_factor(ModelPreset) -> float:
	"""
    :param ModelPreset: VeryHigh = 0; High = 1; Medium = 2; Low = 3
    """
	# if ModelPreset:
	#
	model_PrecisionFactor = {
		process.QualityPreset.Low: 100.0,
		process.QualityPreset.Medium: 50.0,
		process.QualityPreset.High: 10,
		process.QualityPreset.VeryHigh: 4,
		}
	return model_PrecisionFactor.get(ModelPreset, 0)


def repairing(Target_Occurrences, Model_Quality):
	# print("正在修复错误……")
	# TargetOcc = scene.getChildren(target_occurrences)
	TargetOcc = Target_Occurrences
	# cad
	algo.repairCAD(TargetOcc, 1.000000 * model_factor(Model_Quality), False)
	algo.retessellate(
		TargetOcc, 5 * model_factor(Model_Quality), -
		1, -1, False, 0, 1, 0.0, False, False)
	# algo.tessellateRelativelyToAABB([1], 0.200000, 0.000300, -1, -1, True, 0, 1, 0.000000, False, False, True,False)
	# mesh
	algo.repairMesh(TargetOcc, 1 * model_factor(Model_Quality), True, True)
	algo.removeHoles(TargetOcc, True, True, False, 20)
	algo.repairNullNormals(TargetOcc)
	algo.createNormals(TargetOcc, -1.000000000000, True, True)


# todo: Target_Occurrence need to be a list, will be used in studio
def decimating(Target_Occurrence, Model_Quality):
	# print("正在优化三角面……")
	surfacicTolerance = 10.0 * model_factor(Model_Quality)
	lineicTolerance = 1 * model_factor(Model_Quality)
	# query occs
	TargetOcc = []
	for occ in scene.getPartOccurrences(Target_Occurrence):
		polygon_count = scene.getPolygonCount([occ], True, True, True)
		if polygon_count > 10000:
			TargetOcc.append(occ)
	######################
	# general
	######################
	if TargetOcc:
		algo.mergeVertices(
			TargetOcc, 0.5, pxz.polygonal.TopologyCategoryMask(7, 15))
		algo.decimateEdgeCollapse(
			TargetOcc, surfacicTolerance * 0.6, 1., 1., 1., 1., 10., -1, True, -1, -1, False, 0)
		algo.decimate(
			TargetOcc, surfacicTolerance,
			lineicTolerance, 10, -1, False)
	algo.repairNullNormals(TargetOcc)
	algo.createNormals(TargetOcc, -1.000000000000, True, True)


def AdvancedDecimating(Target_Occurrences, Model_Quality):
	# print("正在优化三角面……")
	surfacicTolerance = 10.0 * model_factor(Model_Quality)
	lineicTolerance = 1 * model_factor(Model_Quality)

	TargetOcc = []
	if len(Target_Occurrences) == 0 or len(Target_Occurrences) > 20:
		raise Exception("Null | 选择太多了，性能消耗巨大，请减少个数！")
	for Target_Occurrence in Target_Occurrences:
		for occ in scene.getPartOccurrences(Target_Occurrence):
			polygon_count = scene.getPolygonCount([occ], True, True, True)
			if polygon_count > 10000:
				TargetOcc.append(occ)
	######################
	# general
	######################
	if TargetOcc:
		algo.mergeVertices(
			TargetOcc, 0.5, pxz.polygonal.TopologyCategoryMask(7, 15))
		algo.decimateEdgeCollapse(
			TargetOcc, surfacicTolerance * 0.6, 1., 1., 1., 1., 10., -1, True, -1, -1, False, 0)
		algo.decimate(
			TargetOcc, surfacicTolerance,
			lineicTolerance, 10, -1, False)
	algo.repairNullNormals(TargetOcc)
	algo.createNormals(TargetOcc, -1.000000000000, True, True)
	print("Status:三角面优化完成！")


def AdvancedMerging(Target_Occurrences, Type):
	print("Status:正在合并……")
	Category = "Other/Category"
	# wall = scene.findByMetadata(Category, "^.*Wall.*", occs_root)
	RVT_ElementsList_One = ['Wall', 'Floor', 'Roof', 'Rail', 'Site', 'Pipes', 'Cable Tray', 'Fitting','Ramp','Structural','Duct','Slab']
	RVT_ElementsList_ISM = ['Window', 'Door', 'Stairs', 'Equipment',
	                        'Sprinkler', 'Accessories', 'Curtain', 'Air Terminals', 'Generic Model']

	elmts = RVT_ElementsList_ISM + RVT_ElementsList_One
	scene.mergeFinalLevel(Target_Occurrences, 2, True)

	for RootOccurrences in Target_Occurrences:
		TargetOccurrence = scene.getChildren(RootOccurrences)
		for occ in TargetOccurrence:
			_count = 0
			for i in elmts:
				_count = _count + 1
				_rex = '^.*' + i + '.*'
				_ism = scene.findByMetadata(Category, _rex, [occ])
				if _ism:
					_occ1 = scene.createOccurrenceFromSelection(i, _ism, occ, True)
					if _count > len(RVT_ElementsList_ISM):
						scene.mergeParts([_occ1], 2)
	print("Status:合并完成！")
	scene.deleteEmptyOccurrences(1)


def AdvancedExport(Level):
	algo.triangularize([1])
	algo.optimizeForRendering([1])
	print('=========Start exporting=========')

	Target_Occurrences = scene.getRoot().getChildren()
	io.exportScene()
