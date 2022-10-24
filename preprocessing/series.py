import datetime
from pydicom import Dataset
from PyQt6.QtCore import QThread, pyqtSignal
from preprocessing import cfind, study, patient

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
        return [self.UID, self.modality, self.serdesc, patient.toISOdate(self.serdate)]

    def getFilename(self):
        std = study.Study.studies[self.stduid]
        pat = patient.Patient.patients[std.patid]
        return f"{pat.patname}{self.serdesc}"
        
class SeriesWorker(QThread):
    rebound = pyqtSignal(str)
    
    def __init__(self, stduid, parent=None):
        QThread.__init__(self, parent)
        print("Thread startet!")
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
        data = cfind.cfind(self.ds)
        res = None
        for elem in data:
            res = elem.StudyInstanceUID
            Series(elem)
        Series.serieses = dict(sorted(Series.serieses.items(), key=lambda i: i[1].serdesc))
        if res != None:
            self.rebound.emit(res)
        else:
            print("######NO DATA######")
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False
