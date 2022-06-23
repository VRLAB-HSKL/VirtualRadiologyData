from pydicom.uid import generate_uid
import pydicom
import convertDicomDir

fin = r""
fout = r""
series = "Hip"
seriesUID = generate_uid()
imglist = convertDicomDir.imagelist(fin)
for i, ds in enumerate(imglist):
    ds.SeriesDescription = series
    ds.SeriesInstanceUID = seriesUID
    ds.save_as(f"{fout}\\{ds.PatientSex}{ds.SeriesDescription}{i:04d}.dcm")
print(f"{imglist[0] = }")

