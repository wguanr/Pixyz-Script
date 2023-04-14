import sys
import json
import os
import subprocess
from ctypes import windll

def main(config_file):
    printLogo()
    input_folder, output_folder, extensions, optimization = read_config(config_file)

    waiting = False

    while(1):
        input_files = [file for file in os.listdir(input_folder)\
                        if (os.path.isfile(input_folder + '/' + file)\
                        and getFileExtension(file) not in ['.xml', ''])]

        if len(input_files) == 0:
            if not waiting:
                print('\n')
                print('Waiting for files to process...\n')
                waiting = True
            continue
        elif not isCopyFinished(input_folder + '/' + input_files[0]):
            continue
        else:
            waiting = False

        input_file = input_folder + '/' + input_files[0]
        executeScenarioProcessor(input_file, output_folder, extensions, optimization)

        os.remove(input_file) # remove when finishing processing

def read_config(config_file):

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
    optimization = inputs['optimization']

    print('\n')
    print('Input folder: %s\n' % input_folder)
    print('Output folder: %s\n' % output_folder)
    print('Extensions: %s\n' % ' '.join(extensions))
    print('Optimization: %s\n' % optimization)

    return input_folder, output_folder, extensions, optimization

def isCopyFinished(inputFile):
    """
    Check if the file that was dropped in the input folder has finished being copied
    """
    GENERIC_WRITE         = 1 << 30
    FILE_SHARE_READ       = 0x00000001
    OPEN_EXISTING         = 3
    FILE_ATTRIBUTE_NORMAL = 0x80
    handle = windll.Kernel32.CreateFileW(inputFile, GENERIC_WRITE, FILE_SHARE_READ, None, OPEN_EXISTING,\
            FILE_ATTRIBUTE_NORMAL, None)
    if handle != -1:
        windll.Kernel32.CloseHandle(handle)
        return True
    return False

def getFileExtension(file):
    return os.path.splitext(file)[1]

def executeScenarioProcessor(input_file, output_folder, extensions, optimization):
    args = ['C:\Program Files\PiXYZScenarioProcessor\PiXYZScenarioProcessor.exe', 'scripts/sampleScript.py', input_file, output_folder, str(extensions), str(optimization)]
    print(sys.argv[0])
    print(args)
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    while p.poll() is None:
        l = str(p.stdout.readline().rstrip()) # This blocks until it receives a newline.
        print(l)
    print(p.stdout.read())

def printLogo():
    print('')
    print("     #######                %######     ")
    print("  ##############        &#############& ")
    print("######      ######    ######      &#####")
    print("####          &###########          ####")
    print("####%            ######             ####")
    print(" #####&       &###### ####        #####%")
    print("   ######   ######    ######   &######  ")
    print("     ######& ###        &##########     ")
    print("       #######             ######       ")
    print("    &###########&       #### &######    ")
    print("  ######     ######  &######    ######& ")
    print(" #####         ##% ######         &####%")
    print("####%           %#######            ####")
    print("####%         ############&         ####")
    print(" #####&    %#####%     ######%    #####%")
    print("   ############          #############  ")
    print("     #######                %######     ")


if __name__ == "__main__":
    main(sys.argv[1])