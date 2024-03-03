from exocounts import exocounts
from exocounts import planet
from exocounts import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np
mlist = convmag.get_magdict()
center = [mlist["lambda0"][5], mlist["lambda0"][6]]
bandarr = [mlist["band"][5], mlist["band"][6]]
print(bandarr)
for i, center_lambda in enumerate(center):
    band=exocounts.InstClass()
    band.lamb = center_lambda*u.micron #micron
    band.dlam = 0.1*u.micron #micron
    band.dtel = 4.0*u.m #telescope diameter m
    band.dstel = 0.00*u.m #secondary telescope diameter m
    band.throughput = 0.3
    band.ndark = 3.e-5/u.s #dark current [e-/pix/s]
    band.nread = 0.008 #nr [e-/pix/read]
    band.fullwell = 1.e7
    
    target=exocounts.TargetClass()
    target.teff = 5500.0*u.K #K
    target.rstar = 1.0*const.R_sun #Rsolar
    target.d = 10.0*u.pc #pc
    
    obs=exocounts.ObsClass(band,target) 
    obs.texposure = 1.0*u.h #= [hour]
    obs.tframe = 10.0*u.s  #time for one frame [sec]
    obs.napix = 1 # number of the pixels in aperture 
    obs.mu = 1 
    obs.effnpix = 0.5    
    obs.target = target
    obs.update()
    
    magdict=convmag.get_magdict()
    mag = bandarr[i]
    print(mag+" band magnitude=",convmag.get_mag(mag,obs.flux,magdict))

#print("magnitude=",convmag.get_mag("H",obs.flux,magdict))
