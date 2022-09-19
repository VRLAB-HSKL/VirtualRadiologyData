from pydicom.uid import generate_uid
import pydicom
import convertDicomDir

fin = r"C:\Users\RHoock\Downloads\VHF-Pelvis.tar\VHF-Pelvis\Pelvis"
fout = r"C:\Users\RHoock\Desktop\DICOM\female\Pelvis"
series = "Pelvis"
seriesUID = generate_uid()
imglist = convertDicomDir.imagelist(fin)
for i, ds in enumerate(imglist):
    ds.SeriesDescription = series
    ds.SeriesInstanceUID = seriesUID
    ds.save_as(f"{fout}\\{ds.PatientSex}{ds.SeriesDescription}{i:04d}.dcm")
print(f"{imglist[0] = }")

