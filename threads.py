import datetime
from PyQt6.QtCore import QThread, pyqtSignal
import cfind
import cget



class StudyWorker(QThread):
    rebound = pyqtSignal(dict)

    def __init__(self, parent=None, query="STUDY"):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.query = query
        self.patid = ''
        self.studyid = ''

    def run(self):
        """abrufen der Study-Informationen von Orthanc"""
        data = cfind.cfind(patid=self.patid, query=self.query, studyid=self.studyid)
        """bringt Daten in Form:
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

    def __init__(self, parent=None, query="Study"):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.query = query
        self.patid = ''
        self.studyid = ''

    def run(self):
        """abrufen der Series-Informationen von Orthanc"""
        data = cfind.cfind(patid=self.patid, query=self.query, studyid=self.studyid)
        """bringt Daten in Form:
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
        self.rebound.emit(res)
        self.stop()

    def stop(self):
        print("stopping thread!")
        self._isRunning = False


class ImageWorker(QThread):
    rebound = pyqtSignal(list)

    def __init__(self, modality, parent=None):
        QThread.__init__(self, parent)
        self.modality = modality
        self.seriesid = ''
        print("Thread startet!")

    def run(self):
        imglist = cget.imagelist(self.seriesid, self.modality)
        self.rebound.emit(imglist)
        #self.rebound.emit(cgetdirekt.cgetdirekt())
        self.stop()

    def stop(self):
        print("stopping thread!")
        self._isRunning = False
