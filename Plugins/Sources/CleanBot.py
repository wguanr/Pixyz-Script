

#Preset
max_Occurrence_Name = 64

def clean():
	#global, called muti time.
	print("正在清理" )
	scene.cleanUnusedMaterials(True)
	scene.deleteEmptyOccurrences()
	scene.renameLongOccurrenceName(64)
	scene.removeUselessInstances(1)
	scene.resetTransform(1, True, True, False)  # 保留Instances的Transform
	# scene.compress()

#global, called only once.
#after deleting and merging
def final_optimize():
	clean_materials()
	algo.triangularize([1])
	#algo.removeDegeneratedPolygons([1], 50)
	algo.optimizeForRendering([1])
	algo.createInstancesBySimilarity([1], dimensionsSimilarity = 0.95, polycountSimilarity = 0.90, ignoreSymmetry = False, keepExistingPrototypes = True, createNewOccurrencesForPrototypes = True) 
	print ("Success! 优化结束！")



#deprecate!!!!!
def find_occurrences(DeletedOrMerged):
	#TODO add your code here.
	if DeletedOrMerged:
		occs = scene.getFilteredOccurrences(filter_exprs.RVT_deleted_expr)
	else:
		occs = scene.getFilteredOccurrences(filter_exprs.RVT_merged_expr)
	return occs

	
def clean_filtered_occurrences(FilterExpression):
	#TODO add your code here.
	try:
		scene.deleteOccurrences(scene.getFilteredOccurrences(FilterExpression))
		scene.deleteComponentsByType(2, [1])
		print("-过滤完成-")
		return True
	except:
		return False
		print("过滤了个大西瓜")

def clean_materials():
	algo.deleteLines([1])
	algo.identifyPatches([1], True, False, -1.000000000000, True, True, True, False)
	scene.cleanUnusedMaterials(True)
	scene.mergeMaterials()
	material.makeMaterialNamesUnique()


