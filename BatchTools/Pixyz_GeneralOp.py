scene.applyTransformation(1, [[1.000000, 0.000000, 0.000000, 0.000000], [0.000000, 1.000000, 0.000000, 0.000000], [0.000000, 0.000000, 1.000000, 0.000000], [0.000000, 0.000000, 0.000000, 1.000000]])

#scene.removeUselessInstances(1)
algo.deleteFreeVertices([1])
algo.deleteLines([1])
_ret_ = scene.cleanUnusedMaterials(True)

scene.renameLongOccurrenceName(128)
scene.mergeMaterials()
scene.mergeImages()
material.makeMaterialNamesUnique()
scene.deleteEmptyOccurrences()

algo.repairCAD([1], 10.000000, False)
algo.tessellateRelativelyToAABB([1], 0.200000, 0.000300, -1, -1, True, 0, 1, 0.000000, False, False, True, False)
algo.createInstancesBySimilarity([1], 0.950000, 0.500000, True, True, True)

