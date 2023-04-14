import json
import fileutils


def main():
    # read input parameters from config.json file
    with open('config.json') as config:
        inputs = json.load(config)
        input_folder    = inputs['input_folder']
        output_folder     = inputs['output_folder'] 

    files_to_import = fileutils.get_files(input_folder, fileutils.get_import_extensions())
    
    if len(files_to_import) == 0: 
        print('No files to import. Closing.')
        return   
    #测试
    # 
    io.importFiles(files_to_import)
    
    scene.mergeByTreeLevel([scene.getRoot()], 2)
    scene.selectAllPartOccurrences()
    #occs = [scene.selectAllPartOccurrences()]
    occs = [scene.getSelectedOccurrences()]

    #print(scene.getNodeName(occurrences))
    scene.unselect(occs)

    for occ in occs:
        
        output_file = output_folder + '/'+ scene.getNodeName(occ)  +'.fbx'
        io.exportSelection(output_file, False)

        #files_to_outport = fileutils.get_files(output_folder, extensions='.fbx')
        #
        #optimize(scene.getRoot())
        
        

def optimize(root):
    # if meshes are present, process them first
    algo.repairMesh([root], 0.100000, True, False)
    algo.decimate([root], 1.0, -1, 8.0, -1, False)

    # then process CAD (mesh generation)
    algo.repairCAD([root], 0.1, False)
    algo.tessellate([root], 0.2, -1, -1, True, 0, 1, 0, False, False, False, False)

if __name__ == "__main__":
    # execute only if run as a script
    main()