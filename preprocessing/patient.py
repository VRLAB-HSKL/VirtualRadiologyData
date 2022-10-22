import datetime, threading, time
from pydicom import Dataset
from PyQt6.QtCore import QThread, pyqtSignal
from preprocessing import cfind

def toISOdate(dcmdate):
    date = str(dcmdate)
    if len(date) == 8:
        date = [date[0:4], date[4:6], date[6:8]]
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        date = date.strftime("%Y-%m-%d")
    else:
        date = "Unkown"
    return date


class Patient():
    
    patients = {}
    
    def __init__(self, ds):
        self.id = ds.PatientID
        self.patname = str(ds.PatientName)
        self.patsex = ds.PatientSex
        self.patbirthdate = ds.PatientBirthDate
        self.data = ds
        Patient.patients[self.id] = self
        
    def toTreeView(self):
        return [self.id, self.patname, self.patsex, toISOdate(self.patbirthdate)]

    
class PatientWorker(QThread):
    rebound = pyqtSignal(str)
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.ds = Dataset()
        self.ds.QueryRetrieveLevel = "PATIENT"
        self.ds.PatientName = ""
        self.ds.PatientID = ""
        self.ds.PatientSex = ''
        self.ds.PatientBirthDate = ''
    
    def run(self):
        """abrufen der Study-Informationen von Orthanc"""
        data = cfind.cfind(self.ds)
        for elem in data:
            res = elem.PatientID
            Patient(elem)
        self.rebound.emit(res)
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False
