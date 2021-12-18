import exocounts
import planet
import convmag
import nstar
import pandas as pd
import matplotlib.pyplot as plt
from astropy import constants as const
from astropy import units as u
from astropy.coordinates import SkyCoord
import diflimit
import numpy as np

dat=pd.read_csv("nearby_updateA.txt",delimiter="|")
NIR=1.26*u.micron
TelD=30.*u.m
fig=plt.figure()
for i in range(0,len(dat["name"])):
#    if True:
    try:
        star=exocounts.TargetClass()
        star.name=dat["name"][i]
        star.teff = dat["t"][i]*u.K #K ## optimistic (no cloud)
        star.rstar = dat["r"][i]*const.R_sun        
        star.d = dat["dpc"][i]*u.pc #pc
        
        exoplanet=planet.PlanetClass()
        exoplanet.rplanet = 1.0*const.R_earth #Re
        exoplanet.a =float(dat["amin"][i])*u.AU #AU
        exoplanet.albedo = 0.3
        exoplanet.phase = np.pi/2.0
        exoplanet.compute_reflectivity()
        print("Star-Planet Contrast =",exoplanet.reflectivity)
        contrast=exoplanet.reflectivity
        
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
        plt.plot([sep],[contrast],"o",color=col)
            
        if str(dat["propername"][i])=="nan":
            plt.text(sep,contrast,dat["name"][i],color=col,alpha=0.5,fontsize=13)
        else:
            plt.text(sep,contrast,dat["propername"][i],color=col,alpha=0.5,fontsize=13)
        print("OK:",dat["name"][i])

    except:
        print("Error:",dat["name"][i])

for i in range(1,4):
    ld=(diflimit.ld(NIR,TelD))
    plt.axvline(i*(ld.value),alpha=0.5,ls="dashed")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("Separation [arcsec]",fontsize=18)
plt.ylabel("Contrast",fontsize=18)
plt.xlim(3.e-3,1.e1)

plt.ylim(3.e-10,3.e-5)
plt.tick_params(labelsize=18)
plt.show()
