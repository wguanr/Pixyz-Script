# Preset
max_Occurrence_Name = 64


def clean():
	# global, called muti time.
	scene.cleanUnusedMaterials(True)
	scene.deleteEmptyOccurrences()
	scene.renameLongOccurrenceName(64)
	scene.removeUselessInstances(1)


# after deleting and merging
def final_optimize():
	scene.mergeFinalLevel([1], 2, True)
	algo.createInstancesBySimilarity(
		[1], dimensionsSimilarity=0.95, polycountSimilarity=0.90,
		ignoreSymmetry=False, keepExistingPrototypes=True, createNewOccurrencesForPrototypes=True)
	algo.triangularize([1])
	# algo.removeDegeneratedPolygons([1], 50)
	algo.optimizeForRendering([1])
	print("Final optimized with instances")


# deprecate!!!!!
def find_occurrences(DeletedOrMerged):
	if DeletedOrMerged:
		occs = scene.getFilteredOccurrences(filter_exprs.RVT_deleted_expr)
	else:
		occs = scene.getFilteredOccurrences(filter_exprs.RVT_merged_expr)
	return occs


def clean_filtered_occurrences(FilterExpression):
	try:
		scene.deleteOccurrences(scene.getFilteredOccurrences(FilterExpression))
		scene.deleteComponentsByType(2, [1])
		return True
	except:
		return False
		print("nothing returned")


def clean_materials(Target_Occurrences):
	algo.deleteLines(Target_Occurrences)
	algo.identifyPatches(
		Target_Occurrences, True, False, -
		1.000000000000, True, True, True, False)
	scene.cleanUnusedMaterials(True)
	scene.mergeMaterials()
	material.makeMaterialNamesUnique()
