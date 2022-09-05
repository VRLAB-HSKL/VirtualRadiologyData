from PyQt6.QtGui import QImage, QPixmap


class Fenster(object):
    def __init__(self, transversal, frontal=None, sagittal=None):
        self.transversal = transversal
        self.frontal = frontal
        self.sagittal = sagittal


def show(window, cvimage):
    window.label.resize(cvimage.shape[1], cvimage.shape[0])

    qimg = QImage(cvimage, cvimage.shape[1], cvimage.shape[0], cvimage.shape[1]*3,
                  QImage.Format.Format_RGB888)
    pixmap = QPixmap.fromImage(qimg)
    window.label.setPixmap(pixmap)
