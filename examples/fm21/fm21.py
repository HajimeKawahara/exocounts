from exocounts import exocounts
from exocounts import planet
from exocounts import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np

#
#
# each side
# 32deg 11.26d for mid M
# 40deg 2.27d for late M
#



#Table 3
fm21=exocounts.InstClass()
fm21.dtel = 6.5*u.m #telescope diameter m
fm21.dstel = 0.00*u.m #secondary telescope diameter m
fm21.throughput = 0.15

fm21.ndark = 0.2/u.s #dark current [e-/pix/s]
fm21.nread = 14.0 #nr [e-/pix/read]
fm21.fullwell = 1.e7


fm21.lamb = 10.0*u.micron #micron
R=30000. #Table 3
fm21.dlam = fm21.lamb/R #micron

target=exocounts.TargetClass()
#mid M
#target.teff = 3000.0*u.K #K #Table 2
#target.rstar = 0.14*const.R_sun #Table 2
#late M
target.teff = 2500.0*u.K #K #Table 2
target.rstar = 0.1*const.R_sun #Table 2
target.d = 5.0*u.pc #pc #Table 3


######
planet=planet.PlanetClass()
planet.rplanet = 1.0*const.R_earth #Re
planet.a = 0.0485*u.AU #AU #Table 2
planet.albedo = 0.3
planet.phase = np.pi/2.0
#planet.compute_reflectivity()
print("Star-Planet Contrast =",planet.reflectivity)

#set planet scattered light as a target
#target.contrast = planet.reflectivity

obs=exocounts.ObsClass(fm21,target) 


#
# each side
# 32deg 11.26d for mid M
# 40deg 2.27d for late M
#


obs.texposure = 40.0/360.0*2.27*u.d
obs.tframe = 1800.0*u.s  #time for one frame [sec]
obs.napix = 1 # number of the pixels in aperture 
obs.mu = 1 
obs.effnpix = 1.0

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("magnitude=",convmag.get_mag("V",obs.flux,magdict))
print(obs.nphoton_brightest/fm21.fullwell)
print(obs.sat)
print("photon/pix/frame=",obs.nphoton_frame)
print("shot noise (sigma) in total=",obs.sign_relative*1.e-6)
print("shot noise (dark) in total=",obs.sigd_relative*1.e-6)
print("shot noise (read) in total=",obs.sigr_relative*1.e-6)
