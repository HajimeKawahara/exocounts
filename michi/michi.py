import exocounts
import convmag
import diflimit
import numpy as np
from astropy import constants as const
from astropy import units as u

ost=exocounts.InstClass()
michi.lamb =  11.0*u.micron #micron
michi.dlam = 0.5*u.micron #micron
#michi.dtel = 9.1 #telescope diameter m
michi.dtel = 30.0*u.m #telescope diameter m

michi.dstel = 0.00 #secondary telescope diameter m
michi.throughput = 0.8*0.9*0.3 #QE x Efficiency x Inst throughtput
michi.ndark = 0.0 #dark current
michi.nread = 0.0 #nr
michi.fullwell = 80000.

michi.fgtel=0.25/u*s/u*m/u*m/u.arcsec/u.arcsec/u.micron #pt/s/m2/arcsec2/um
michi.fgatm=0.2/u*s/u*m/u*m/u.arcsec/u.arcsec/u.micron #pt/s/m2/arcsec2/um

target=exocounts.TargetClass()
target.name="Tau Ceti Earth"
target.teff = 2559.0 #K
target.rstar = 0.117 #Rsolar
target.dpc = 12.1 #pc

obs=exocounts.ObsClass(ost,target) 

obs.texposure = 30.0 #cadence [hour] # 30 x visits (1 hr=transit dur trappist e) 
obs.tframe = 7.1  #time for one frame [sec]
obs.napix = 15 # number of the pixels in aperture 
obs.mu = 1 
S=1.8*1.8*np.pi #core size
obs.effnpix = S/3.0 #3 is an approx. increment factor of PSF
obs.mu = 1
obs.aparture = diflimit.ld(michi.lamb*u.micron,michi.dtel*u.m))**2*np.pi


obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("photon noise [ppm]=",obs.sign_relative)
print("photon N for exp=",obs.nphoton_exposure)
