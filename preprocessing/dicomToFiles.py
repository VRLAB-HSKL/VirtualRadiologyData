from preprocessing import image, series


def convert(seruid, path=None, name=None):
    
    
    if path is None:
        path = ".\\"
    else:
        path = f"{path}\\"
    encoding = 'uint8'
        
    
    
    imglist = image.Image.images[seruid].imglist
    ds = imglist[0]
     
    ds.InstitutionAddress = ds.InstitutionAddress if ("InstitutionAddress" in ds) else 'Unknown'
    if not name:
        name = series.Series.series[ds.SeriesInstanceUID].getFilename()
       
    cube = image.Image.images[ds.SeriesInstanceUID].volume
    cube = cube.astype("uint8")
    cube = cube[::-1, :, ::-1]
    cube.astype(encoding).tofile(f"{path}{name}.raw")
    
    
    string = f"{ds.PatientName}\n"\
            + f"{ds.PatientID}\n"\
            + f"{ds.PatientBirthDate}\n"\
            + f"{ds.PatientSex}\n"\
            + f"{ds.InstitutionName}\n"\
            + f"{ds.InstitutionAddress}\n"\
            + f"{ds.ReferringPhysicianName}\n"\
            + f"{ds.StudyDescription}\n"\
            + f"{ds.Modality}\n"\
            + f"{ds.Manufacturer}\n"\
            + f"{ds.StudyID}\n"\
            + f"{ds.StudyDate}\n"\
            + f"{ds.SeriesNumber}\n"\
            + f"{ds.PixelSpacing[0]}\n"\
            + f"{ds.PixelSpacing[1]}\n"\
            + f"{ds.SliceThickness}\n"\
            + f"{cube.shape[2]}\n"\
            + f"{cube.shape[1]}\n"\
            + f"{ds.ImagePositionPatient[0]}\n"\
            + f"{ds.ImagePositionPatient[1]}\n"\
            + f"{ds.ImagePositionPatient[2]}\n"\
            + f"{ds.ImageOrientationPatient[0]}\n"\
            + f"{ds.ImageOrientationPatient[1]}\n"\
            + f"{ds.ImageOrientationPatient[2]}\n"\
            + f"{ds.ImageOrientationPatient[3]}\n"\
            + f"{ds.ImageOrientationPatient[4]}\n"\
            + f"{ds.ImageOrientationPatient[5]}\n"      
    
    with open(f"{path}\\{name}.txt", "w") as ftxt:
        ftxt.write(string)

    with open(f"{path}\\{name}.ini", "w") as fini:
        fini.write(f"dimx:{cube.shape[2]}\n"
                   f"dimy:{cube.shape[1]}\n"
                   f"dimz:{cube.shape[0]}\n"
                   f"skip:0\n"
                   f"format:{encoding}")

