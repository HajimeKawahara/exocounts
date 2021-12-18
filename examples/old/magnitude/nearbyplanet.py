import exocounts
import convmag
import nstar
import numpy as np
import planet
from astropy import constants as const
from astropy import units as u

lamMIR=10.47*u.micron
lamNIR=1.5*u.micron
magdict=convmag.get_magdict()

print("=========================")

tauceti=exocounts.TargetClass()
tauceti.name="tau ceti"
print(tauceti.name)
print("-Emission")

tauceti.teff = 255.0*u.K #K ## optimistic (no cloud)
tauceti.rstar = 1.0*const.R_earth
tauceti.d = 3.65*u.pc #pc

fluxB=nstar.getflux(tauceti,lamMIR)
fluxBj=nstar.getfluxJy(tauceti,lamMIR)
fluxBp=nstar.getfluxph(tauceti,lamMIR)

print(fluxB)
print(fluxBj)
print(fluxBp)
print("cts / J",fluxBp.value/fluxB.value)

print("N mag=",convmag.get_mag("N",fluxB,magdict))

print("=========================")

alphacenA=exocounts.TargetClass()
alphacenA.name="alpha cen A"
alphacenA.teff = 255.0*u.K #K ## optimistic (no cloud)
alphacenA.rstar = 1.0*const.R_earth
alphacenA.d = 1.34*u.pc #pc

fluxA=nstar.getflux(alphacenA,lamMIR)
fluxAj=nstar.getfluxJy(alphacenA,lamMIR)

print(alphacenA.name)

print("-Emission")
print(fluxA)
print(fluxAj)
print("N mag=",convmag.get_mag("N",fluxA,magdict))


bernard=exocounts.TargetClass()
bernard.name="Barnard"
bernard.teff = 3210.0*u.K #K ## optimistic (no cloud)
bernard.rstar = 0.196*const.R_sun 
bernard.d = 1.82*u.pc #pc

planet=planet.PlanetClass()
planet.rplanet = 1.0*const.R_earth #Re
planet.a = 0.06*u.AU #AU
planet.albedo = 0.3
planet.phase = np.pi/2.0
planet.compute_reflectivity()
print("Star-Planet Contrast =",planet.reflectivity)

fluxpB=nstar.getflux(bernard,lamNIR)*planet.reflectivity
fluxpBj=nstar.getfluxJy(bernard,lamNIR)*planet.reflectivity
fluxpBp=nstar.getfluxph(bernard,lamNIR)*planet.reflectivity

print(fluxpB)
print(fluxpBj)
print(fluxpBp)

