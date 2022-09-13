import cfind, datetime, menu, study, patient
from pydicom import Dataset
from PyQt6.QtCore import QThread, pyqtSignal

class Series():
    
    serieses = {}
    
    def __init__(self, ds):
        self.UID = ds.SeriesInstanceUID
        self.stduid = ds.StudyInstanceUID
        self.serdate = ds.SeriesDate
        self.serdesc = ds.SeriesDescription
        self.modality = ds.Modality
        self.data = ds
        Series.serieses[self.UID] = self

    def toTreeView(self):
        return [self.UID, self.modality, self.serdesc, menu.toISOdate(self.serdate)]    

    def getFilename(self):
        std = study.Study.studies[self.stduid]
        pat = patient.Patient.patients[std.patid]
        return f"{pat.patname}{self.serdesc}"
        
class SeriesWorker(QThread):
    rebound = pyqtSignal(str)
    
    def __init__(self, server, stduid, parent=None):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.server = server
        self.ds = Dataset()
        self.ds.QueryRetrieveLevel = "SERIES"
        self.ds.StudyInstanceUID = stduid
        self.ds.SeriesInstanceUID = ""
        self.ds.SeriesDate = ""
        self.ds.SeriesDescription = ""
        self.ds.Modality = ''
        self.ds.InstitutionName = ''
        self.ds.InstitutionAddress = ''
    
    def run(self):
        """abrufen der Study-Informationen von Orthanc"""
        data = cfind.cfind(self.server, self.ds)
        for elem in data:
            res = elem.StudyInstanceUID
            Series(elem)
        self.rebound.emit(res)
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False
