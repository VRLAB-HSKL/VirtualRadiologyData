import numpy as np
from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
import sys
import os
import cv2
from preprocessing.showimg2d import fenster


class WindowSagittal(QDialog):
    def __init__(self, fenster, bild_daten):
        super().__init__()
        loadUi("./preprocessing/showimg2d/bilder.ui", self)
        self.setWindowTitle('Sagittalebene')
        '''Attribute'''
        self.fenster = fenster
        self.bildDaten = bild_daten

        self.get_image()
        self.label.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.label:
            if event.type() == 5:
                pos = event.position()
                y = (self.bildDaten.cube.shape[2] - 1) - max(0, min(pos.x(), self.bildDaten.cube.shape[2]-1))
                z = max(0, min(pos.y(), self.bildDaten.cube.shape[0]-1))
                self.bildDaten.cross = (int(z), self.bildDaten.cross[1], int(y))
                self.get_image()
                self.fenster.transversal.get_image()
                self.fenster.frontal.get_image()
            return False
        return False

    def get_image(self):
        """herausholen einer Schicht aus dem "Voxelblock"""""
        pixel = self.bildDaten.cube[::, :, self.bildDaten.cross[1]]
        '''umwendeln in cv-Bild'''
        new_pixel = np.transpose(pixel)
        new_pixel = np.rot90(new_pixel, 3)
        new8_bit_grey = new_pixel.astype('uint8')
        cvimage = cv2.cvtColor(new8_bit_grey, cv2.COLOR_GRAY2RGB)
        '''einzeichnen der Linien'''
        cv2.line(cvimage, (0, self.bildDaten.cross[0]),
                 (cvimage.shape[1], self.bildDaten.cross[0]),
                 self.bildDaten.cyan, 1, cv2.LINE_4)
        cv2.line(cvimage, (cvimage.shape[1] - self.bildDaten.cross[2], 0), (cvimage.shape[1] - self.bildDaten.cross[2], cvimage.shape[0]-1),
                 self.bildDaten.red, 1, cv2.LINE_4)
        cv2.rectangle(cvimage, (0, 0), (cvimage.shape[1] - 1, cvimage.shape[0]-1),
                      self.bildDaten.yellow, 1, cv2.LINE_4)
        self.label.resize(cvimage.shape[1], cvimage.shape[0])

        fenster.show(self, cvimage)


    def wheelEvent(self, event):
        #if keyboard.is_pressed('p'):
         #   print('p pressed')
        y = (self.bildDaten.cross[1] + event.angleDelta().y() / 120) % self.bildDaten.cube.shape[2]
        self.bildDaten.cross = (self.bildDaten.cross[0], int(y), self.bildDaten.cross[2])
        self.get_image()
        self.fenster.transversal.get_image()
        self.fenster.frontal.get_image()

