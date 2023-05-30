# Preset
max_Occurrence_Name = 64


def clean():
	# global, could be called muti time.
	scene.cleanUnusedMaterials(True)
	scene.deleteEmptyOccurrences()
	scene.renameLongOccurrenceName(64)
	scene.removeUselessInstances(1)


def clean_filtered_occurrences(FilterExpression):
	try:
		scene.deleteOccurrences(scene.getFilteredOccurrences(FilterExpression))
		scene.deleteComponentsByType(2, [1])
		return True
	except:
		print("nothing returned")
		return False


def clean_materials(Target_Occurrences):
	algo.deleteLines(Target_Occurrences)
	algo.identifyPatches(
		Target_Occurrences, True, False, -
		1.000000000000, True, True, True, False)
	scene.cleanUnusedMaterials(True)
	scene.mergeMaterials()
	material.makeMaterialNamesUnique()
