import os
import time
import sys

def convertFile(inputFile, outputFolder, extensions, optimization):
	
	fileName = getFileNameWithoutExtension(inputFile)
	
	# Set log file in output folder for debug purposes (otherwise it will be overwritten by next 3d file processing)
	core.setLogFile(outputFolder + '/' + fileName + '.log')

	# Imports and prepares the input_files using the automatic "Guided import" process (see documentation)
	roots = process.guidedImport([inputFile], pxz.process.CoordinateSystemOptions(["automaticOrientation",0], ["automaticScale",0], False, True), ["usePreset",2], pxz.process.ImportOptions(False, True, True), False, False, False, False, False, False)

	if optimization:# Comment or delete the lines not necessary to your workflow, adjust parameters' values if necessary
		
		t0, n_triangles, n_vertices, n_parts = getStats(roots[0])

		# Automatically selects and deletes parts in the scene, whose size is lower than a maximum size defined in by the parameter Size (in millimeters)
		SIZE = 20
		scene.selectByMaximumSize(roots, SIZE, -1, False)
		scene.deleteSelection()
		
		# Removes through holes from CAD models whose diameter is below the defined diameter
		DIAMETER = 10
		algo.removeHoles(roots, True, False, False, DIAMETER, 0)
		
		# Deletes patches borders (black lines delimiting CAD models' faces) to allow decimation (run in the next step) to be more efficient. Otherwise, patches borders are considered as important information to preserve.
		algo.deletePatches(roots, True)
		
		# Reduces meshes density (triangles count) by decimating them, using the "Decimate To Quality" function (see documentation). The values used here are meant to decimate meshes just enough to lower the triangles count without affecting the visual quality too much, especially on CAD models.
		algo.decimate(roots, 1, 0.1, 3, -1, False)
		
		# Removes triangles not visible from a set of cameras automatically placed around the model.
		algo.hiddenRemoval(roots, 2, 1024, 16, 90, False, 1)

		t1, _n_triangles, _n_vertices, _n_parts = getStats(roots[0])

	# Export files
	for extension in extensions:
		io.exportScene(outputFolder + '/' + fileName + extension)
	
	if optimization:
		printStats(fileName, t1 - t0, n_triangles, _n_triangles, n_vertices, _n_vertices, n_parts, _n_parts)


def getFileNameWithoutExtension(file):
	return os.path.splitext(os.path.basename(file))[0]

def getStats(root):
	core.configureInterfaceLogger(False, False, False) # hide next lines from logs
	
	t = time.time()
	n_triangles = scene.getPolygonCount([root], True, False, False)
	n_vertices = scene.getVertexCount([root], False, False, False)
	n_parts = len(scene.getPartOccurrences(root))

	core.configureInterfaceLogger(True, True, True) # reenable logs

	return t, n_triangles, n_vertices, n_parts

def printStats(fileName, t, n_triangles, _n_triangles, n_vertices, _n_vertices, n_parts, _n_parts):
	print('\n')
	print('{:<20s}{:<3s}\n'.format('file ', fileName))
	print('{:<20s}{:<8.3f}{:<3s}\n'.format('optimization ', t, ' s'))
	print('{:<20s}{:<3s}\n'.format('triangles ', str(n_triangles) + ' -> ' + str(_n_triangles)))
	print('{:<20s}{:<3s}\n'.format('vertices ', str(n_vertices) + ' -> ' + str(_n_vertices)))
	print('{:<20s}{:<3s}\n'.format('parts ', str(n_parts) + ' -> ' + str(_n_parts)))

# Get arguments passed in command line and call main function
if __name__ == "__main__":
	convertFile(sys.argv[1], sys.argv[2], eval(sys.argv[3]), eval(sys.argv[4]))
