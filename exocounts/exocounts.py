import numpy as np
from astropy import units as u

class InstClass(object):
    def __init__(self):
        self.lamb = None
        self.dlam = None
        self.dtel = None
        self.dstel = None
        self.throughput = None
        self.ndark = None #nd
        self.nread = None #nr
        self.fullwell = None
        
class TargetClass(object):
    def __init__(self):
        self.teff = None
        self.rstar = None
        self.d = None
        self.name = "No Name"
        self.contrast = 1
        
class ObsClass(object):
    def __init__(self,Inst,Target):
        self.inst = Inst
        self.target = Target

        #INPUTS
        self.mu = None
        self.texposure = None #th
        self.tframe = None  #tr   
        self.napix = None
        self.effnpix = None #conversion for the brightest pixel

        ####OUTPUTS####
        self.nphoton_exposure = None
        self.nphoton_frame = None
        self.flux = None
        self.photonf = None
        
        self.sign = None
        self.sigd = None 
        self.sigr = None
        self.sign_relative = None
        self.sigd_relative = None 
        self.sigr_relative = None
        
        self.sat = False #Saturation

        
    def update(self):
        self.calc_noise()

        try:
            self.nphoton_brightest = self.nphoton_frame/self.effnpix
            if self.nphoton_brightest > self.inst.fullwell:
                self.sat = True
            else:
                self.sat = False
        except:
            self.sat = False
            
    def calc_noise(self):
        import nstar
        nstar.Nstar(self.inst,self.target,self)
        ppm=1.e6
        #hr2sec=3600.0
        #ndframe=self.texposure*hr2sec*self.inst.ndark
        ndframe=self.texposure.to(u.s)*self.inst.ndark

        try:
            self.sigd=np.sqrt(self.mu*self.napix*ndframe)
            self.sigd_relative=self.sigd/self.nphoton_exposure*ppm
        except:
            self.sigd=None
            self.sigd_relative=None

        try:
            self.sigr=np.sqrt(self.mu*self.napix*self.texposure.to(u.s)/self.tframe)*self.inst.nread
            self.sigr_relative=self.sigr/self.nphoton_exposure*ppm
        except:
            self.sigr=None
            self.sigr_relative=None
