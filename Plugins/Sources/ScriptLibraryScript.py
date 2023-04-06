

def ScriptLibrary():
	#TODO add your code here.
	# 这里是需要执行的程序代码
	pass
	
'''
class special_operations:
	algo.smartHiddenRemoval([1], 0, 100, 1, 256, 0, False, 1)
	algo.combineMeshes([1], pxz.algo.BakeOption(0, 2048, 1, pxz.algo.BakeMaps(True, False, False, False, True, False, False)), True)

'''

class gets:
	RVT_deleted_expr = "(Property(\"Name\").Matches(\"^.*dwg.*$\")) OR (Property(\"Name\").Matches(\"^.*Text.*$\")) OR (Property(\"Name\").Matches(\"^.*图纸.*$\"))"
	RVT_merged_expr = "(Property(\"Name\").Matches(\"^.*梁.*$\") OR (Property(\"Name\").Matches(\"^.*Stairs.*$\") OR (Property(\"Name\").Matches(\"^.*Curtain.*$\") OR (Property(\"Name\").Matches(\"^.*Site.*$\") OR (Property(\"Name\").Matches(\"^.*Railings.*$\") OR (Property(\"Name\").Matches(\"^.*Floors.*$\") OR Property(\"Name\").Matches(\"^.*Walls.*$\")))))))"
	RVT_merged = scene.getFilteredOccurrences(RVT_merged_expr)
	"(Component(\"Metadata\").Property(\"Other/Category\") AND Component(\"Metadata\").Property(\"Other/Category\").Matches(\"^$\"))"
	#映射关系
	Category = "Other/Category"
	# wall = scene.findByMetadata(Category, "^.*Wall.*", occs_root)
	RVT_ElementsList_One = ['Wall','Floor','Rail','Site','Pipes','Pipe Fitting','Cable Tray','Ducts','Duct Fitting']
	RVT_ElementsList_ISM = ['Window','Door','Equipment','Structural Column','Structural Framing','Sprinkler','Accessories','Curtain','Air Terminals']
	

#

def Revit_Process(ImportFiles, OutputFile):
	core.resetSession()
	 
#	if len(ImportFiles) > 20 and core.askYesNo("前方高能预警，导入大量模型，继续？"):
#		print("前方高能预警，导入大量模型")
#		Import_Task(ImportFiles)
	for filepath in ImportFiles:
		# FileName = scene.evaluateExpressionOnOccurrences(scene.getSelectedOccurrences(), 'Property("Name")')
		FileName = filepath.split("/")[-1]
		RVTcode = FileName.split("_")[2]
		print(f"开始处理模型{FileName}，类型为 {RVTcode}")
		occs_root = process.guidedImport([filepath], pxz.process.CoordinateSystemOptions(["automaticOrientation",0], ["automaticScale",0], False, False), ["usePreset",2], pxz.process.ImportOptions(False, True, True), False, False, False, False, False, False)
			#cleaning
		clean()
		clean_filtered_occurrences(gets.RVT_deleted_expr)
			# merging operations 
		scene.mergePartsByAssemblies([1], 2)
			# create occs
		elmts = gets.RVT_ElementsList_ISM + gets.RVT_ElementsList_One
			#deal with elements
		_count = 0
		for i in elmts:
			_count = _count+1
			_rex = '^.*' + i + '.*'
			_ism = scene.findByMetadata(gets.Category, _rex, occs_root)
			_occ = scene.createOccurrenceFromSelection(i, _ism, occs_root[0], True)
			if _ism and _count > len(gets.RVT_ElementsList_ISM) :
				print(f'{_count} > {len(gets.RVT_ElementsList_ISM)}---- debug' )
				scene.mergeParts([_occ], 2)
			#deal with generic models
			#optmiazations begin
		if RVTcode in ["S","GL"]:
			repairing(3)
			decimating(occs_root,2)
		if RVTcode in ["M","A","SS","E"]:	
				#SS为钢结构
				#optimaze
			repairing(2)
			decimating(occs_root,2)
			
		if RVTcode in ["P"]:
			print()
				#optimaze
			decimating(occs_root,1)
			
	clean()
	final_optimize()
	if OutputFile == "":
		print("==========Debugging=============")
	else:
		io.exportScene(OutputFile)
	
