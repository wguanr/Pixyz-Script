import pxz


def clean1():
    #scene.removeUselessInstances(1)
    algo.deleteFreeVertices([1])
    algo.deleteLines([1])

class preset:
    def target_occurrences():
        selected_occurrences = scene.getSelectedOccurrences()
        if not selected_occurrences:
            is_selected = False
            target_occurrences = scene.getRoot()
        else:
            is_selected = True
            target_occurrences = selected_occurrences
        return target_occurrences        

class clean_bot:
    def __init__(self):
        self._occ = preset.target_occurrences()
        self.max_Occurrence_Name = 64
        self.is_instance_reset = False #保留Instances的Transform
    
    def clean(self):
        print("正在清理"+str(self._occ))
        scene.cleanUnusedMaterials(True)
        scene.deleteEmptyOccurrences()
        scene.renameLongOccurrenceName(self.max_Occurrence_Name)
        scene.removeUselessInstances(self._occ)
        scene.resetTransform(1, True, not self.is_instance_reset, False)

    def clean_by_filter(self,filter):
        pass
    
class geometry_optimazation:
    def __init__(self):
        self._occ = preset.target_occurrences()
    def decimate_operation():
        algo.decimateTarget(self._occ, ["ratio",80.000000], 0, False, 5000000)

        algo.repairCAD([1], 10.000000, False)
        algo.tessellateRelativelyToAABB([1], 0.200000, 0.000300, -1, -1, True, 0, 1, 0.000000, False, False, True, False)



class material_operation:
    def __init__(self):
        scene.cleanUnusedMaterials()
    def material_replace(origin_materials,new_material):
        #使用Filter
        for mat in origin_materials:
            scene.replaceMaterial(mat, new_material, [1])
	
    



def main():
    # 这里是需要执行的程序代码
    print("Lib已经导入")
    bot = clean_bot()
    bot.clean()



if __name__ == '__main__':
    main()