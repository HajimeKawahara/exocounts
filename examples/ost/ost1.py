from exocounts import exocounts
from exocounts import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np

ost=exocounts.InstClass()
ost.lamb =  10.0*u.micron #micron
ost.dlam = 0.25*u.micron #micron
#ost.dtel = 9.1 #telescope diameter m
ost.dtel = 5.9*u.m #telescope diameter m

ost.dstel = 0.00*u.m #secondary telescope diameter m
ost.throughput = 0.1
ost.ndark = 0.17 #dark current
ost.nread = 14.0 #nr
ost.fullwell = 80000.

target=exocounts.TargetClass()
target.name="Trappist e"
target.teff = 2559.0*u.K #K
target.rstar = 0.117*const.R_sun #Rsolar
target.d = 12.1*u.pc #pc

obs=exocounts.ObsClass(ost,target) 

obs.texposure = 30.0*u.h #cadence [hour] # 30 x visits (1 hr=transit dur trappist e) 
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
