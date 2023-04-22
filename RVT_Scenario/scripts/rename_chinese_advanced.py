
import os
import re
from xpinyin import Pinyin


def main(target_dir):
    # get a list of all files and directories in the target directory
    for root, dirs, files in os.walk(target_dir):
        # print the current root directory
        print(f"Current directory: {root}")
        # print all subdirectories in the current root directory
        print(f"Subdirectories: {dirs}")
        # print all files in the current root directory
        print(f"Files: {files}")
        # iterate through all directories
        for dir in dirs:
            # check if the directory name contains any Chinese characters
            if re.search('[\u4e00-\u9fff]', dir):
                # convert the Chinese characters to pinyin
                p = Pinyin()
                new_dir_name = p.get_pinyin(dir, '')
                # rename the directory
                os.rename(os.path.join(root, dir),
                          os.path.join(root, new_dir_name))
        # iterate through all files
        for file in files:
            # check if the file name contains any Chinese characters
            if re.search('[\u4e00-\u9fff]', file):
                # convert the Chinese characters to pinyin
                p = Pinyin()
                new_file_name = p.get_pinyin(os.path.splitext(file)[0], '')
                # add original file extensions to new_file_name
                new_file_name += os.path.splitext(file)[1]
                # rename the file
                os.rename(os.path.join(root, file),
                          os.path.join(root, new_file_name))


if __name__ == '__main__':
    for i in range(5):
        main(r'F:\PCG\pixyz\RVT_Scenario\_input')
