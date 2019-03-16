import os
import sys


def listdir(folder, indent):
    os.chdir(folder)
    files = filter(os.path.isdir, os.listdir(folder))
    indentation = ""
    for i in range(0, indent):
        indentation = indentation + " "
    for f in files:
        line = indentation + f
        print line
        listdir(folder+'/'+f, indent+2)

if __name__ == '__main__':
    topfolder = os.getcwd()
    if len(sys.argv) > 1:
        topfolder = sys.argv[1]
    listdir(topfolder, 0)
