import exocounts
import planet
import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np

habex=exocounts.InstClass()
habex.lamb = 0.5*u.micron #micron
habex.dlam = 0.1*u.micron #micron
habex.dtel = 4.0*u.m #telescope diameter m
habex.dstel = 0.00*u.m #secondary telescope diameter m
habex.throughput = 0.3
habex.ndark = 3.e-5/u.s #dark current [e-/pix/s]
habex.nread = 0.008 #nr [e-/pix/read]
habex.fullwell = 1.e7

target=exocounts.TargetClass()
target.teff = 5800.0*u.K #K
target.rstar = 1.0*const.R_sun #Rsolar
target.d = 5.0*u.pc #pc

planet=planet.PlanetClass()
planet.rplanet = 1.0*const.R_earth #Re
planet.a = 1.0*u.AU #AU
planet.albedo = 0.3
planet.phase = np.pi/2.0
planet.compute_reflectivity()
print("Star-Planet Contrast =",planet.reflectivity)

#set planet scattered light as a target
target.contrast = planet.reflectivity

obs=exocounts.ObsClass(habex,target) 

obs.texposure = 1.0*u.h #= [hour]
obs.tframe = 10.0*u.s  #time for one frame [sec]
obs.napix = 1 # number of the pixels in aperture 
obs.mu = 1 
obs.effnpix = 0.5

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("magnitude=",convmag.get_mag("V",obs.flux,magdict))
print(obs.nphoton_brightest/habex.fullwell)
print(obs.sat)
print("photon/pix/frame=",obs.nphoton_frame)
print("shot noise (sigma)=",obs.sign_relative*1.e-6)
print("shot noise (dark)=",obs.sigd_relative*1.e-6)
print("shot noise (read)=",obs.sigr_relative*1.e-6)
