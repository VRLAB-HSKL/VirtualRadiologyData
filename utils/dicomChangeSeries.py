from pydicom.uid import generate_uid
import convertDir

fin = r"/path/to/series"
fout = r"/output/folder"
series = "Series Description"
seriesUID = generate_uid()
imglist = convertDir.imagelist(fin)
for i, ds in enumerate(imglist):
    ds.SeriesDescription = series
    ds.SeriesInstanceUID = seriesUID
    ds.save_as(f"{fout}\\{ds.PatientSex}{ds.SeriesDescription}{i:04d}.dcm")
print(f"{imglist[0] = }")

