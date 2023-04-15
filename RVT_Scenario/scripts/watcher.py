import sys
import json
import os
import subprocess
from ctypes import windll


def main(config_file):
    printLogo()
    input_folder, output_folder, extensions = read_config(config_file)

    waiting = False

    while 1:
        input_files = [file for file in os.listdir(input_folder)
                       if (os.path.isfile(input_folder + '/' + file)
                           and os.path.splitext(file)[1] not in ['.xml', ''])]

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

        # input_folder, output_folder, extensions, ExportName
        execute_Revit_Process(input_folder, output_folder, extensions=extensions, export_name='DefaultOutput')

        # os.remove(input_folder + '/' + input_files[0])
        print('Done')


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

    print('\n')
    print('Input folder: %s\n' % input_folder)
    print('Output folder: %s\n' % output_folder)
    print('Extensions: %s\n' % ' '.join(extensions))
    print('\n')

    return input_folder, output_folder, extensions


def isCopyFinished(inputFile):
    """
    Check if the file that was dropped in the input folder has finished being copied
    """
    GENERIC_WRITE = 1 << 30
    FILE_SHARE_READ = 0x00000001
    OPEN_EXISTING = 3
    FILE_ATTRIBUTE_NORMAL = 0x80
    handle = windll.Kernel32.CreateFileW(inputFile, GENERIC_WRITE, FILE_SHARE_READ, None, OPEN_EXISTING,
                                         FILE_ATTRIBUTE_NORMAL, None)
    if handle != -1:
        windll.Kernel32.CloseHandle(handle)
        return True
    return False


def getFileExtension(file):
    return os.path.splitext(file)[1]


def execute_Revit_Process(input_folder, output_folder, export_name, extensions):
    args = ['C:\Program Files\PiXYZScenarioProcessor\PiXYZScenarioProcessor.exe', 'ScriptLibrary', 'Revit_Process',
            "\"" + input_folder.replace("\\", "\\\\") + "\"", "\"" + output_folder.replace("\\", "\\\\") + "\"",
            "\"" + export_name + "\"", str(extensions)]
    p = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    while p.poll() is None:
        l = str(p.stdout.readline().rstrip())  # This blocks until it receives a newline.
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
