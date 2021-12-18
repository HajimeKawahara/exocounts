import exocounts
import convmag
import nstar
import pandas as pd
import matplotlib.pyplot as plt
from astropy import constants as const
from astropy import units as u
from astropy.coordinates import SkyCoord
import diflimit

dat=pd.read_csv("nearby_updateA.txt",delimiter="|")
MIR=10.47*u.micron
TelD=30.*u.m
fig=plt.figure()
for i in range(0,len(dat["name"])):
#    if True:
    try:
        star=exocounts.TargetClass()
        star.name=dat["name"][i]
#        star.teff = dat["t"][i]*u.K #K ## optimistic (no cloud)
        star.teff = 255.0*u.K #K ## optimistic (no cloud)
#        star.rstar = dat["r"][i]*const.R_sun        
        star.rstar = 1.0*const.R_earth
        star.d = dat["dpc"][i]*u.pc #pc
        flux=nstar.getflux(star,MIR)
        fluxc=(flux.value)
        ra=str(dat["ra"][i])
        dec=str(dat["dec"][i])
        radec=ra+" "+dec
        c = SkyCoord(radec, unit=(u.hourangle, u.deg))
        decdeg=(c.dec.degree)
        amin=dat["amin"][i]
        d=dat["dpc"][i]
        sep=float(amin)/float(d)
        if decdeg > -40:
            col="C1"
        else:
            col="gray"
        plt.plot([sep],[fluxc],"o",color=col)
            
        if str(dat["propername"][i])=="nan":
            plt.text(sep,fluxc,dat["name"][i],color=col,alpha=0.5,fontsize=13)
        else:
            plt.text(sep,fluxc,dat["propername"][i],color=col,alpha=0.5,fontsize=13)
        print("OK:",dat["name"][i])

    except:
        print("Error:",dat["name"][i])

for i in range(1,4):
    ld=(diflimit.ld(MIR,TelD))
    plt.axvline(i*(ld.value),alpha=0.5,ls="dashed")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Separation [arcsec]",fontsize=18)
plt.ylabel("Flux [J/s/m2/um]",fontsize=18)
plt.xlim(3.e-3,1.e1)

plt.ylim(3.e-21,3.e-17)
plt.tick_params(labelsize=18)
plt.show()
