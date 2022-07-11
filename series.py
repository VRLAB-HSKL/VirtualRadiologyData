import cfind, datetime
from pydicom import Dataset
from PyQt6.QtCore import QThread, pyqtSignal

class Series():
    
    serieses = {}
    
    def __init__(self, uid, stduid, serdate, serdesc, modality):
        self.UID = uid
        self.stduid = stduid
        self.serdate = serdate
        self.serdesc = serdesc
        self.modality = modality
        Series.serieses[self.UID] = self

    @classmethod        
    def from_ds(cls, ds):
        Series(ds.SeriesInstanceUID, ds.StudyInstanceUID, ds.SeriesDate, ds.SeriesDescription, ds.Modality)

    
class SeriesWorker(QThread):
    rebound = pyqtSignal(str)
    
    def __init__(self, server, stduid, parent=None):
        QThread.__init__(self, parent)
        print("Thread startet!")
        self.server = server
        self.ds = Dataset()
        self.ds.QueryRetrieveLevel = "STUDY"
        self.ds.StudyInstanceUID = stduid
        self.ds.SeriesInstanceUID = ""
        self.ds.SeriesDate = ""
        self.ds.SeriesDescription = ""
        self.ds.Modality = ''
    
    def run(self):
        """abrufen der Study-Informationen von Orthanc"""
        data = cfind.cfind(self.server, self.ds)
        for i in data:
            if i[1]:
                elem = i[1]
                res = elem.SeriesInstanceUID
                Series.from_ds(elem)
        self.rebound.emit(res)
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False