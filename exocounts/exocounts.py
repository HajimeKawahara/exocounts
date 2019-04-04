import numpy as np

class InstClass(object):
    def __init__(self):
        self.lamb = None
        self.dlam = None
        self.dtel = None
        self.dstel = None
        self.throughput = None
        self.tcadence = None #th
        self.tframe = None  #tr   
        self.ndark = None #nd
        self.nread = None #nr
        self.mu = None
        self.npix = None
        self.effnpix = None #conversion for the brightest pixel
        
class TargetClass(object):
    def __init__(self):
        self.teff = None
        self.rstar = None
        self.dpc = None


class ObsClass(object):
    def __init__(self,Inst,Target):
        self.nphoton_cadence = None
        self.nphoton_frame = None
        self.sign = None
        self.sigd = None 
        self.sigr = None 
        self.inst = Inst
        self.target = Target
        self.calc_noise()
        self.nphoton_brightest = self.nphoton_frame/self.inst.effnpix
        
    def calc_noise(self):
        from exocounts.exocounts import nstar
        nstar.Nstar(self.inst,self.target,self)
                
        hr2sec=3600.0
        ndframe=self.inst.tcadence*hr2sec*self.inst.ndark 
        self.sigd=np.sqrt(self.inst.mu*self.inst.npix*ndframe)        
        self.sigr=np.sqrt(self.inst.mu*self.inst.npix*self.inst.tcadence*hr2sec/self.inst.tframe)*self.inst.nread
