from PyQt6.QtWidgets import QDialog
from PyQt6.uic import loadUi
import cv2
from showImg2D import fenster, bildDaten


class WindowTransversal(QDialog):
    def __init__(self, img):
        super().__init__()
        loadUi("./showImg2D/bilder.ui", self)
        self.setWindowTitle('Transversalebene')
        '''Attribute'''
        self.fenster = fenster.Fenster(self)
        self.bildDaten = bildDaten.BildDaten(self.fenster, img)

        self.get_image()
        self.label.installEventFilter(self)

    def eventFilter(self, source, event):
        if source == self.label:
            if event.type() == 5:
                pos = event.position()
                x = max(0, min(pos.x(), self.bildDaten.cube.shape[1]-1))
                y = max(0, min(pos.y(), self.bildDaten.cube.shape[2]-1))
                self.bildDaten.cross = (self.bildDaten.cross[0], int(x), int(y))
                self.get_image()
                self.fenster.frontal.get_image()
                self.fenster.sagittal.get_image()
            return False
        return False

    def get_image(self):
        """herausholen einer Schicht aus dem "Voxelblock"""""
        pixel = self.bildDaten.cube[self.bildDaten.cross[0], :, :]
        '''umwendeln in cv-Bild'''
        new8_bit_grey = pixel.astype('uint8')
        cvimage = cv2.cvtColor(new8_bit_grey, cv2.COLOR_GRAY2RGB)
        '''einzeichnen der Linien'''
        cv2.line(cvimage, (self.bildDaten.cross[1], 0), (self.bildDaten.cross[1], cvimage.shape[0]-1),
                 self.bildDaten.yellow, 1, cv2.LINE_4)
        cv2.line(cvimage, (0, self.bildDaten.cross[2]), (cvimage.shape[1]-1, self.bildDaten.cross[2]),
                 self.bildDaten.red, 1, cv2.LINE_4)
        cv2.rectangle(cvimage, (0, 0), (cvimage.shape[0]-1, cvimage.shape[1]-1), self.bildDaten.cyan, 1,
                      cv2.LINE_4)
        #v2.putText(cvimage, f"Cross = {self.bildDaten.cross}", (10, cvimage.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (40, 200, 230), 1)

        fenster.show(self, cvimage)

    def wheelEvent(self, event):
        z = (self.bildDaten.cross[0] - event.angleDelta().y() / 120) % len(self.bildDaten.cube)
        self.bildDaten.cross = (int(z), self.bildDaten.cross[1], self.bildDaten.cross[2])
        self.get_image()
        self.fenster.frontal.get_image()
        self.fenster.sagittal.get_image()
        #print(event.angleDelta().y() / 120)
        #self.label.setText("Total Steps: " + QString.number(self.x))

