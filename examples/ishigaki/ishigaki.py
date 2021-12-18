from exocounts.exocounts import exocounts
from exocounts.exocounts import convmag

import numpy as np

ishigaki=exocounts.InstClass()
ishigaki.lamb = 0.5 #micron
ishigaki.dlam = 0.1 #micron
ishigaki.dtel = 1.05 #telescope diameter m
ishigaki.dstel = 0.2 #secondary telescope diameter m
ishigaki.throughput = 0.7
ishigaki.ndark = 0.0 #dark current
ishigaki.nread = 0.0 #nr
ishigaki.fullwell = np.nan

target=exocounts.TargetClass()
target.teff = 5000.0 #K
target.rstar = 0.68 #Rsolar
target.dpc = 258.0 #pc

obs=exocounts.ObsClass(ishigaki,target) 

obs.texposure = 1.0/60.0 #cadence [hour]
obs.tframe = 120  #time for one frame [sec]
obs.napix = 0 # number of the pixels in aperture 

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("V mag=",convmag.get_mag("V",obs.flux,magdict))
print("=========================")
print(obs.texposure*60.0,"[min] exposure")
print("photon [ppm]=",obs.sign)
print("photon noise fraction (7 sigma)=",7.0/np.sqrt(obs.nphoton_exposure))
