import sys, getopt
import pydicom
import numpy as np
from os import listdir
from os.path import isfile, join

import dicomToFiles


def loadFieles(instanceList, path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for i, val in enumerate(onlyfiles):
        dataset = pydicom.filereader.dcmread(path + '\\' + val)
        ds = pydicom.dataset.Dataset(dataset)
        ds.file_meta = dataset.file_meta
        instanceList.append(dataset)

def imagelist(path):
    instanceList = []
    loadFieles(instanceList, path)
    return instanceList

def main(argv):
    name = ''
    path = ''
    try:
        opts, args = getopt.getopt(argv, "hn:p:", )
    except getopt.GetoptError:
        print
        'dicomToRaw -n <nameOfOutput> -p <pathToDirectory>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print
            'dicomToRaw -n <nameOfOutput> -p <pathToDirectory>'
            sys.exit()
        elif opt in ("-n"):
            name = arg
        elif opt in ("-p"):
            path = arg

    imglist = imagelist(path)
    dicomToFiles.convert(imglist, name=name)

if __name__ == "__main__":
   main(sys.argv[1:])