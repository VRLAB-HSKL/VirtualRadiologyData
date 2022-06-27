import numpy as np
import skimage.exposure as se
import windowFrontal
import windowSagittal


class BildDaten(object):
    def __init__(self, fenster, imglist, cross=(0, 200, 200)):
        self.fenster = fenster
        self.cube = None
        self.cross = cross
        self.grauwerte = {}
        self.yellow = (255, 255, 0)
        self.cyan = (0, 255, 255)
        self.red = (255, 0, 0)
        self.get_cube(imglist)

    def get_cube(self, imglist):
        newlist = [i.pixel_array for i in imglist]
        self.cube = np.asarray(newlist)
        '''grauwerte anpassen'''
        self.cube, p_low, p_high = rescale_intensity(self.cube)
        p_level = (p_low + p_high) / 2
        p_width = p_high - p_low
        self.grauwerte = {'pLow': p_low, 'pHigh': p_high, 'pLevel': p_level, 'pWidth': p_width}

        self.fenster.frontal = windowFrontal.WindowFrontal(self.fenster,  self)
        self.fenster.sagittal = windowSagittal.WindowSagittal(self.fenster, self)
        self.fenster.frontal.show()
        self.fenster.sagittal.show()


def rescale_intensity(data):
    p_low, p_high = np.percentile(data, (0, 100))
    data = se.rescale_intensity(data, in_range=(p_low, p_high), out_range=(0, 255))
    return data, p_low, p_high
