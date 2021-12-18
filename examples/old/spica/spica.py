import exocounts
import convmag

import numpy as np

spica=exocounts.InstClass()
spica.lamb =  15.0 #micron
spica.dlam = 10.0 #micron
spica.dtel = 2.5 #telescope diameter m
spica.dstel = 0.00 #secondary telescope diameter m
spica.throughput = 0.2
spica.ndark = 0.17 #dark current
spica.nread = 14.0 #nr
spica.fullwell = 80000.

target=exocounts.TargetClass()
target.teff = 5800.0 #K
target.rstar = 1.0 #Rsolar
target.dpc = 10.0 #pc

obs=exocounts.ObsClass(spica,target) 

obs.texposure = 1.0 #cadence [hour]
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
