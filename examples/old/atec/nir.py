import exocounts
import convmag
import numpy as np
from astropy import constants as const
from astropy import units as u

atec=exocounts.InstClass()
atec.lamb =  1.7*u.micron #micron
R=100000.0
atec.dlam = atec.lamb/R #micron
#atec.dtel = 9.1 #telescope diameter m
atec.dtel = 2.0*u.m #telescope diameter m

atec.dstel = 0.00*u.m #secondary telescope diameter m
atec.throughput = 0.05
atec.ndark = 0.17/u.s #dark current
atec.nread = 14.0 #nr
atec.fullwell = 80000.

target=exocounts.TargetClass()
target.name="HR8799bcde"
target.teff = 1000.0*u.K #K
target.rstar = 0.1*const.R_sun  #Rsolar
target.d = 39*u.pc #pc

obs=exocounts.ObsClass(atec,target) 

obs.texposure = 1.0*24.0*1.0*u.h #1 d
obs.tframe = 7.1*u.s  #time for one frame [sec]
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
print("photon S/N for exp=",np.sqrt(obs.nphoton_exposure))
