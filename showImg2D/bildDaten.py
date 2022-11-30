from showImg2D import windowSagittal, windowFrontal


class BildDaten(object):
    def __init__(self, fenster, img, cross=(0, 200, 200)):
        self.fenster = fenster
        self.cube = img.volume
        self.cross = cross
        #self.grauwerte = {}
        self.yellow = (255, 255, 0)
        self.cyan = (0, 255, 255)
        self.red = (255, 0, 0)
        self.fenster.frontal = windowFrontal.WindowFrontal(self.fenster, self)
        self.fenster.sagittal = windowSagittal.WindowSagittal(self.fenster, self)
        self.fenster.frontal.show()
        self.fenster.sagittal.show()
