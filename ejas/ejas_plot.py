from exocounts.exocounts import exocounts
from exocounts.exocounts import convmag
import matplotlib.pyplot as plt
import pylab
import numpy as np

ejas=exocounts.InstClass()
ejas.lamb = 1.4 #micron
ejas.dlam = 0.6 #micron
ejas.dtel = 0.31 #telescope diameter m
ejas.dstel = 0.09 #secondary telescope diameter m
ejas.throughput = 0.7
ejas.ndark = 60.0 #dark current
ejas.nread = 30.0 #nr
ejas.fullwell = 80000.

target=exocounts.TargetClass()
target.teff = 3000.0 #K
target.rstar = 0.2 #Rsolar
target.dpc = 15.0 #pc

obs=exocounts.ObsClass(ejas,target) 

obs.texposure = 0.0833 #cadence [hour]
obs.tframe = 7.1  #time for one frame [sec]
obs.napix = 15 # number of the pixels in aperture 
obs.mu = 1 
S=1.8*1.8*np.pi #core size
obs.effnpix = S/3.0 #3 is an approx. increment factor of PSF
obs.mu = 1 

shot=[]
dark=[]
read=[]
H=[]
darr=np.linspace(10,30,101)
magdict=convmag.get_magdict()

for distpc in darr:
    target.dpc=distpc #change targets
    obs.target = target
    obs.update()
    H.append(convmag.get_mag("H",obs.flux,magdict))
    #print(distpc,convmag.get_mag("H",obs.flux,magdict))
    #print("saturation?",obs.sat)
    dark.append(obs.sigd_relative)
    read.append(obs.sigr_relative)
    shot.append(obs.sign_relative)
    
sigsarr_relative=np.array(shot)
sigdarr_relative=np.array(dark)
sigrarr_relative=np.array(read)
magarr=np.array(H)

fig=plt.figure(figsize=(7,5))

ax=fig.add_subplot(211)
ax.plot(magarr,sigsarr_relative,label="shot noise")
ax.plot(magarr,sigdarr_relative,label="dark noise",ls="dotted")
ax.plot(magarr,sigrarr_relative,label="read noise",ls="dashed")
pylab.legend()
pylab.xlim(9.,10.9)
pylab.ylim(0,600)
ax.fill([9,9.5,9.5,9.0,9.0],[0,0,600,600,0],alpha=0.3,color="gray")
for i,dpc in enumerate(darr):
    if np.mod(dpc,5)==0:
        plt.axvline(magarr[i],ls="dashed",color="gray",alpha=0.3)
plt.ylabel("noise for 5 min (ppm)")
ppm=1.e6
ax=fig.add_subplot(212)
ax.plot(magarr,np.sqrt(sigsarr_relative**2 + sigdarr_relative**2 + sigrarr_relative**2)/ppm*7*100)
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
plt.show()
