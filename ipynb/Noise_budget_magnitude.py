# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 0.8.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
#   language_info:
#     codemirror_mode:
#       name: ipython
#       version: 3
#     file_extension: .py
#     mimetype: text/x-python
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#     version: 3.6.5
# ---

# %load_ext autoreload
# %autoreload 2
import nstar
import nreadout
import ndark
import readspec
import argparse
import convmag
import numpy as np
import matplotlib.pyplot as plt
import pylab



specfile="/home/kawahara/exocal/exocounts/ejas.txt"
case="A"
dat=readspec.readspec(specfile,case=case)
stellar_temperature,lambda_micron,dpc,rsol,dtel,dstel,dlam_micron,throughput,th,nd,npix,tr,nr,mu,b=readspec.expanddat(dat,case)

flux,photonf,Nphoton,sign=nstar.Nstar(lambda_micron,stellar_temperature,rsol,dpc,dtel,dstel,dlam_micron,throughput,th,info=False)
sigd=ndark.Ndark(th,nd,npix,mu)
sigr=nreadout.Nreadout(th,tr,nr,npix,mu,mode="linear")

print("band:",b)
magdict=convmag.get_magdict()
print("magnitude=",convmag.get_mag(b,flux,magdict))
print("star,dark,readout")
print(sign,sigd,sigr)

Nread=(th*3600)/tr
Nave=Nphoton/Nread/npix
print("Average photon counts: e-/pix/read: ",Nave)

print("[ppm] star,dark,readout")
Ntot=Nphoton
ppm=1.e6
print(sign/Ntot*ppm,sigd/Ntot*ppm,sigr/Ntot*ppm)

# +
darr=np.linspace(10,30,21)
sigsarr=[]
sigdarr=[]
sigrarr=[]
magarr=[]
Navearr=[]
Nread=(th*3600)/tr

for dpc in darr:
    flux,photonf,Nphoton,sign=nstar.Nstar(lambda_micron,stellar_temperature,rsol,dpc,dtel,dstel,dlam_micron,throughput,th,info=False)
    Nave=Nphoton/Nread/npix
    Navearr.append(Nave)
    Ntot=Nphoton
    sigsarr.append(sign/Ntot*ppm)
    sigdarr.append(ndark.Ndark(th,nd,npix,mu)/Ntot*ppm)
    sigrarr.append(nreadout.Nreadout(th,tr,nr,npix,mu,mode="linear")/Ntot*ppm)
    magarr.append(convmag.get_mag(b,flux,magdict))
sigsarr=np.array(sigsarr)
sigdarr=np.array(sigdarr)
sigrarr=np.array(sigrarr)
Navearr=np.array(Navearr)
# -

S=1.8*1.8*np.pi
ind=np.searchsorted(3*Navearr[::-1]*npix/S,80000.0)
ind=21-ind
print(3*Navearr[ind]*npix/S)
print(magarr[ind])

3*Navearr

# +
fig=plt.figure(figsize=(7,5))

ax=fig.add_subplot(211)
ax.plot(magarr,sigsarr,label="shot noise")
ax.plot(magarr,sigdarr,label="dark noise",ls="dotted")
ax.plot(magarr,sigrarr,label="read noise",ls="dashed")
pylab.legend()
pylab.xlim(9.,10.9)
pylab.ylim(0,600)
ax.fill([9,9.5,9.5,9.0,9.0],[0,0,600,600,0],alpha=0.3,color="gray")
for i,dpc in enumerate(darr):
    if np.mod(dpc,5)==0:
        plt.axvline(magarr[i],ls="dashed",color="gray",alpha=0.3)
plt.ylabel("noise for 5 min (ppm)")

ax=fig.add_subplot(212)
ax.plot(magarr,np.sqrt(sigsarr**2 + sigdarr**2 + sigrarr**2)/ppm*7*100)
pylab.xlim(9.,10.9)
pylab.ylim(0,0.5)
ax.fill([9,9.5,9.5,9.0,9.0],[0,0,1,1,0],alpha=0.3,color="gray")
plt.axhline(0.35,color="gray",alpha=0.2,c="orange")
for i,dpc in enumerate(darr):
    if np.mod(dpc,5)==0 and dpc>10:
        plt.axvline(magarr[i],ls="dashed",color="gray",alpha=0.3)
        plt.text(magarr[i],0.05,str(int(dpc))+"pc",horizontalalignment="center")
plt.xlabel("H-band magnitude")
plt.ylabel("depth for 7 sigma \n limit in 5 min [%]")
plt.savefig("noise.png")
plt.savefig("noise.pdf", bbox_inches="tight", pad_inches=0.0)


# +
#1.8 pix = 1.22 l/d
#l/d = 1.48 pix
#sigma = 0.437 l/d = 0.65 pixの2D Gaussianにだいたい対応


# +
#Integrate[r Exp[-r^2/(2*0.65*0.65)],{r,0,Infty}]=0.4225
#Integrate[r Exp[-r^2/(2*0.65*0.65)],{r,0,0.5}]/(0.5*0.5*pi)= 0.13
# -

0.13/0.4225

0.13/0.4225*S

# +
#Integrate[r Exp[-r^2],{r,0,0.28}]/(0.28*0.28*3.14)*2*3.14 = 0.96
