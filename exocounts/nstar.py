#!/usr/bin/python
import sys
import argparse
import numpy as np
from io import StringIO
import csv
from astropy import constants as const
from astropy import units as u

def Blambda(T,lamb):
    lamb5=(lamb.to(u.m))**5    
    fac=const.h*const.c/(lamb.to(u.m)*const.k_B*T)
    bl=2.0*(const.c**2)*const.h/lamb5/(np.exp(fac)-1)
    return bl.to(u.erg/u.cm/u.cm/u.angstrom/u.s)

def Blunitless(T,lamb):
    lamb5=(lamb.to(u.m))**5    
    fac=const.h*const.c/(lamb.to(u.m)*const.k_B*T)
    bl=2.0*(const.c**2)*const.h/lamb5/(np.exp(fac)-1)
    return bl


def photon_Blunitless(T,lamb):
    pB=Blambda(T,lamb)/(const.h*const.c/(lamb.to(u.m)))

    return pB

def Nstar(Inst,Target,Obs,info=False,integrate=True,Nintegrate=128):
    tstar=Target.teff    
    lamin=Inst.lamb
    d=Target.d
    r=Target.rstar
    texp=Obs.texposure
    a=np.pi*(Inst.dtel/2.0)**2 - np.pi*(Inst.dstel/2.0)**2
    dl=Inst.dlam
    contrast = Target.contrast
    if integrate:
        ddl=dl/Nintegrate
        lamarr=lamin+np.linspace(-dl/2,dl/2,Nintegrate)
        fluxarr=[]
        photonfarr=[]
        photonarr=[]
        for j,lamlow in enumerate(lamarr[:-1]):
            lamc=(lamarr[j+1]+lamlow)/2.0
            dll=lamarr[j+1]-lamlow
            flux=np.pi*Blunitless(tstar,lamc)*r*r/(d*d)*contrast
            photonf=np.pi*photon_Blunitless(tstar,lamc)*r*r/(d*d)*contrast
            photon=photonf*a*dll*texp*Inst.throughput
            fluxarr.append(flux)
            photonfarr.append(photonf)
            photonarr.append(photon)

        photon=np.sum(photonarr)
    else:
        flux=np.pi*Blunitless(tstar,lamin)*r*r/(d*d)*contrast
        photonf=np.pi*photon_Blunitless(tstar,lamin)*r*r/(d*d)*contrast
        photon=photonf*a*dl*texp*Inst.throughput
        photon=photon.to(1)
        
    flux=np.pi*Blunitless(tstar,lamin)*r*r/(d*d)*contrast
    photonf=np.pi*photon_Blunitless(tstar,lamin)*r*r/(d*d)*contrast
        
    if info:
        print("B(lambda) for",tstar,"at ",lamin)
        print('{:e}'.format(Blunitless(tstar,lamin).to(u.erg/u.cm/u.cm/u.angstrom/u.s)))
        print('{:e}'.format(Blunitless(tstar,lamin).to(u.erg/u.cm/u.cm/u.micron/u.s)))
        print('{:e}'.format(Blunitless(tstar,lamin).to(u.J/u.m/u.m/u.m/u.s)))
        print("---------------------")
        print("FLUX from a sphere with r=",Target.rstar,"[Rsol] and","dpc=",d,"[pc]")
        print(flux.to(u.erg/u.cm/u.cm/u.micron/u.s))
        print("Photon FLUX from a sphere with  r=",Target.rstar,"[Rsol] and","dpc=",d,"[pc]")
        print(photonf.to(1/u.cm/u.cm/u.micron/u.s))
        print("---------------------")
        print("Photon Count with observation:")
        print("  telescope diameter", Inst.dtel, "[m]")
        print("  band width", Inst.dlam,"[micron]")
        print("  exposure", Obs.texposure,"[hour] = ",Obs.texposure.to(u.min)," [min]")
        print("  throughput", Inst.throughput)
        print("N=",'{:e}'.format(photon.to(1)))
        print("photon noise 1/sqrt(N)=",np.sqrt(1.0/photon.to(1))*1e6,"[ppm]")
        print("photon noise 1/sqrt(N)=",np.sqrt(1.0/photon.to(1))*1e2,"[%]")
        print("7 sigma depth=",np.sqrt(1.0/photon.to(1))*1e2*7.0,"[%]")

    Nphoton=photon
    Obs.nphoton_exposure=Nphoton
    Obs.nphoton_frame = Nphoton*(Obs.tframe/Obs.texposure).to(1)
    Obs.sign=np.sqrt(Nphoton)
    Obs.flux = flux
    Obs.photonf= photonf
    ppm=1.e6
    Obs.sign_relative = Obs.sign/Obs.nphoton_exposure*ppm
