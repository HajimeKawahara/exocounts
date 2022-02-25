from exocounts import exocounts
from exocounts import convmag

from astropy import units as u
from astropy import constants as const

import matplotlib.pyplot as plt
import pylab
import numpy as np

ejas=exocounts.InstClass()
ejas.lamb = 1.35*u.micron #micron
ejas.dlam = 0.5*u.micron #micron
ejas.dtel = 0.35*u.m #telescope diameter m
ejas.dstel = 0.14*u.m #secondary telescope diameter m or 12.4 (3 tels)
ejas.throughput = 0.8
ejas.ndark = 15.5/u.s #dark current
ejas.nread = 15.0 #nr
ejas.fullwell = 150000.

target=exocounts.TargetClass()
target.teff = 3000.0*u.K #K
target.rstar = 0.2*const.R_sun #Rsolar
target.d = 15.0*u.pc #pc

obs=exocounts.ObsClass(ejas,target) 

obs.texposure = 0.0833*u.h #cadence [hour]
obs.tframe = 12.5*u.s  #time for one frame [sec]
obs.napix = 15 # number of the pixels in aperture 
obs.mu = 1 
S=1.8*1.8*np.pi #core size
obs.effnpix = S/3.0 #3 is an approx. increment factor of PSF
obs.mu = 1 

shot=[]
dark=[]
read=[]
H=[]
J=[]
Hw=[]
darr=np.linspace(5,35,91)
magdict=convmag.get_magdict()
for distpc in darr:
    target.d=distpc*u.pc #change targets
    obs.target = target
    obs.update()
    Htmp=convmag.get_mag("H",obs.flux,magdict)
    Jtmp=convmag.get_mag("J",obs.flux,magdict)
    Hwtmp=0.7*Jtmp + 0.3*Htmp
    H.append(Htmp)
    J.append(Jtmp)
    Hw.append(Hwtmp)
    #print(distpc,convmag.get_mag("H",obs.flux,magdict))
    if obs.sat:
        satmag=[Hwtmp,Htmp,Jtmp]
    dark.append(obs.sigd_relative)
    read.append(obs.sigr_relative)
    shot.append(obs.sign_relative)
    
sigsarr_relative=np.array(shot)
sigdarr_relative=np.array(dark)
sigrarr_relative=np.array(read)
magarr=np.array(Hw)

fig=plt.figure(figsize=(7,5))

ax=fig.add_subplot(211)
ax.plot(magarr,sigsarr_relative,label="shot noise")
ax.plot(magarr,sigdarr_relative,label="dark noise",ls="dotted")
ax.plot(magarr,sigrarr_relative,label="read noise",ls="dashed")
pylab.legend()
pylab.xlim(8.5,12.0)
pylab.ylim(0,600)
#ax.fill([10,satmag[0],satmag[0],10.0,10.0],[0,0,600,600,0],alpha=0.3,color="gray")
for i,dpc in enumerate(darr):
    if np.mod(dpc,5)==0:
        plt.axvline(magarr[i],ls="dashed",color="gray",alpha=0.3)
plt.ylabel("noise for 5 min (ppm)")
ppm=1.e6

ax=fig.add_subplot(212)
ax.plot(magarr,np.sqrt(sigsarr_relative**2 + sigdarr_relative**2 + sigrarr_relative**2)/ppm*7*100)
pylab.xlim(8.5,12.0)
pylab.ylim(0,0.5)
#ax.fill([10,satmag[0],satmag[0],10.0,10.0],[0,0,1,1,0],alpha=0.3,color="gray")
plt.axhline(0.35,color="gray",alpha=0.2,c="orange")

for i,dpc in enumerate(darr):
    if np.mod(dpc,5)==0 and dpc>=10:
        plt.axvline(magarr[i],ls="dashed",color="gray",alpha=0.3)
        plt.text(magarr[i],0.05,str(int(dpc))+"pc",horizontalalignment="center")
plt.xlabel("Hw-band magnitude")
plt.ylabel("depth for 7 sigma \n limit in 5 min [%]")
plt.savefig("noise.png")
plt.savefig("noise.pdf", bbox_inches="tight", pad_inches=0.0)
plt.show()
