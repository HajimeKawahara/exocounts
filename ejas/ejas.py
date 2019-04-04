from exocounts.exocounts import exocounts
from exocounts.exocounts import nstar
import numpy as np

ejas=exocounts.InstClass()
ejas.lamb = 1.4 #micron
ejas.dlam = 0.6 #micron
ejas.dtel = 0.31 #telescope diameter m
ejas.dstel = 0.09 #secondary telescope diameter m
ejas.throughput = 0.7
ejas.tcadence = 0.0833 #cadence [hour]
ejas.tframe = 7.1  #time for one frame [sec]
ejas.ndark = 10.0 #dark current
ejas.nread = 30.0 #nr
ejas.npix = 15 # number of the pixels in aperture 

S=1.8*1.8*np.pi #core size
ejas.effnpix = S/3.0 #3 is an approx. increment factor of PSF
ejas.mu = 1 

target=exocounts.TargetClass()
target.teff = 3000.0 #K
target.rstar = 0.2 #Rsolar
target.dpc = 15.0 #pc

obs=exocounts.ObsClass(ejas,target) 

print(obs.nphoton_brightest)
print(obs.sign)
print(obs.sigd)
print(obs.sigr)
