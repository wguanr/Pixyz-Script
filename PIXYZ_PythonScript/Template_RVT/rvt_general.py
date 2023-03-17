useless_occs_filter =  "(Property(\"Name\").Matches(\"^.*dwg.*$\"))"
max_Occurrence_Name = 64
selOccs = scene.getSelectedOccurrences()
merged_occs_filter = "(Property(\"Name\").Matches(\"^.*Stairs.*$\") OR (Property(\"Name\").Matches(\"^.*Railings.*$\") OR (Property(\"Name\").Matches(\"^.*Floors.*$\") OR Property(\"Name\").Matches(\"^.*Walls.*$\") )))"

filteredOccurrences = scene.getFilteredOccurrences(merged_occs_filter)
deletedOccurrences = scene.getFilteredOccurrences(useless_occs_filter)
core.deleteEntities(deletedOccurrences)

#Presets
scene.resetTransform(1, True, True, False)
scene.renameLongOccurrenceName(max_Occurrence_Name)

#Merge
scene.mergePartsByAssemblies([1], 2)
for occ in filteredOccurrences:
	scene.mergeParts([occ],0)
	
scene.mergeByTreeLevel([1], 6, 2)
#post 
scene.deleteEmptyOccurrences()