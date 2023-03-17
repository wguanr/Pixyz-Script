import sys
import json
import os
from watcher import Watcher

config_file = sys.argv[1]

with open(config_file) as config:
    inputs = json.load(config)

    # Get arguments from config json file
    input_folder = inputs['input_folder']
    # convert relative path to absolute path (if needed)
    input_folder = os.path.abspath(input_folder) 
    output_folder = inputs['output_folder'] 
     # convert relative path to absolute path
    output_folder = os.path.abspath(output_folder)
    extensions = inputs['extensions']
    quality = inputs['quality']

    print('\n')
    print('Input folder: %s\n' % input_folder)
    print('Output folder: %s\n' % output_folder)
    print('Extensions: %s\n' % ' '.join(extensions))
    print('Quality: %s\n' % quality)

    Watcher(input_folder, output_folder, extensions, quality)

