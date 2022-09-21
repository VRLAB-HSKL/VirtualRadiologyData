from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog, QTreeWidgetItem, QMenu
from PyQt6.QtGui import QAction
from PyQt6.uic import loadUi
import os, sys, subprocess, tempfile, threading, datetime, re
from pydicom import Dataset
from threading import Thread
import copy
from postprocessing import srmain, config
from preprocessing import patient, study, series, image, dicomToFiles, windowTransversal


class Menu(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(sys.path[0], "menu.ui"), self)
        self.server = "127.0.0.1" #10.0.27.2"
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
        self.seriestree.setHeaderLabels(["SeriesUID", "Modality", "SeriesDescription", "SeriesDate"])
        self.seriestree.itemDoubleClicked.connect(self.series_line_click_handler)
        self.seriestree.itemClicked.connect(self.series_line_singleclick_handler)
        self.seriestree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.seriestree.customContextMenuRequested.connect(self.menuContextTree)
        '''Label Einstellungen'''
        #self.label.setText("Dies ist ein Test")
        '''Button Einstellungen'''
        self.schichtenBtn.setEnabled(False)
        self.schichtenBtn.clicked.connect(self.schichtenbtn_clicked)
        self.vrBtn.setEnabled(False)
        self.vrBtn.clicked.connect(self.vrBtn_clicked)
        self.srBtn = QAction("Hüftendoprothetik")
        self.srBtn.triggered.connect(self.createSR)
        '''Attribute'''
        self.role = 'patient'
        self.data = None
        self.thread = None
        self.srThread = None
        self.id = None
        self.tempdir = tempfile.TemporaryDirectory()
        print(self.tempdir.name)
        self.loadData()
        
    
    def __del__(self):
        self.tempdir.cleanup()
        print("tempdir gelöscht")
        
        
    def loadData(self):
        if self.role == 'patient':
            self.thread = patient.PatientWorker(self.server)
        if self.role == 'study':
            self.thread = study.StudyWorker(self.server, self.id)
        if self.role == 'series':
            self.thread = series.SeriesWorker(self.server, self.id)  
        if self.role == 'image':
            self.thread = image.ImageWorker(self.server, self.id)
            self.schichtenBtn.setText("downloading ...")
        self.thread.start()
        self.thread.rebound.connect(self.loadhandler)
        
    def loadhandler(self):
        if self.role == 'patient':
            dictionary = patient.Patient.patients
            tree = self.patienttree
        if self.role == 'study':
            dictionary = study.Study.studies
            tree = self.studytree
            tree.clear()
        if self.role == 'series':
            dictionary = series.Series.serieses
            tree = self.seriestree
            tree.clear()
        if self.role == 'image':
            dictionary = image.Image.images
        for k, v in dictionary.items():
            if self.role == 'study' and self.id != v.patid:
                continue
            if self.role == 'series' and self.id != v.stduid:
                continue
            if self.role == 'image':
                if k == self.id:
                    dicomToFiles.convert(k, path=self.tempdir.name)
                    self.schichtenBtn.setEnabled(True)
                    self.vrBtn.setEnabled(True)
                    self.schichtenBtn.setText("Bilder anzeigen")
                    self.vrBtn.setText("Bilder in VR anzeigen")
            else:
                line = QTreeWidgetItem(v.toTreeView())
                tree.addTopLevelItem(line)
        
        
    def patient_line_click_handler(self):
        self.role = 'study'
        if self.thread:
            self.thread.terminate()
            self.thread = None
            print('Thread terminated!')
        item = self.patienttree.currentItem()
        self.id = str(item.text(0))
        pat = patient.Patient.patients[self.id]
        self.data = copy.deepcopy(pat.data)
        self.label.setText(f"{self.data}")
        self.seriestree.clear()
        if any(v.patid == self.id for k, v in study.Study.studies.items()):
            self.loadhandler()
        else:
            self.loadData()
    
            
    def study_line_click_handler(self):
        self.role = 'series'
        """auswählen einer Study"""
        if self.thread:
            self.thread.terminate()
            self.thread = None
            print('Thread terminated!')
        item = self.studytree.currentItem()
        self.id = item.text(0)
        std = study.Study.studies[self.id]
        for k, v in std.data.items():
            self.data.add_new(k, v.VR, v.value)
        self.label.setText(f"{self.data}")
        if any(v.stduid == self.id for k, v in series.Series.serieses.items()):
            self.loadhandler()
        else:
            self.loadData()
    
    def series_line_click_handler(self):
        self.role = 'image'
        """auswählen einer Series"""
        if self.thread:
            self.thread.terminate()
            self.thread = None
            print('Thread terminated!')
        self.schichtenBtn.setEnabled(False)
        self.vrBtn.setEnabled(False)
        item = self.seriestree.currentItem()
        self.id = item.text(0)
        ser = series.Series.serieses[self.id]
        for k, v in ser.data.items():
            self.data.add_new(k, v.VR, v.value)
        self.label.setText(f"{self.data}")
        if any(k == self.id for k, v in image.Image.images.items()):
            self.loadhandler()
        else:
            self.loadData()
    
    def series_line_singleclick_handler(self):
        item = self.seriestree.currentItem()
        self.id = item.text(0)
        ser = series.Series.serieses[self.id]
        for k, v in ser.data.items():
            self.data.add_new(k, v.VR, v.value)
        self.label.setText(f"{self.data}")
        if str(self.data['SeriesInstanceUID'].value) in image.Image.images:
            self.schichtenBtn.setEnabled(True)
        else:
            self.schichtenBtn.setEnabled(False)
           
    def schichtenbtn_clicked(self):
        if ("SeriesInstanceUID" in self.data):
            window = windowTransversal.WindowTransversal(image.Image.images[self.data.SeriesInstanceUID])
            window.show()
            
    def vrBtn_clicked(self):
        if self.id in image.Image.images:
            subprocess.Popen([r"C:\Users\RHoock\Desktop\VirtualRadiologyBuild\VirtualRadiology.exe", "-ap", self.tempdir.name, "-m", f"{series.Series.serieses[self.id].getFilename()}"])
        else:
            self.vrBtn.setText("keine Serie ausgewählt!")

    def menuContextTree(self, point):
        index = self.seriestree.indexAt(point)

        if not index.isValid():
            return

        item = self.seriestree.itemAt(point)
        self.id = item.text(0)
        self.series_line_singleclick_handler()
        menu = QMenu()
        submenu = QMenu("SR erstellen", self)
        submenu.addAction(self.srBtn)
        menu.addMenu(submenu)
        menu.exec(self.seriestree.mapToGlobal(point))

    def createSR(self, s):
        global httpd
        imgdata = {}
        imgdata['PatientID'] = str(self.data['PatientID'].value)
        imgdata['PatientName'] = str(self.data['PatientName'].value)
        imgdata['PatientSex'] = str(self.data['PatientSex'].value)
        imgdata['StudyDescription'] = str(self.data['StudyDescription'].value)
        imgdata['SeriesDescription'] = str(self.data['SeriesDescription'].value)
        imgdata['InstanceCreationDate'] = "20050726"
        imgdata['InstanceCreationTime'] = "102049"
        imgdata['Date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        imgdata['Time'] = datetime.datetime.now().strftime('%H:%M:%S')
        with open("./template/Hüftendoprothetik/huefttepV1templ.xml", 'r') as sr:
            txt = sr.read()
        for k, v in imgdata.items():
            pat = f"{{{k}}}"
            txt = re.sub(pat, v, txt)
        with open("./output/output.xml", 'w') as out:
            out.write(txt)
        if self.srThread is not None:
            config.httpd.shutdown()
        self.srThread = Thread(target=srmain.main)
        self.srThread.start()
