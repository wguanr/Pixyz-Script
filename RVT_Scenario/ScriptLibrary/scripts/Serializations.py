import json
import os
import pathlib as phb


####
# PropertyInfoList = core.listProperties(entity)
# core.getProperties(entities, "propertyName", "")
# core.hasProperty(entity, "propertyName")
# core.setProperty(entity, "propertyName", "propertyValue")
# core.supportCustomProperties(entity)
# scene.addMetadata(metadata, "name", "value")
# scene.addMetadataBlock(metadata, names, values)
###

def StandardSerialization(output_folder):
	# prepare
	# make_unique_name, 为每一个Nodename添加ID
	# 将JSON字符串写入文件
	output_folder = phb.Path(output_folder)
	JSON_path = output_folder / 'Local_Metadata'
	if not JSON_path.exists():
		JSON_path.mkdir()
	# scene.hasComponent(occurrence, 5, False)

	removeAllVerbose()
	target_occs = []
	for occ in scene.getPartOccurrences(1):
		occ_parent = scene.getParent(occ)
		MetadataKey = 'UNIQUE_ID'
		Metadata_Comps = scene.getComponentByOccurrence([occ_parent], 5, True)
		MetadataValue = scene.getMetadata(Metadata_Comps[0], MetadataKey)
		core.setProperty(occ, "Name", MetadataValue)
		target_occs.append(occ_parent)
	serializeMetadataToJSON(target_occs, JSON_path, False)

	addAllVerbose()
	print('**************\n', 'serializeMetadataToJSON\n', '**************')
	# add more metadata
	removeAllVerbose()
	building_stories = scene.findByMetadata("TYPE", "IFCBUILDINGSTOREY", [])
	serializeMetadataToJSON(building_stories, JSON_path, True)
	addAllVerbose()
	print('+++++++++++++\n','serializeMetadataToJSON', '\n+++++++++++++')


# 在Pixyz的环境下执行
# 递归查找每一个Occurrence，然后将其Metadata写入JSON文件
def serializeMetadataToJSON(Occurrences, JSON_dir, json_add_mode):
	print('**************')
	print('serializeMetadataToJSON Begin')
	print('**************')

	json_data = []
	for Target_Occurrence in Occurrences:
		if not scene.hasComponent(Target_Occurrence, 5, True):
			continue
		print('Current_Occurrences is ', scene.getNodeName(Target_Occurrence))
		Metadata_Comp = scene.getComponentByOccurrence([Target_Occurrence], 5, True)
		Metadata_Defis = scene.getMetadatasDefinitions(Metadata_Comp)

		json_data_metadata = {}
		NodeName = scene.getNodeName(Target_Occurrence)
		for Metadata_KeyValue in Metadata_Defis:
			if not Metadata_KeyValue:
				continue
			json_data_metadata.update({Metadata.name: Metadata.value for Metadata in Metadata_KeyValue})

		json_data.append(
			{
				'NodeName': NodeName,
				**json_data_metadata
				})

	json_data = list(json_data)  # 将集合转换为列表

	JSON_path = os.path.join(JSON_dir, 'Metadata.json')
	if not json_add_mode:

		json_str = json.dumps(json_data, ensure_ascii=False, indent=4)
		with open(JSON_path, 'w', encoding='utf-8') as f:
			f.write(json_str)
			f.write('\n')

		# close file
		f.close()
		return f
	else:
		# 读取已有的JSON文件,并且添加新的数据
		with open(JSON_path, 'r', encoding='utf-8') as f:
			json_data_old = json.load(f)
			json_data_old.extend(json_data)
			json_data_old = list(json_data_old)
			json_str = json.dumps(json_data_old, ensure_ascii=False, indent=4)
			# print(json_str)
			with open(JSON_path, 'w', encoding='utf-8') as f:
				f.write(json_str)
				f.write('\n')
			# close file
			f.close()

		return f




def export_all_metadata_to_json_str():
	json_data = []
	Metadata_Comps = scene.listComponent(5)
	for Metadata_Comp in Metadata_Comps:
		Metadata_Defis = scene.getMetadatasDefinitions([Metadata_Comp])

		json_data_metadata = {}
		for Metadata_KeyValue in Metadata_Defis:
			if not Metadata_KeyValue:
				continue
			json_data_metadata.update({Metadata.name: Metadata.value for Metadata in Metadata_KeyValue})

		json_data.append(
			{
				**json_data_metadata
				})

	json_data = list(json_data)
	json_str = json.dumps(json_data, ensure_ascii=False, indent=4)

	return json_str


def removeAllVerbose():
	core.removeConsoleVerbose(2)
	core.removeLogFileVerbose(2)
	core.removeLogFileVerbose(5)
	core.removeSessionLogFileVerbose(2)


def addAllVerbose():
	core.addLogFileVerbose(2)
	core.addSessionLogFileVerbose(2)
	core.addConsoleVerbose(2)
