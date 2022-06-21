import sys
import pydicom
import numpy as np
from os import listdir
from os.path import isfile, join

def cgetdirekt(instanceList):
    path = sys.argv[1]
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    for i, val in enumerate(onlyfiles):
        dataset = pydicom.filereader.dcmread(path + '\\' + val)
        ds = pydicom.dataset.Dataset(dataset)
        ds.file_meta = dataset.file_meta
        instanceList.append(dataset)

def imagelist():
    instanceList = []
    cgetdirekt(instanceList)
    return instanceList


imglist = imagelist()
ds = imglist[0]
with open("hip.txt", "w") as ftxt:
    ftxt.write(f"{ds.PatientName}\n"\
               f"{ds.PatientID}\n"\
               f"{ds.PatientBirthDate}\n"\
               f"{ds.PatientSex}\n"\
               f"{ds.InstitutionName}\n"\
               f"{ds.ReferringPhysicianName}\n"\
               f"{ds.StudyDescription}\n"\
               f"{ds.Modality}\n"\
               f"{ds.Manufacturer}\n"\
               f"{ds.StudyID}\n"\
               f"{ds.StudyDate}\n"\
               f"{ds.SeriesNumber}\n"\
               f"{ds.PixelSpacing[0]}\n"\
               f"{ds.PixelSpacing[1]}\n"\
               f"{ds.SliceThickness}\n"\
               f"{ds.Columns}\n"\
               f"{ds.Rows}\n"\
               f"{ds.ImagePositionPatient[0]}\n"\
               f"{ds.ImagePositionPatient[1]}\n"\
               f"{ds.ImagePositionPatient[2]}\n"\
               f"{ds.ImageOrientationPatient[0]}\n"\
               f"{ds.ImageOrientationPatient[1]}\n"\
               f"{ds.ImageOrientationPatient[2]}\n"\
               f"{ds.ImageOrientationPatient[3]}\n"\
               f"{ds.ImageOrientationPatient[4]}\n"\
               f"{ds.ImageOrientationPatient[5]}\n")

with open("hip.ini", "w") as fini:
    fini.write(f"dimx:{ds.Columns}\n"\
               f"dimy:{ds.Rows}\n"\
               f"dimz:{len(imglist)}\n"\
               f"skip:0\n"\
               f"format:uint8\n")

pixellst = []
for i in imglist:
    pixellst.append(i.pixel_array)
cube = np.asarray(pixellst)
cube.astype('uint8').tofile("hip.raw")


