
scene.compress()
scene.mergeByTreeLevel([scene.getRoot()],1)


occ = scene.getSelectedOccurrences()
RVT_name = core.getProperties(occ, "Name")
filePath = 'E:/Wk_UnrealEngine_Library/Model_opt/' + RVT_name[0] + '.fbx'
io.exportSelection(filePath, False)




	
	
	



