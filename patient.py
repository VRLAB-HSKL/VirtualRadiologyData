import cfind, datetime, threading, time, menu
from pydicom import Dataset
from PyQt6.QtCore import QThread, pyqtSignal

class Patient():
    
    patients = {}
    
    def __init__(self, patid, patname="Unknown", patsex="Unknown", patbirthdate="Unknown"):
        self.id = patid
        self.patname = patname
        self.patsex = patsex
        self.patbirthdate = patbirthdate
        Patient.patients[self.id] = self

    @classmethod        
    def from_ds(cls, ds):
        Patient(ds.PatientID, str(ds.PatientName), ds.PatientSex, ds.PatientBirthDate)
        
    def toTreeView(self):
        return [self.id, self.patname, self.patsex, menu.toISOdate(self.patbirthdate)]

    
class PatientWorker(QThread):
    rebound = pyqtSignal(dict)
    
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
        res = {}
        for i in data:
            if i[1]:
                elem = i[1]
                res[elem.PatientID] = Patient.from_ds(elem)
        self.rebound.emit(res)
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False