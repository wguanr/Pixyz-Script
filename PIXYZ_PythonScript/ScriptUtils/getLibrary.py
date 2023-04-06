from enum import Enum
from pxz import *


useless_occurrences = scene.getFilteredOccurrences(
    "(Property(\"Name\").Matches(\"^.*dwg.*$\")) OR (Property(\"Name\").Matches(\"^.*图纸.*$\"))"
    )
merged_occurrences = scene.getFilteredOccurrences(
    "(Property(\"Name\").Matches(\"^.*Stairs.*$\") OR (Property(\"Name\").Matches(\"^.*Railings.*$\") OR (Property(\"Name\").Matches(\"^.*Floors.*$\") OR Property(\"Name\").Matches(\"^.*Walls.*$\") )))"
    )

print(useless_occurrences)
print(merged_occurrences)

class LOD_set(Enum):
    LOD0 = 'Origin' # for mark 
    LOD1 = 'Proxy' # special workflow
    LOD2 = 'Simplified'
    LOD3 = 'Detailed'
    LOD4 = 'HighDetailed'
    LOD5 = 'Nanite'


def target_occurrences():
    selected_occurrences = scene.getSelectedOccurrences()
    if not selected_occurrences:
        is_selected = False
        tar_occurrences = scene.getRoot()
    else:
        is_selected = True
        tar_occurrences = selected_occurrences
    return tar_occurrences


def model_factor(lod: LOD_set, PrecisionFactor: float = 1.):
    if lod:
        # origin = nothing
        model_PrecisionFactor = {
            'Proxy': 50.0,
            'Simplified': 10.0,
            'Detailed': 5.0,
            'HighDetailed': 0.2,
            'Nanite': 1.0
        }
        return model_PrecisionFactor.get(lod.value, 0)
    else:
        return PrecisionFactor


def set_model_preset(lod:LOD_set):
    pass

def instacing():
    algo.selectSimilar(occurrences, 0.98, 0.98, False)