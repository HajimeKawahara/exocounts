from exocounts import exocounts
from exocounts import planet
from exocounts import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np

tmt=exocounts.InstClass()
tmt.lamb = 0.63*u.micron #micron
tmt.dlam = tmt.lamb*1.e-5 # line width micron

tmt.dtel = 30.0*u.m #telescope diameter m
tmt.dstel = 0.00*u.m #secondary telescope diameter m
tmt.throughput = 0.1 #10% throughput 
tmt.ndark = 3.e-5/u.s #dark current [e-/pix/s]
tmt.nread = 0.008 #nr [e-/pix/read]
tmt.fullwell = 1.e7

target=exocounts.TargetClass()
target.teff = 3000.0*u.K #K
target.rstar = 0.2*const.R_sun #Rsolar
target.d = 5.0*u.pc #pc


target.contrast = 1.e-5 #contrast

obs=exocounts.ObsClass(tmt,target) 

obs.texposure = 1.0*u.h # exposure [hour]
obs.tframe = 10.0*u.s  #time for one frame [sec]
obs.napix = 1 # number of the pixels in aperture 
obs.mu = 1 
obs.effnpix = 0.5

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("magnitude=",convmag.get_mag("V",obs.flux,magdict))
print(obs.nphoton_brightest/tmt.fullwell)
