import datetime, subprocess
from PyQt6.QtCore import QThread, pyqtSignal
from pydicom.dataset import Dataset
import cfind
import cget


class StudyWorker(QThread):
    rebound = pyqtSignal(dict)

    def __init__(self, server, parent=None):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.server = server
        self.ds = Dataset()
        self.ds.QueryRetrieveLevel = "STUDY"
        self.ds.PatientName = ""
        self.ds.PatientID = ""
        self.ds.PatientSex = ''
        self.ds.PatientBirthDate = ''
        self.ds.StudyInstanceUID = ""
        self.ds.StudyDate = ''
        self.ds.Modality = ''

    def run(self):
        """abrufen der Study-Informationen von Orthanc"""
        data = cfind.cfind(self.server, self.ds)
        """liefert Daten in Form:
        res = {StudyInstanceUID: (StudyDate:datetime.date, 'PatientName, PatientSex, PatientBirthDate', 'PatientID')}"""
        res = {}
        for i in data:
            if i[1]:
                elem = i[1]
                key = elem.StudyInstanceUID
                val = str(elem.PatientName) + ', ' + str(elem.PatientSex) + ', ' + str(elem.PatientBirthDate)

                if len(str(elem.StudyDate)) == 8:
                    date = str(elem.StudyDate)
                    date = [date[0:4], date[4:6], date[6:8]]
                    date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                else:
                    date = ['0000', '00', '00']

                value = (date.strftime("%Y-%m-%d"), val, str(elem.PatientID))
                res[key] = value

                print("_______")
        self.rebound.emit(res)
        self.stop()

    def stop(self):
        print("stopping thread!")
        self._isRunning = False


class SeriesWorker(QThread):
    rebound = pyqtSignal(dict)

    def __init__(self, treeview, server, key, patid, parent=None):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.server = server
        self.ds = Dataset()
        self.ds.QueryRetrieveLevel = "SERIES"
        self.ds.StudyInstanceUID = key
        self.ds.PatientID = patid
        self.ds.SeriesDate = ''
        self.ds.SeriesDescription = ''
        self.ds.Modality = ""
        self.ds.BodyPartExamined = ''
        self.treeview = treeview

    def run(self):
        """abrufen der Series-Informationen von Orthanc"""
        data = cfind.cfind(self.server, self.ds)
        """liefert Daten in Form:
        res = {SeriesInstanceUID: (SeriesDate:datetime.datetime, 'SeriesDescription, Modality, BodyPartExamined')}"""
        res = {}
        for i in data:
            if i[1]:
                elem = i[1]
                key = elem.SeriesInstanceUID
                val = str(elem.SeriesDescription) + ', ' + str(elem.Modality) + ', ' + str(elem.BodyPartExamined)
                if elem.SeriesDate != '':
                    date = elem.SeriesDate
                    date = [date[0:4], date[4:6], date[6:8]]
                else:
                    date = ["01", "01", "01"]
                if elem.SeriesTime != '':
                    time = elem.SeriesTime
                    time1 = time.split(".")
                    time2 = time1[0]
                    time3 = [time2[0:2], time2[2:4], time2[4:6]]
                else:
                    time3 = ["00", "00", "00"]
                dati = datetime.datetime(int(date[0]), int(date[1]), int(date[2]),
                                         int(time3[0]), int(time3[1]), int(time3[2]))
                value = (dati.strftime("%Y-%m-%d, %H:%M:%S"), val)
                res[key] = value
                print("_______")
        self.treeview.label.setText("In threads geschrieben!")
        self.rebound.emit(res)
        self.stop()

    def stop(self):
        print("stopping thread!")
        self._isRunning = False


class ImageWorker(QThread):
    rebound = pyqtSignal(list)

    def __init__(self, treeview, server, modality, parent=None):
        QThread.__init__(self, parent)
        self.treeview = treeview
        self.server = server
        self.modality = modality
        self.seriesid = ''
        print("Thread startet!")

    def run(self):
        imglist = cget.imagelist(self.server, self.seriesid, self.modality)
        ds = imglist[0]
        self.treeview.label.setText(f"{ds.PatientName = }\n"
                                    f"{ds.PatientID = }\n"
                                    f"{ds.PatientBirthDate = }\n"
                                    f"{ds.PatientSex = }\n"
                                    f"{ds.InstitutionName = }\n"
                                    f"{ds.ReferringPhysicianName = }\n"
                                    f"{ds.StudyDescription = }\n"
                                    f"{ds.Modality = }\n"
                                    f"{ds.Manufacturer = }\n"
                                    f"{ds.StudyID = }\n"
                                    f"{ds.StudyDate = }\n"
                                    f"{ds.SeriesNumber = }\n"
                                    f"{ds.PixelSpacing[0] = }\n"
                                    f"{ds.PixelSpacing[1] = }\n"
                                    f"{ds.SliceThickness = }\n"
                                    f"{ds.Columns = }\n"
                                    f"{ds.Rows = }\n"
                                    f"{ds.ImagePositionPatient[0] = }\n"
                                    f"{ds.ImagePositionPatient[1] = }\n"
                                    f"{ds.ImagePositionPatient[2] = }\n"
                                    f"{ds.ImageOrientationPatient[0] = }\n"
                                    f"{ds.ImageOrientationPatient[1] = }\n"
                                    f"{ds.ImageOrientationPatient[2] = }\n"
                                    f"{ds.ImageOrientationPatient[3] = }\n"
                                    f"{ds.ImageOrientationPatient[4] = }\n"
                                    f"{ds.ImageOrientationPatient[5] = }")
        self.rebound.emit(imglist)
        self.stop()

    def stop(self):
        print("stopping thread!")
        self._isRunning = False

