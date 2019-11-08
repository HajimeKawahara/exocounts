import exocounts
import convmag
import diflimit
import nstar
import numpy as np
from astropy import constants as const
from astropy import units as u

michi=exocounts.InstClass()
michi.lamb =  10.0*u.micron #micron
michi.dlam = 1.0*u.micron #micron
#michi.dtel = 9.1 #telescope diameter m
michi.dtel = 30.0*u.m #telescope diameter m

michi.dstel = 0.00*u.m #secondary telescope diameter m
michi.throughput = 0.8*0.9*0.3 #QE x Efficiency x Inst throughtput
michi.ndark = 0.0/u.s #dark current [1/s]
michi.nread = 0.0 #nr
michi.fullwell = 80000.

fgunit=u.s*u.m*u.m*u.arcsec*u.arcsec*u.micron
michi.fgtel=0.05*1e10/fgunit #pt/s/m2/arcsec2/um
michi.fgatm=0.05*1e10/fgunit #pt/s/m2/arcsec2/um

target=exocounts.TargetClass()
target.name="Tau Ceti Earth"
target.teff = 300.0*u.K #K ## optimistic (no cloud)
target.rstar = 1.0*const.R_earth 

tau_ceti_teff = 5344.0*u.K #K ## optimistic (no cloud)
tau_ceti_rstar = 0.79*const.R_sun 



c=(((target.rstar)**2*nstar.Blunitless(target.teff,michi.lamb))/(nstar.Blunitless(tau_ceti_teff,michi.lamb)*(tau_ceti_rstar)**2)).to(1)
print("contrast=",c)

target.d = 3.65*u.pc #pc

obs=exocounts.ObsClass(michi,target) 

obs.texposure = 30.0*u.h #cadence [hour] # 30 x visits (1 hr=transit dur trappist e) 
obs.tframe = 7.1*u.s  #time for one frame [sec]
obs.napix = 15 # number of the pixels in aperture 
obs.mu = 1 
S=1.8*1.8*np.pi #core size
obs.effnpix = S/3.0 #3 is an approx. increment factor of PSF
obs.mu = 1
obs.fgaparture = ((diflimit.ld(michi.lamb,michi.dtel))/2.0)**2*np.pi

obs.target = target
obs.update()

magdict=convmag.get_magdict()
print("photon count for foreground",obs.nphoton_foreground)
print("photon count signal for exp=",obs.nphoton_exposure)

print("S/N for Nsig/sqrt(Nthermal)",obs.nphoton_exposure/np.sqrt(obs.nphoton_foreground))


print("Contrast for/sig (log)",np.log10(obs.nphoton_foreground/obs.nphoton_exposure))
print("Contrast for/sig ",(obs.nphoton_foreground/obs.nphoton_exposure))

magdict=convmag.get_magdict()
print("N mag=",convmag.get_mag("N",obs.flux,magdict))

#print("photon noise [ppm]=",obs.sign_relative)
