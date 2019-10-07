import exocounts
import planet
import convmag

import numpy as np

habex=exocounts.InstClass()
habex.lamb = 0.5 #micron
habex.dlam = 0.1 #micron
habex.dtel = 4.0 #telescope diameter m
habex.dstel = 0.00 #secondary telescope diameter m
habex.throughput = 0.3
habex.ndark = 2.e-5 #dark current [e-/pix/s]
habex.nread = 0.008 #nr [e-/pix/read]
habex.fullwell = 1.e7

target=exocounts.TargetClass()
target.teff = 5800.0 #K
target.rstar = 1.0 #Rsolar
target.dpc = 5.0 #pc

planet=planet.PlanetClass()
planet.rplanet = 1.0 #Re
planet.a = 1.0 #AU
planet.albedo = 0.3
planet.phase = np.pi/2.0
planet.compute_reflectivity()
print("Star-Planet Contrast =",planet.reflectivity)

#set planet scattered light as a target
target.contrast = planet.reflectivity

obs=exocounts.ObsClass(habex,target) 

obs.texposure = 1.0 #= [hour]
obs.tframe = 10.0  #time for one frame [sec]
obs.napix = 72 # number of the pixels in aperture 
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
