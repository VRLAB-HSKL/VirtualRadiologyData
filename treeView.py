from PyQt6.QtWidgets import QDialog, QTreeWidgetItem
from PyQt6.uic import loadUi
import os, sys
import threads, dicomToFiles, windowTransversal


class TreeView(QDialog):
    def __init__(self):
        super().__init__()
        loadUi(os.path.join(sys.path[0], "treeView.ui"), self)
        self.server = "10.0.27.15"
        '''Study TreeWidget Einstellungen'''
        self.studytree.hideColumn(0)
        self.studytree.setAlternatingRowColors(True)
        self.studytree.setHeaderLabels(["StudyUID", "Patient", "Date", "PatientID"])
        self.studytree.itemClicked.connect(self.study_line_click_handler)
        '''Series TreeWidget Einstellungen'''
        self.seriestree.hideColumn(0)
        self.seriestree.setAlternatingRowColors(True)
        self.seriestree.setHeaderLabels(["SeriesUID", "Series", "DateTime"])
        self.seriestree.itemDoubleClicked.connect(self.series_line_click_handler)
        #self.seriestree.itemClicked.connect(self.showdetailinfo)
        '''Label Einstellungen'''
        self.label.setText("Dies ist ein Test")
        '''PushButton Einstellungen'''
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.btnclicked)
        '''Attribute'''
        self.data = None
        self.studythread = None
        self.seriesthread = None
        self.imagethread = None
        self.study()

    def study(self):
        """abrufen der Studies"""
        if not self.studythread:
            self.studythread = threads.StudyWorker(self.server)
            self.studythread.start()
            self.studythread.rebound.connect(self.studyhandler)

    def studyhandler(self, val):
        """anzeigen der Study-Informationen"""
        for key, value in val.items():
            line = QTreeWidgetItem([key, value[1], value[0], value[2]])
            self.studytree.addTopLevelItem(line)
        self.studythread = None

    def study_line_click_handler(self):
        """auswählen einer Study"""
        if self.seriesthread:
            self.seriesthread.terminate()
            self.seriesthread = None
            print('Thread terminated!')
        else:
            item = self.studytree.currentItem()
            key = item.text(0)
            value = item.text(1)
            patid = item.text(3)
            print(key, value)
            self.series(key, patid)

    def series(self, key, patid):
        """abrufen der Serieses"""
        self.seriesthread = threads.SeriesWorker(self, self.server)
        self.seriesthread.query = 'SERIES'
        self.seriesthread.studyid = key
        self.seriesthread.patid = patid
        self.seriesthread.start()
        self.seriesthread.rebound.connect(self.serieshandler)

    def serieshandler(self, val):
        """anzeigen der Series-Informationen"""
        self.seriestree.clear()
        for key, value in val.items():
            line = QTreeWidgetItem([key, value[1], value[0]])
            self.seriestree.addTopLevelItem(line)
        self.seriesthread = None

    def series_line_click_handler(self):
        """auswählen einer Series"""
        if self.imagethread:
            self.imagethread.terminate()
            self.imagethread = None
            print('Thread terminated!')
        self.pushButton.setEnabled(False)
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
            self.pushButton.setText("downloading ...")
            self.imagethread.rebound.connect(self.imagehandler)


    def imagehandler(self, val):
        if val[0]:
            elem = val[0]
            if str(elem.Modality) == 'CT':
                print(f"{len(val) = }")
                dicomToFiles.convert(val)
                self.data = val
            self.pushButton.setEnabled(True)
            self.pushButton.setText("Bilder anzeigen")
            

    def btnclicked(self):
        if self.data:
            window = windowTransversal.WindowTransversal(self.data)
            window.show()