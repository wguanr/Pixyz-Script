
# 自动修改文件夹下所有文件的文件名. 文件名=文件夹名+序号
#
import os, time

firstfolder =r"D:\个人信息"


def changename(file):
    # 根据文件名改名. 改成 文件夹名+newname
    if os.path.isfile(file):
        filename = os.path.basename(file).split('.')[0]
        print(filename)
        fileextensions = os.path.basename(file).split('.')[1]
        print(fileextensions )
        filepath = os.path.dirname(file)
        foldername = filepath.split('\\')[-1]
        newfile = filepath + '\\' + foldername + '-' +filename + '.' + fileextensions
        print(newfile)
        try:
            os.rename(file, newfile)
        except FileExistsError:
            pass
    else:
        return False


import os


def getlist(folder):
    # 读取该文件夹下所有的文件路径

    list = []
    if os.path.isdir(folder):
        for row in os.listdir(folder):
            list.append(folder + '\\' + row)
    else:
        pass
    return list



list = []
list=getlist(firstfolder)

for file in list:
    print(file)
    changename(file)
print('done')


