import numpy as np

import struct

def convert(imglist, path=None, name=None):
    if path is None:
        path = ""
    else:
        path = f"{path}\\"
    form = 'uint8'
        
    ds = imglist[0]
    ds.InstitutionAddress = ds.InstitutionAddress if ("InstitutionAddress" in ds) else 'Unknown'
    if name:
        pass
    else:
        name = ds.SeriesDescription.replace(" ", "")
    #print(f"{ds = }")
    with open(f"{path}\\{name}.txt", "w") as ftxt:
        ftxt.write(f"{ds.PatientName}\n"
                   f"{ds.PatientID}\n"
                   f"{ds.PatientBirthDate}\n"
                   f"{ds.PatientSex}\n"
                   f"{ds.InstitutionName}\n"
                   f"{ds.InstitutionAddress}\n"
                   f"{ds.ReferringPhysicianName}\n"
                   f"{ds.StudyDescription}\n"
                   f"{ds.Modality}\n"
                   f"{ds.Manufacturer}\n"
                   f"{ds.StudyID}\n"
                   f"{ds.StudyDate}\n"
                   f"{ds.SeriesNumber}\n"
                   f"{ds.PixelSpacing[0]}\n"
                   f"{ds.PixelSpacing[1]}\n"
                   f"{ds.SliceThickness}\n"
                   f"{ds.Columns}\n"
                   f"{ds.Rows}\n"
                   f"{ds.ImagePositionPatient[0]}\n"
                   f"{ds.ImagePositionPatient[1]}\n"
                   f"{ds.ImagePositionPatient[2]}\n"
                   f"{ds.ImageOrientationPatient[0]}\n"
                   f"{ds.ImageOrientationPatient[1]}\n"
                   f"{ds.ImageOrientationPatient[2]}\n"
                   f"{ds.ImageOrientationPatient[3]}\n"
                   f"{ds.ImageOrientationPatient[4]}\n"
                   f"{ds.ImageOrientationPatient[5]}\n")

    with open(f"{path}\\{name}.ini", "w") as fini:
        fini.write(f"dimx:{ds.Columns}\n"
                   f"dimy:{ds.Rows}\n"
                   f"dimz:{len(imglist)}\n"
                   f"skip:0\n"
                   f"format:{form}")

    pixellst = []
    for i in imglist:
        pixellst.append(i.pixel_array)
    cube = np.asarray(pixellst)
    cube = cube*(255/cube.max())
    cube = cube.astype("uint8")
    cube = cube[::-1, :, ::-1]
    #cube = cube[::2, ::2, ::2]
    '''array = cube.flatten()
    #array = array[::-1]
    print(array.dtype)
    with open(f"{path}\\{name}.raw", "wb") as fini:
        for i in range(3):
            fini.write(struct.pack('>I', cube.shape[i]))
        fini.write(struct.pack('>I', 0))
        for i in range(3):
            fini.write(struct.pack('>f', 1))
        for i in array:
            fini.write(struct.pack('>B', i))'''
    cube.astype(form).tofile(f"{path}\\{name}.raw")
