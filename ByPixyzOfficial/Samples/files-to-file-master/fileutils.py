import os
from os import listdir
from os.path import isfile, join
from pxz import io

def get_import_extensions():
    return [extension[1:] for file_format in io.getImportFormats() for extension in file_format.extensions] 

def get_files(folder, extensions=list()):
    # ignore .pxz files
    return [folder + '/' + f for f in listdir(folder) if isfile(join(folder, f)) and os.path.splitext(f)[1] in extensions]
    