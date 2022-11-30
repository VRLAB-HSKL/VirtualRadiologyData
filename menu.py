import copy
import datetime
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from threading import Thread

from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDialog, QTreeWidgetItem, QMenu
from PyQt6.uic import loadUi
from pydicom.uid import generate_uid

import config
from postprocessing import srmain, templconf
from preprocessing import patient, study, series, image, dicomToFiles
from showImg2D import windowTransversal


class Menu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VirtualRadiologyData")
        loadUi(os.path.join(sys.path[0], "menu.ui"), self)
        self.server = config.pacsIP
        '''Patient TreeWidget Einstellungen'''
        self.patienttree.hideColumn(0)
        self.patienttree.setAlternatingRowColors(True)
        self.patienttree.setHeaderLabels(["PatientID", "PatientName", "PatientSex", "BirthDate"])
        self.patienttree.itemClicked.connect(self.patient_singleclick_handler)
        self.patienttree.itemDoubleClicked.connect(self.patient_doubleclick_handler)
        '''Study TreeWidget Einstellungen'''
        self.studytree.hideColumn(0)
        self.studytree.setAlternatingRowColors(True)
        self.studytree.setHeaderLabels(["StudyUID", "PatientID", "StudyDate", "StudyDescription"])
        self.studytree.itemClicked.connect(self.study_singleclick_handler)
        self.studytree.itemDoubleClicked.connect(self.study_doubleclick_handler)
        '''Series TreeWidget Einstellungen'''
        self.seriestree.hideColumn(0)
        self.seriestree.setAlternatingRowColors(True)
        self.seriestree.setHeaderLabels(["SeriesUID", "Modality", "SeriesDescription", "SeriesDate"])
        self.seriestree.itemDoubleClicked.connect(self.series_doubleclick_handler)
        self.seriestree.itemClicked.connect(self.series_singleclick_handler)
        self.seriestree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.seriestree.customContextMenuRequested.connect(self.menuContextTree)
        '''Button Einstellungen'''
        self.schichtenBtn.setEnabled(False)
        self.schichtenBtn.clicked.connect(self.schichtenbtn_clicked)
        self.vrBtn.setEnabled(False)
        self.vrBtn.clicked.connect(self.vrBtn_clicked)
        self.srBtns = []
        self.srBtn = QAction("Hüftendoprothetik")
        self.srBtn.triggered.connect(self.createSR)
        '''Attribute'''
        self.role = 'patient'
        self.data = None
        self.thread = None
        self.srThread = None
        self.id = None  #ID des zuletzt ausgewählten Eintrag (kann PatientID, StudyInstanceUID oder SeriesInstanceUID sein)
        
        self.tempdir = tempfile.TemporaryDirectory() #Anlegen eines temporären Ordners für die Bilddateien
        print(self.tempdir.name)
        for root, dirnames, filenames in os.walk('./template'):                                         #
            if dirnames:                                                                                #
                index = 0                                                                               #
                for elem in dirnames:                                                                   #Erstellen der Einträge
                    fnames = os.path.join(root, elem, elem)                                             #im Context Menü, um
                    if os.path.isfile(fnames + '.html') and os.path.isfile(fnames + '.xml'):            #SR Vorlagen auszuwählen
                        action = QAction(elem)                                                          #
                        action.triggered.connect(lambda checked, index = index: self.createSR(index))   #
                        self.srBtns.append(action)                                                      #
                        index += 1
        Path('./output').mkdir(parents=True, exist_ok=True) #Erstellen eines Output-Ordners, falls nicht exitstent
        self.loadData()
        
              
    def loadData(self):
        if self.role == 'patient':
            self.thread = patient.PatientWorker()
        if self.role == 'study':
            self.thread = study.StudyWorker(self.id)
        if self.role == 'series':
            self.thread = series.SeriesWorker(self.id)
        if self.role == 'image':
            self.thread = image.ImageWorker(self.id)
            self.schichtenBtn.setText("downloading ...")
        self.thread.start()
        self.thread.rebound.connect(self.showData)
        
    def showData(self):
        dictionary = {}
        if self.role == 'patient':
            dictionary = patient.Patient.patients
            tree = self.patienttree
        if self.role == 'study':
            dictionary = study.Study.studies
            tree = self.studytree
            tree.clear()
        if self.role == 'series':
            dictionary = series.Series.series
            tree = self.seriestree
            tree.clear()
        if self.role == 'image':
            dictionary = image.Image.images
        if dictionary:
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
        else:
            print("#######NO DATA#######")

    def select_patient(self):
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
        self.studytree.clear()
        self.seriestree.clear()

    def patient_singleclick_handler(self):
        self.select_patient()
        if any(v.patid == self.id for k, v in study.Study.studies.items()):
            self.showData()
        else:
            self.loadData()

    def patient_doubleclick_handler(self):
        study.Study.studies = {}
        series.Series.series = {}
        self.select_patient()
        self.loadData()


    def select_study(self):
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
        self.seriestree.clear()

    def study_singleclick_handler(self):
        self.select_study()
        if any(v.stduid == self.id for k, v in series.Series.series.items()):
            self.showData()
        else:
            self.loadData()

    def study_doubleclick_handler(self):
        series.Series.series = {}
        self.select_study()
        self.loadData()

    def series_singleclick_handler(self):
        item = self.seriestree.currentItem()
        self.id = item.text(0)
        ser = series.Series.series[self.id]
        for k, v in ser.data.items():
            self.data.add_new(k, v.VR, v.value)
        self.label.setText(f"{self.data}")
        if str(self.data['SeriesInstanceUID'].value) in image.Image.images:
            self.schichtenBtn.setEnabled(True)
        else:
            self.schichtenBtn.setEnabled(False)

    def series_doubleclick_handler(self):
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
        ser = series.Series.series[self.id]
        for k, v in ser.data.items():
            self.data.add_new(k, v.VR, v.value)
        self.label.setText(f"{self.data}")
        if ser.data.Modality != "SR":
            if any(k == self.id for k, v in image.Image.images.items()):
                self.showData()
            else:
                self.loadData()

    def schichtenbtn_clicked(self):
        if ("SeriesInstanceUID" in self.data):
            window = windowTransversal.WindowTransversal(image.Image.images[self.data.SeriesInstanceUID])
            window.show()
            
    def vrBtn_clicked(self):
        if self.id in image.Image.images:
            subprocess.Popen([config.VirtRadPath, "-ap", self.tempdir.name, "-m", f"{series.Series.series[self.id].getFilename()}"])
        else:
            self.vrBtn.setText("keine Serie ausgewählt!")

    def menuContextTree(self, point):
        index = self.seriestree.indexAt(point)

        if not index.isValid():
            return

        item = self.seriestree.itemAt(point)
        self.id = item.text(0)
        self.series_singleclick_handler()

        if item.text(1) != "SR":
            menu = QMenu()
            submenu = QMenu("SR erstellen", self)
            for btn in self.srBtns:
                submenu.addAction(btn)
            menu.addMenu(submenu)
            menu.exec(self.seriestree.mapToGlobal(point))

    def createSR(self, index):
        global httpd
        time = datetime.datetime.now().strftime('%H%M%S')
        date = datetime.datetime.now().strftime('%Y%m%d')
        imgdata = {
            'ReferencedSeriesUID' : str(self.data['SeriesInstanceUID'].value),
            'PatientID' : str(self.data['PatientID'].value),
            'PatientName' : str(self.data['PatientName'].value),
            'PatientSex' : str(self.data['PatientSex'].value),
            'StudyDescription' : str(self.data['StudyDescription'].value),
            'SeriesDescription' : f"{self.data['SeriesDescription'].value}-REPORT",
            'StudyInstanceUID' : str(self.data['StudyInstanceUID'].value),
            'SeriesInstanceUID' : generate_uid(),
            'SOPInstanceUID' : generate_uid(),
            'InstanceCreationDate' : date,
            'InstanceCreationTime' : time,
            'Date' : date,
            'Time' : time
        }
        templconf.fname = self.srBtns[index].text()
        with open(f"./template/{templconf.fname}/{templconf.fname}.xml", 'r', encoding='utf-8') as sr:
            txt = sr.read()
        for k, v in imgdata.items():
            pat = f"{{{k}}}" #-> '{k}'
            txt = re.sub(pat, v, txt)
        with open("./output/output.xml", 'w', encoding='utf-8') as out:
            out.write(txt)
        if self.srThread is not None:
            templconf.httpd.shutdown()
        self.srThread = Thread(target=srmain.main)
        self.srThread.start()
