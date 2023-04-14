"""
DEMO - BATCH SAMPLE
This demo demonstrates how to use PiXYZ Batch to watch a directory for changes (Watcher class). Each time a new file 
appear in the input directory, it is processed, optimised, and exported to an output folder (BatchFile class).
"""

import os
import sys
import time
from ctypes import windll
import pxz

try:# Prevent IDE errors
	from pxz import io
	from pxz import algo
	from pxz import scene
	from pxz import core
	from pxz import generateproxy
except: pass


class Watcher:
	"""
	This class handles the input folder listnening.
	"""
	def __init__(self, input_folder : str, output_folder : str, extensions : list, quality : str):
		self.input_folder = input_folder
		self.output_folder = output_folder if output_folder.endswith('/') else output_folder + '/'
		self.extensions = extensions
		self.quality = quality

		self.watch()

	def watch(self):
		waiting = False
		while(1):
			input_files = [file for file in os.listdir(self.input_folder)\
						   if (os.path.isfile(self.input_folder + '/' + file)\
						   and self.getFileExtension(file) not in ['.xml', ''])]

			if len(input_files) == 0:
				if not waiting:
					print('\n')
					print('Waiting for files to process...\n')
					waiting = True
				continue
			elif not self.isCopyFinished(self.input_folder + '/' + input_files[0]):
				continue
			else:
				waiting = False

			input_file = self.input_folder + '/' + input_files[0]
			BatchFile(input_file, self.output_folder, self.extensions, self.quality)
			os.remove(input_file)
	
	def isCopyFinished(self, inputFile):
		GENERIC_WRITE         = 1 << 30
		FILE_SHARE_READ       = 0x00000001
		OPEN_EXISTING         = 3
		FILE_ATTRIBUTE_NORMAL = 0x80
		handle = windll.Kernel32.CreateFileW(inputFile, GENERIC_WRITE, FILE_SHARE_READ, None, OPEN_EXISTING,\
				FILE_ATTRIBUTE_NORMAL, None)
		if handle != -1:
			windll.Kernel32.CloseHandle(handle)
			return True
		return False

	def getFileExtension(self, file):
		return os.path.splitext(file)[1]


class BatchFile:
	"""
	Import, process, and export an input file to an output folder.
	"""
	def __init__(self, input_file : str, output_folder : str, extensions : list, quality : str):
		
		self.input_file = input_file
		self.output_folder = output_folder
		self.extensions = extensions
		self.quality = quality

		self.run()

	def run(self):
		root = io.importScene(self.input_file)

		n_triangles = scene.getPolygonCount([root], True, False, False)
		n_vertices = scene.getVertexCount([root], False, False, False)
		n_parts = len(scene.getPartOccurrences(root))

		print('\n')
		print('Data preparation and optimization...\n')
		removeAllVerbose()

		t_1 = time.time()
		root = self.runPixyzProcess(root, self.quality)
		process_time = time.time() - t_1
		
		_n_triangles = scene.getPolygonCount([root], True, False, False)
		_n_vertices = scene.getVertexCount([root], False, False, False)
		_n_parts = len(scene.getPartOccurrences(root))

		addAllVerbose()

		stats = dict()
		for extension in self.extensions:
			try:
				print('Exporting to: %s\n' % extension)
				t_1 = time.time()
				self.export(root, extension)
				stats[extension] = time.time() - t_1
			except Exception as e:
				print('Failed exporting to %s: %s\n' % (extension, e))
				
		core.resetSession()

		# Log statistics:
		print('\n')
		print('{:<20s}{:<3s}\n'.format('file ', self.input_file))
		print('{:<20s}{:<8.3f}{:<3s}\n'.format('data prep ', process_time, ' s'))
		[print('{:<20s}{:<8.3f}{:<3s}\n'.format(extension[1:] + ' export ', time, ' s')) for extension, time in stats.items()]
		print('{:<20s}{:<3s}\n'.format('triangles ', str(n_triangles) + ' -> ' + str(_n_triangles)))
		print('{:<20s}{:<3s}\n'.format('vertices ', str(n_vertices) + ' -> ' + str(_n_vertices)))
		print('{:<20s}{:<3s}\n'.format('parts ', str(n_parts) + ' -> ' + str(_n_parts)))

	def runPixyzProcess(self, root, quality):
		""" TO BE CUSTOMIZED: Where the PiXYZ magic happens. 
		- RepairCAD before tessellation for a better result
		- Decimate before tessellating (so PiXYZ tessellation is not affected)
		"""
		self.recenterModel(root)

		if quality == "HIGH":
			algo.repairCAD([root], 0.1, False)
			algo.tessellate([root], 0.1, -1, -1, True, 0, 1, 0, False, False, False, False)
			algo.mapUvOnAABB([root], False, 100.0, 0, False)
			return root
		elif quality == "MEDIUM":
			algo.repairCAD([root], 0.1, False)
			algo.decimate([root], 1.0, -1, 8.0, -1, False)
			algo.tessellate([root], 0.2, -1, -1, True, 0, 1, 0, False, False, False, False)
			algo.mapUvOnAABB([root], False, 100, 0, False)
			return root
		elif quality == "LOW":
			algo.tessellate([root], 1, -1, -1, True, 0, 1, 0, False, False, False, False)
			newRoot = generateproxy.proxyFromMeshes(50, ["Yes", pxz.generateproxy.BakeOptions(1024, 1, pxz.generateproxy.BakeMaps(True, True, True, True, True, True, False, False))], True)
			return newRoot

	def recenterModel(self, root):
		"""
		Move the imported model to the origin of the scene based on its bounding box
		"""
		aabb = scene.getAABB([root])
		centerX = (aabb.high.x + aabb.low.x)/2
		centerY = (aabb.high.y + aabb.low.y)/2
		centerZ = (aabb.high.z + aabb.low.z)/2
		translationMatrix = [[1, 0, 0, -centerX],\
							 [0, 1, 0, -centerY],\
							 [0, 0, 1, -centerZ],\
							 [0, 0, 0, 1]]
		scene.applyTransformation(root, translationMatrix)
			
	def export(self, root, extension):
		output_file = self.output_folder + self.getFileNameWithoutExtension(self.input_file) + extension		
		if extension   == '.pxz':
			core.save(self.output_folder + self.getFileNameWithoutExtension(self.input_file))
		elif extension == '.usdz':
			self.exportUSDZ(output_file, root)
		else:
			io.exportScene(output_file, root)

	def exportUSDZ(self, output_file, root):
		""" USDZ format does not handle lot of meshes """
		temp_root = scene.prototypeSubTree(root)
		scene.setParent(temp_root, scene.getRoot())
		scene.mergeParts([temp_root])
		io.exportScene(output_file, temp_root)

	def getFileNameWithoutExtension(self, file):
		return os.path.splitext(os.path.basename(file))[0]

#
def removeAllVerbose():
	core.removeConsoleVerbose(2)
	core.removeLogFileVerbose(2)
	core.removeSessionLogFileVerbose(2)

def addAllVerbose():
	core.addLogFileVerbose(2)
	core.addSessionLogFileVerbose(2)
	core.addConsoleVerbose(2)

		
