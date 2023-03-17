sel_occs = scene.getSelectedOccurrences()
scene.mergePartsByMaterials(sel_occs)
scene.compress()
scene.deleteEmptyOccurrences()