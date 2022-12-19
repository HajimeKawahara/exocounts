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
#rep



#Table 3
case2=exocounts.InstClass()
case2.dtel = 0.04*u.m #telescope diameter m
case2.dstel = 0.0*u.m #secondary telescope diameter m
case2.throughput = 0.7*0.6

case2.ndark = 2.5/u.s #dark current [e-/pix/s]
case2.nread = 2.4 #nr [e-/pix/read]
case2.fullwell = 1.e7


case2.lamb = 0.6*u.micron #micron
R=6. #Table 3
case2.dlam = case2.lamb/R #micron

target=exocounts.TargetClass()

#HIP41378f
#target.teff = 6251.0*u.K #K #Table 2
#target.rstar = 1.25*const.R_sun #Table 2
#target.d = 106.0*u.pc #pc #Table 3

#TOI 2180
target.teff = 5695.0*u.K #K #Table 2
target.rstar = 1.63*const.R_sun #Table 2
target.d = 116.3*u.pc #pc #Table 3


######
#planet=planet.PlanetClass()
#planet.rplanet = 1.0*const.R_earth #Re
#planet.a = 0.0485*u.AU #AU #Table 2
#planet.albedo = 0.3
#planet.phase = np.pi/2.0
#planet.compute_reflectivity()
#print("Star-Planet Contrast =",planet.reflectivity)

#set planet scattered light as a target
#target.contrast = planet.reflectivity

obs=exocounts.ObsClass(case2,target) 


#
# each side
# 32deg 11.26d for mid M
# 40deg 2.27d for late M
#


obs.texposure = 30.0/60.0/24.0*u.d #30 min
obs.tframe = 1200.0*u.s  #time for one frame [sec]
obs.napix = 1 # number of the pixels in aperture 
obs.mu = 1 
obs.effnpix = 1.0

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("magnitude=",convmag.get_mag("V",obs.flux,magdict))
print(obs.nphoton_brightest/case2.fullwell)
print(obs.sat)
print("photon/pix/frame=",obs.nphoton_frame)
print("shot noise (sigma) in total=",obs.sign_relative*1.e-6)
print("shot noise (dark) in total=",obs.sigd_relative*1.e-6)
print("shot noise (read) in total=",obs.sigr_relative*1.e-6)
