old_mats = [59012818]
for mat in old_mats:
	scene.replaceMaterial(mat, 59151440, [1])
	
scene.cleanUnusedMaterials()