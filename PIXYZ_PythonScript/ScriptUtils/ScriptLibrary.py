# make autoScript with pxz api
import getLibrary as getlib
from pxz import *

#presets
Target = getlib.LOD_set.LOD2
target_occurrences = getlib.target_occurrences()
model_factor = getlib.model_factor(Target,1)
print(f"目前的处理目标是：{Target.value} ,模型数 = {model_factor}")


def init_op(index:float):
	init_op = {
		0 : 1
	}
	init_op.get(index)
	
	print("Lib已经导入")
	clean_bot().clean()
	clean_bot().clean_filtered_occurrences()
	ge = geometry_optimization()
	print("______________________________________")
	ge.decimating()
	ge.repairing()
	ge.merging(0)
	ge.merging(1)
	ge.merging(3)
	clean_bot().clean()
	mo = material_operation()
	mo.opt()

# 1.清理
class clean_bot:
	#先清理删除，再优化
	def __init__(self):
		self.max_Occurrence_Name = 64
		# self.optimazing()

	def clean(self):
		print("正在清理" + str(target_occurrences))
		scene.cleanUnusedMaterials(True)
		scene.deleteEmptyOccurrences()
		scene.renameLongOccurrenceName(self.max_Occurrence_Name)
		scene.removeUselessInstances(1)
		scene.resetTransform(1, True, True, False)  # 保留Instances的Transform
		scene.compress()
		
	
	def clean_filtered_occurrences(self):
		try:
			scene.deleteOccurrences(getlib.useless_occurrences)
			scene.deleteComponentsByType(2, target_occurrences)
			print(f"{getlib.useless_occurrences}-过滤完成-")
		except:
			print("过滤了个大西瓜")

	def clean_futher(self):
		# not neccessory if guided import
		algo.deleteFreeVertices([1])
		algo.deleteLines([1])
	
	def optimazing(self):
		algo.triangularize([1])
		algo.removeDegeneratedPolygons(target_occurrences, 50)
		algo.optimizeForRendering(target_occurrences)
		algo.createInstancesBySimilarity(target_occurrences, dimensionsSimilarity = 0.96, polycountSimilarity = 0.96, ignoreSymmetry = False, keepExistingPrototypes = True, createNewOccurrencesForPrototypes = True) 
		scene.removeUselessInstances()
	


# 针对几何的优化
class geometry_optimization:
	def __init__(self):
		self.surfacicTolerance = 10 * model_factor
		self.lineicTolerance = 1 * model_factor

	def repairing(self):
		
		print("正在修复错误……")
		# TargetOcc = scene.getChildren(target_occurrences)
		TargetOcc = [target_occurrences]
		# cad
		algo.repairCAD(TargetOcc, 1.000000, False)
		algo.retessellate(TargetOcc, 5, -1, -1, False, 0, 1, 0.0, False, False)
		#algo.tessellateRelativelyToAABB([1], 0.200000, 0.000300, -1, -1, True, 0, 1, 0.000000, False, False, True,False)
		# mesh
		algo.repairMesh(TargetOcc, 0.5, False, True)
		algo.repairNullNormals(TargetOcc)
		algo.removeHoles(TargetOcc, True, True, False, 20)

		 
	def decimating(self):
		print("正在优化三角面……")
		# if Proxy , continue the other way---proxy way, no decimating!
		if Target == "Proxy":
		   return False
	   # query occs
		TargetOcc = []
		for occ in scene.getChildren(target_occurrences):
			polygon_count = scene.getPolygonCount([occ], True, True, True) 
			if polygon_count > 10000 :
				TargetOcc.append(occ)
				print(polygon_count)
		#general 
		algo.mergeVertices(TargetOcc, 0.5, pxz.polygonal.TopologyCategoryMask(7, 15))
		algo.decimateEdgeCollapse(TargetOcc, self.surfacicTolerance * 0.5, 1., 1., 1., 1., 10., -1, True, -1, -1, False, 0)
		# LOD 1 2
		if Target == "Simplified":
			#keep topology
			algo.decimateTarget(TargetOcc, ["ratio", 80.0], 0, True, 5000000) # if bug , review the iterativeThreshold
		else:
			# LOD 3 4 5 0
			algo.decimate(TargetOcc, self.surfacicTolerance, self.lineicTolerance, 10, -1, False)
		
	def merging(self,merge_method_index:int):
		maxLevel = 7
		merging_method = {
			0 : scene.mergeParts([target_occurrences], 2),
			1 : scene.mergePartsByAssemblies([target_occurrences], 2),
			2 : scene.mergeByTreeLevel([1], maxLevel, 2),
			3 : scene.mergePartsByMaterials([target_occurrences], False, 2, True),
			4 : scene.mergePartsByName(1, 2) #need rootOcc 
		}
		merging_method[merge_method_index]
  		algo.optimizeCADLoops(occurrences)
		
	def removing(self):
		_ret_ = scene.getPolygonCount([1], True, True, True)
		algo.smartHiddenRemoval(target_occurrences, 0, 100, 1, 256, 0, False, 1)
	
	def making_poxy(self):
		algo.combineMeshes(target_occurrences, pxz.algo.BakeOption(0, 2048, 1, pxz.algo.BakeMaps(True, False, False, False, True, False, False)), True)
		algo.proxyMesh(target_occurrences, 500, 0, 0, False)


# 材质操作
class material_operation:
	def __init__(self):
		print('正在处理材质……')

	def replace(self, origin_materials, new_material):
		# 使用Filter
		for mat in origin_materials:
			scene.replaceMaterial(mat, new_material, [1])


	def opt(self):
		algo.deleteLines([target_occurrences])
		algo.identifyPatches([1], True, False, -1.000000000000, True, True, True, False)
		scene.cleanUnusedMaterials(True)
		scene.mergeMaterials()
		material.makeMaterialNamesUnique()


#debug测试运行
def main():
	# 这里是需要执行的程序代码
	print("Lib已经导入")
	clean_bot().clean()
	clean_bot().clean_filtered_occurrences()
	ge = geometry_optimization()
	print("______________________________________")
	# ge.decimating()
	# ge.repairing()
	# ge.merging(0)
	# ge.merging(1)
	# ge.merging(3)
	clean_bot().clean()
	mo = material_operation()
	mo.opt()


if __name__ == '__main__':
	main()
