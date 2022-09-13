import skimage.exposure as se
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
import cget

class Image():
    
    images = {}
    
    def __init__(self, seruid, imglist):
        self.volume, self.pLow, self.pHigh = createVolume(imglist)
        self.imglist = imglist
        Image.images[seruid] = self
        
def createVolume(imglist):
        pixellst = [i.pixel_array for i in imglist]
        cube = np.asarray(pixellst)
        cube, pLow, pHigh = rescale_intensity(cube)
        return cube, pLow, pHigh

def rescale_intensity(data):
    p_low, p_high = np.percentile(data, (0, 100))
    data = se.rescale_intensity(data, in_range=(p_low, p_high), out_range=(0, 255))
    return data, p_low, p_high

class ImageWorker(QThread):
    rebound = pyqtSignal(str)
    
    def __init__(self, server, seriesid, parent=None):
        QThread.__init__(self, parent)
        self.server = server
        self.seriesid = seriesid
        print("Thread startet!")
        
    def run(self):
        imglist = cget.imagelist(self.server, self.seriesid)
        print(imglist)
        seruid = imglist[0].SeriesInstanceUID
        Image(seruid, imglist)
        self.rebound.emit(seruid)
        self.stop()
    
    def stop(self):
        print("stopping thread!")
        self._isRunning = False
