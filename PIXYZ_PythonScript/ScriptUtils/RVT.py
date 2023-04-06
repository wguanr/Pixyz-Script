import pxz
import sys


import ScriptLibrary as lib
import getLibrary as getlib

# mergedOccs = getlib.merged_occurrences
# deletedOccs = getlib.useless_occurrences
# tarOccs = getlib.target_occurrences()
print("ScriptLibrary已经导入")

cl = lib.clean_bot()
cl.clean_filtered_occurrences()
cl.clean_futher()
cl.optimazing()


ge = lib.geometry_optimization()
ge.decimating()
ge.repairing()





# Merge
# ge.decimate_operation()


'''

fileNames = ['']
coordinateSystem: CoordinateSystemOptions(["automaticOrientation", 0], ["automaticScale", 0], False, False)
tessellation: ["usePreset", process.QualityPreset.Medium]
otherOptions: ImportOptions(False, True, True)
importLines: False
importPoints: False
importHidden: False
importPMI: False
importVariants: False
process.guidedImport(fileNames, coordinateSystem, tessellation, otherOptions, importLines, importPoints, importHidden, importPMI, importVariants, False)

#
def guide_import_opt():
    scene.deleteEmptyAnimation()
    scene.applyTransformation()
    algo.deleteFreeVertices()
    algo.deleteLines()
    
    scene.cleanUnusedMaterials(True)
    scene.mergeMaterials()
    material.makeMaterialNamesUnique()
    scene.deleteEmptyOccurrences

    algo.repairCAD()
    algo.tessellateRelativelyToAABB()
    algo.UVGenerationMode.NoUV
    scene.getDuplicatedParts
    algo.createInstancesBySimilarity
    scene.removeUselessInstances

    algo.repairMesh
    algo.identifyPatches()
    algo.deleteLines
    algo.createNormals
    algo.mapUvOnAABB
    algo.orientNormals
    algo.createTangents
    scene.removeSymmetryMatrices
    
    
'''