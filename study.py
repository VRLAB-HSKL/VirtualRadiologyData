import cfind, datetime
from pydicom import Dataset
from PyQt6.QtCore import QThread, pyqtSignal

class Study():
    
    studies = {}
    
    def __init__(self, uid, patid, stddate, stddesc, stdid, refphysname):
        self.UID = uid
        self.patid = patid
        self.stddate = stddate
        self.stddesc = stddesc
        self.stdid = stdid
        self.refphysname = refphysname 
        Study.studies[self.UID] = self

    @classmethod        
    def from_ds(cls, ds):
        Study(ds.StudyInstanceUID, ds.PatientID, ds.StudyDate, ds.StudyDescription, ds.StudyID, ds.ReferringPhysicianName)

    
class StudyWorker(QThread):
    rebound = pyqtSignal(str)
    
    def __init__(self, server, patid, parent=None):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.server = server
        self.ds = Dataset()
        self.ds.QueryRetrieveLevel = "STUDY"
        self.ds.PatientID = patid
        self.ds.StudyDescription = ""
        self.ds.StudyID = ""
        self.ds.ReferringPhysicianName = ""
        self.ds.StudyInstanceUID = ""
        self.ds.StudyDate = ''
        self.ds.Modality = ''
    
    def run(self):
        """abrufen der Study-Informationen von Orthanc"""
        data = cfind.cfind(self.server, self.ds)
        for i in data:
            if i[1]:
                elem = i[1]
                res = elem.StudyInstanceUID
                Study.from_ds(elem)
        self.rebound.emit(res)
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False