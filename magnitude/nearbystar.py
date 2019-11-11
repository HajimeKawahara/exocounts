import exocounts
import convmag
import nstar
import numpy as np
from astropy import constants as const
from astropy import units as u

magdict=convmag.get_magdict()

alphacenA=exocounts.TargetClass()
alphacenA.name="alpha cen A"
alphacenA.teff = 5790.0*u.K #K ## optimistic (no cloud)
alphacenA.rstar = 1.2234*const.R_sun
alphacenA.d = 1.34*u.pc #pc

fluxA=nstar.getflux(alphacenA,10.47*u.micron)

print(alphacenA.name)
print(fluxA)
print("N mag=",convmag.get_mag("N",fluxA,magdict))


alphacenB=exocounts.TargetClass()
alphacenB.name="alpha cen B"
alphacenB.teff = 5260.0*u.K #K ## optimistic (no cloud)
alphacenB.rstar = 0.8632*const.R_sun
alphacenB.d = 1.34*u.pc #pc

fluxB=nstar.getflux(alphacenB,10.47*u.micron)

print(alphacenB.name)
print(fluxB)
print("N mag=",convmag.get_mag("N",fluxB,magdict))


tauceti=exocounts.TargetClass()
tauceti.name="tau ceti"
tauceti.teff = 5344.0*u.K #K ## optimistic (no cloud)
tauceti.rstar = 0.79*const.R_sun 
tauceti.d = 3.65*u.pc #pc

fluxB=nstar.getflux(tauceti,10.47*u.micron)

print(tauceti.name)
print(fluxB)
print("N mag=",convmag.get_mag("N",fluxB,magdict))