#!/usr/bin/python
import sys
import argparse
import numpy as np
from io import StringIO
import csv
from astropy import constants as const
from astropy import units as u
import magflux

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

def Nstar(Inst,Target,Obs,info=False):
    tstar=Target.teff*u.K    
    lamin=Inst.lamb*u.micron
    d=Target.dpc*u.pc
    runit=const.R_sun            
    r=Target.rstar*runit        
    flux=np.pi*Blunitless(tstar,lamin)*r*r/(d*d)
    photonf=np.pi*photon_Blunitless(tstar,lamin)*r*r/(d*d)
    a=np.pi*(Inst.dtel/2.0*u.m)**2 - np.pi*(Inst.dstel/2.0*u.m)**2
    dl=Inst.dlam*u.micron
    texp=Inst.tcadence*u.h
    photon=photonf*a*dl*texp*Inst.throughput
    
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
        print("  exposure", Inst.tcadence,"[hour] = ",Inst.tcadence*60.0," [min]")
        print("  throughput", Inst.throughput)
        print("N=",'{:e}'.format(photon.to(1)))
        print("photon noise 1/sqrt(N)=",np.sqrt(1.0/photon.to(1))*1e6,"[ppm]")
        print("photon noise 1/sqrt(N)=",np.sqrt(1.0/photon.to(1))*1e2,"[%]")
        print("7 sigma depth=",np.sqrt(1.0/photon.to(1))*1e2*7.0,"[%]")

    Nphoton=photon.to(1)
    Obs.nphoton_cadence=Nphoton
    Obs.nphoton_frame = Nphoton*(Inst.tframe/(Inst.tcadence*3600))
    Obs.sign=np.sqrt(Nphoton)