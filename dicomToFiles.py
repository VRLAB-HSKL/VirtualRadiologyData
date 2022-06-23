import numpy as np


def convert(imglist, name=None):
    form = 'uint16'

    ds = imglist[0]
    if name:
        pass
    else:
        name = ds.SeriesDescription.replace(" ", "")
    print(f"{ds = }")
    with open(f"{name}.txt", "w") as ftxt:
        ftxt.write(f"{ds.PatientName}\n"
                   f"{ds.PatientID}\n"
                   f"{ds.PatientBirthDate}\n"
                   f"{ds.PatientSex}\n"
                   f"{ds.InstitutionName}\n"
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

    with open(f"{name}.ini", "w") as fini:
        fini.write(f"dimx:{ds.Columns}\n"
                   f"dimy:{ds.Rows}\n"
                   f"dimz:{len(imglist)}\n"
                   f"skip:0\n"
                   f"format:{form}")

    pixellst = []
    for i in imglist:
        pixellst.append(i.pixel_array)
    cube = np.asarray(pixellst)
    cube.astype(form).tofile(f"{name}.raw")
