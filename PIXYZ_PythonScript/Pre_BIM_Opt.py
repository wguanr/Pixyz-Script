
scene.mergeImages()
scene.mergeMaterials()
scene.cleanUnusedImages()
scene.cleanUnusedMaterials()
scene.deleteEmptyOccurrences()
scene.mergeByTreeLevel([1], 6, 2)


algo.deleteFreeVertices([1])
algo.deleteLines([1])

#algo.remeshSurfacicHoles([1], 100.000000)
algo.tessellate([1], 5.000000, -1, -1, True, 0, 1, 0.000000, False, False, True, True)

algo.repairCAD([1], 10.000000, True)
algo.repairMesh([1], 10.000000, True, True)

#scene.deleteEmptyOccurrences()
#scene.removeUselessInstances()
