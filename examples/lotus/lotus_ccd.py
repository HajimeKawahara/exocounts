from exocounts.exocounts import exocounts
from exocounts.exocounts import convmag
from astropy import constants as const
from astropy import units as u

import numpy as np

lotus=exocounts.InstClass()
lotus.lamb = 0.7 #micron
lotus.dlam = 0.4 #micron
lotus.dtel = 0.075 #telescope diameter m
lotus.dstel = 0.00 #secondary telescope diameter m
lotus.throughput = 0.7
lotus.ndark = 0.3 #dark current [e-/pix/s]
lotus.nread = 7.0 #nr [e-/pix/read]
lotus.fullwell = 1.e6

target=exocounts.TargetClass()
target.teff = 6000.0 #K
target.rstar = 1.0 #Rsolar
target.d = 300.0*u.pc #pc

obs=exocounts.ObsClass(lotus,target) 

obs.texposure = 0.3 #=18min cadence [hour]
obs.tframe = 6.0  #time for one frame [sec]
obs.napix = 10 # number of the pixels in aperture 
obs.mu = 1 
obs.effnpix = 0.5

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("magnitude=",convmag.get_mag("V",obs.flux,magdict))

print(obs.nphoton_brightest/lotus.fullwell)
print(obs.sat)
print("shot noise (sigma)=",obs.sign)
print("shot noise (dark)=",obs.sigd)
print("shot noise (read)=",obs.sigr)
