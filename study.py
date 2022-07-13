import cfind, datetime
from pydicom import Dataset
from PyQt6.QtCore import QThread, pyqtSignal
import menu

class Study():
    
    studies = {}
    
    def __init__(self, ds):
        self.UID = ds.StudyInstanceUID
        self.patid = ds.PatientID
        self.stddate = ds.StudyDate
        self.stddesc = ds.StudyDescription
        self.stdid = ds.StudyID
        self.refphysname = ds.ReferringPhysicianName
        self.data = ds
        Study.studies[self.UID] = self

        
    def toTreeView(self):
        return [self.UID, self.patid, menu.toISOdate(self.stddate), self.stddesc]

    
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
        self.ds.StudyTime = ''
        self.ds.InstitutionName = ''
        
    
    def run(self):
        """abrufen der Study-Informationen von Orthanc"""
        data = cfind.cfind(self.server, self.ds)
        for i in data:
            if i[1]:
                elem = i[1]
                res = elem.PatientID
                Study(elem)
        self.rebound.emit(res)
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False