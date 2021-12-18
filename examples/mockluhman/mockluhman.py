import exocounts
import planet
import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np

SUBARU=exocounts.InstClass()
SUBARU.lamb = 2.3*u.micron #micron
R=100000.0
SUBARU.dlam = 2.3/R*u.micron #micron
SUBARU.dtel = 8.2*u.m #telescope diameter m
SUBARU.dstel = 0.00*u.m #secondary telescope diameter m
SUBARU.throughput = 0.05
SUBARU.ndark = 0.0/u.s #dark current [e-/pix/s]
SUBARU.nread = 0.00 #nr [e-/pix/read]
SUBARU.fullwell = 1.e7

target=exocounts.TargetClass()
target.teff = 1300.0*u.K #K
target.rstar = 0.1*const.R_sun #Rsolar
target.d = 40.0*u.pc #pc


obs=exocounts.ObsClass(SUBARU,target) 

obs.texposure = 1.0*u.h #= [hour]
obs.tframe = 10.0*u.s  #time for one frame [sec]
obs.napix = 1 # number of the pixels in aperture 
obs.mu = 1 
obs.effnpix = 0.5

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("magnitude=",convmag.get_mag("V",obs.flux,magdict))
print(obs.nphoton_brightest/SUBARU.fullwell)
print(obs.sat)
print("photon/pix/frame=",obs.nphoton_frame)
print("shot noise (sigma)=",obs.sign_relative*1.e-6)
print("shot noise (dark)=",obs.sigd_relative*1.e-6)
print("shot noise (read)=",obs.sigr_relative*1.e-6)
