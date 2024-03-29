import exocounts
import convmag

import numpy as np

ost=exocounts.InstClass()
ost.lamb =  1.3 #micron
ost.dlam = 0.013 #micron
#ost.dtel = 9.1 #telescope diameter m
ost.dtel = 10.0 #telescope diameter m

ost.dstel = 0.00 #secondary telescope diameter m
ost.throughput = 0.1
ost.ndark = 0.17 #dark current
ost.nread = 14.0 #nr
ost.fullwell = 80000.

target=exocounts.TargetClass()
target.name="Trappist e"
target.teff = 2500.0 #K
target.rstar = 0.1 #Rsolar
target.dpc = 10 #pc

obs=exocounts.ObsClass(ost,target) 

obs.texposure = 1.0 #cadence [hour] # 30 x visits (1 hr=transit dur trappist e) 
obs.tframe = 7.1  #time for one frame [sec]
obs.napix = 15 # number of the pixels in aperture 
obs.mu = 1 
S=1.8*1.8*np.pi #core size
obs.effnpix = S/3.0 #3 is an approx. increment factor of PSF
obs.mu = 1 

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("photon noise [ppm]=",obs.sign_relative)
print("photon N for exp=",obs.nphoton_exposure)
