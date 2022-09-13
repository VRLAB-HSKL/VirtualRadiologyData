import cfind, datetime, threading, time, menu
from pydicom import Dataset
from PyQt6.QtCore import QThread, pyqtSignal

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
        return [self.id, self.patname, self.patsex, menu.toISOdate(self.patbirthdate)]

    
class PatientWorker(QThread):
    rebound = pyqtSignal(str)
    
    def __init__(self, server, parent=None):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.server = server
        self.ds = Dataset()
        self.ds.QueryRetrieveLevel = "PATIENT"
        self.ds.PatientName = ""
        self.ds.PatientID = ""
        self.ds.PatientSex = ''
        self.ds.PatientBirthDate = ''
    
    def run(self):
        """abrufen der Study-Informationen von Orthanc"""
        data = cfind.cfind(self.server, self.ds)
        for elem in data:
            res = elem.PatientID
            Patient(elem)
        self.rebound.emit(res)
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False
