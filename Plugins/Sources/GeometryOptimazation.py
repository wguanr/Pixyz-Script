
#Presets
ModelPreset = 2

#main fuc
def model_factor(ModelPreset) -> float:
	#TODO add your code here.
	#if ModelPreset:
		# VeryHigh = 0
	#High = 1
	#Medium = 2
	#Low = 3
	#origin = nothing        
		model_PrecisionFactor = {            
						process.QualityPreset.Low: 50.0,
						process.QualityPreset.Medium: 15.0,
						process.QualityPreset.High: 2.0,
						process.QualityPreset.VeryHigh: 0.2,
					}
		return model_PrecisionFactor.get(ModelPreset, 0)
	

def repairing(Model_Quality):
	#TODO add your code here.
		print("正在修复错误……")
		# TargetOcc = scene.getChildren(target_occurrences)
		TargetOcc = [scene.getRoot()]
		# cad
		algo.repairCAD(TargetOcc, 1.000000 * model_factor(ModelPreset), False)
		algo.retessellate(TargetOcc, 5 * model_factor(ModelPreset), -1, -1, False, 0, 1, 0.0, False, False)
		#algo.tessellateRelativelyToAABB([1], 0.200000, 0.000300, -1, -1, True, 0, 1, 0.000000, False, False, True,False)
		# mesh
		algo.repairMesh(TargetOcc, 1 * model_factor(ModelPreset), False, True)
		algo.repairNullNormals(TargetOcc)
		algo.removeHoles(TargetOcc, True, True, False, 20)


def decimating(Target_Occurrences, Model_Quality):
	#TODO add your code here.
		print("正在优化三角面……")
		# if Proxy , continue the other way---proxy way, no decimating!
		surfacicTolerance = 10.0 * model_factor(Model_Quality)
		lineicTolerance = 1 * model_factor(Model_Quality)
		# query occs
		TargetOcc = []
		for occ in scene.getPartOccurrences(1):
			polygon_count = scene.getPolygonCount([occ], True, True, True) 
			if polygon_count > 10000 :
				TargetOcc.append(occ)
		print(TargetOcc)
		#general 
		algo.mergeVertices(TargetOcc, 0.5, pxz.polygonal.TopologyCategoryMask(7, 15))
		algo.decimateEdgeCollapse(TargetOcc, surfacicTolerance * 0.6, 1., 1., 1., 1., 10., -1, True, -1, -1, False, 0)

		algo.decimate(TargetOcc, surfacicTolerance, lineicTolerance, 10, -1, False)
		




