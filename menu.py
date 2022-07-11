from PyQt6.QtWidgets import QDialog, QTreeWidgetItem
from PyQt6.uic import loadUi
import os, sys, subprocess, tempfile, patient, threading, study, series, datetime, threads, dicomToFiles, windowTransversal

def toISOdate(dcmdate):
    date = str(dcmdate)
    if len(date) == 8:
        date = [date[0:4], date[4:6], date[6:8]]
        date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
    else:
        date = ['0000', '00', '00']
    return date.strftime("%Y-%m-%d")

class Menu(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(sys.path[0], "menu.ui"), self)
        self.server = "10.0.27.2"
        '''Study TreeWidget Einstellungen'''
        self.patienttree.hideColumn(0)
        self.patienttree.setAlternatingRowColors(True)
        self.patienttree.setHeaderLabels(["PatientID", "PatientName", "PatientSex", "BirthDate"])
        self.patienttree.itemClicked.connect(self.patient_line_click_handler)
        '''Study TreeWidget Einstellungen'''
        self.studytree.hideColumn(0)
        self.studytree.setAlternatingRowColors(True)
        self.studytree.setHeaderLabels(["StudyUID", "PatientID", "StudyDate", "StudyDescription"])
        self.studytree.itemClicked.connect(self.study_line_click_handler)
        '''Series TreeWidget Einstellungen'''
        self.seriestree.hideColumn(0)
        self.seriestree.setAlternatingRowColors(True)
        self.seriestree.setHeaderLabels(["SeriesUID", "Series", "DateTime"])
        self.seriestree.itemDoubleClicked.connect(self.series_line_click_handler)
        #self.seriestree.itemClicked.connect(self.showdetailinfo)
        '''Label Einstellungen'''
        #self.label.setText("Dies ist ein Test")
        '''PushButton Einstellungen'''
        self.schichtenBtn.setEnabled(False)
        self.schichtenBtn.clicked.connect(self.schichtenbtn_clicked)
        self.vrBtn.setEnabled(False)
        self.vrBtn.clicked.connect(self.vrBtn_clicked)
        '''Attribute'''
        self.data = None
        self.patientthread = None
        self.studythread = None
        self.seriesthread = None
        self.imagethread = None
        self.tempdir = tempfile.TemporaryDirectory()
        print(self.tempdir.name)
        self.loadPatients()
        
    
    def __del__(self):
        self.tempdir.cleanup()
        print("tempdir gelöscht")
        
    def loadPatients(self):
        if not self.patientthread:
            self.patientthread = patient.PatientWorker(self.server)
            self.patientthread.start()
            self.patientthread.rebound.connect(self.patienthandler)
        
                
    def patienthandler(self, val):
        for k, v in patient.Patient.patients.items():
                line = QTreeWidgetItem([v.id, v.patname, v.patsex, toISOdate(v.patbirthdate)])
                self.patienttree.addTopLevelItem(line)
        
    def patient_line_click_handler(self):
        if self.studythread:
            self.studythread.terminate()
            self.studythread = None
            print('Thread terminated!')
        item = self.patienttree.currentItem()
        patid = str(item.text(0))
        self.studytree.clear()
        if any(v.patid == patid for k, v in study.Study.studies.items()):
            for k, v in study.Study.studies.items():
                if patid == v.patid:
                    self.studyhandler(patid)
        else:
            self.loadStudies(item.text(0))
            
    def loadStudies(self, patid):
        if not self.seriesthread:
            self.studythread = study.StudyWorker(self.server, patid)
            self.studythread.start()
            self.studythread.rebound.connect(self.studyhandler)
       
    def studyhandler(self, val):
        for k, v in study.Study.studies.items():
            if v.patid == val:
                line = QTreeWidgetItem([v.UID, v.patid, toISOdate(v.stddate), v.stddesc])
                self.studytree.addTopLevelItem(line)
                
    def study_line_click_handler(self):
        """auswählen einer Study"""
        if self.seriesthread:
            self.seriesthread.terminate()
            self.seriesthread = None
            print('Thread terminated!')
        item = self.studytree.currentItem()
        key = item.text(0)
        self.loadSeries(key)

    def loadSeries(self, key):
        """abrufen der Serieses"""
        if not self.seriesthread:
            self.seriesthread = series.SeriesWorker(self.server, key)
            self.seriesthread.start()
            self.seriesthread.rebound.connect(self.serieshandler)

    def serieshandler(self, val):
        """anzeigen der Series-Informationen"""
        self.seriestree.clear()
        for k, v in study.Study.studies.items():
            if v.UID == val:
                line = QTreeWidgetItem([v.UID, v.stdid, toISOdate(v.serdate), v.serdesc])
                self.studytree.addTopLevelItem(line)
        self.seriesthread = None

    def series_line_click_handler(self):
        """auswählen einer Series"""
        if self.imagethread:
            self.imagethread.terminate()
            self.imagethread = None
            print('Thread terminated!')
        self.schichtenBtn.setEnabled(False)
        self.vrBtn.setEnabled(False)
        item = self.seriestree.currentItem()
        key = item.text(0)
        value = item.text(1)
        print(key, value)
        self.image(key, value)
    
    #def showdetailinfo(self):
       

    def image(self, key, value):
        value = value.split(", ")
        if value[1] == 'CT':
            """abrufen der Bilder"""
            self.imagethread = None
            self.imagethread = threads.ImageWorker(self, self.server, value[1])
            self.imagethread.seriesid = key
            self.imagethread.start()
            self.schichtenBtn.setText("downloading ...")
            self.imagethread.rebound.connect(self.imagehandler)


    def imagehandler(self, val):
        if val[0]:
            elem = val[0]
            if str(elem.Modality) == 'CT':
                print(f"{len(val) = }")
                dicomToFiles.convert(val, path=self.tempdir.name)
                self.data = val
            self.schichtenBtn.setEnabled(True)
            self.vrBtn.setEnabled(True)
            self.schichtenBtn.setText("Bilder anzeigen")
    
    def schichtenbtn_clicked(self):
        if self.data:
            window = windowTransversal.WindowTransversal(self.data)
            window.show()
            
    def vrBtn_clicked(self):
        subprocess.Popen([r"C:\Users\RHoock\Desktop\VirtualRadiologyBuild\VirtualRadiology.exe", "-ap", self.tempdir.name, "-m", "Head"])
        

