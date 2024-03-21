import pandas as pd
import matplotlib.pyplot as plt
from exocounts import exocounts
from exocounts import planet
from exocounts import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np
import sys

ts=exocounts.InstClass()
ts.lamb = 2.3*u.micron #micron
ts.dlam = 0.001*u.micron #1 nm
ts.dtel = 8.2*u.m #telescope diameter m
ts.dstel = 0.00*u.m #secondary telescope diameter m

# uses TSHITS setting
ts.throughput = 0.1
ts.ndark = 0.0/u.s #dark current [e-/pix/s]
ts.nread = 0.0 #nr [e-/pix/read]
ts.fullwell = 1.e7



dat = pd.read_csv("../../data/gemini/mk_skybg_zm_10_10_ph.dat",delimiter=";",names=("wav","ct"))
wav = dat["wav"]
ct = dat["ct"] # ph/sec/arcsec^2/nm/m^2

ld=((ts.lamb.to(u.m)/ts.dtel).value*u.radian).to(u.arcsec) 
ldarr = (((1.0*u.nm).to(u.m)/ts.dtel).value*u.radian).to(u.arcsec)*wav 

fov = ldarr*ldarr*np.pi
A = ((ts.dtel.value)/2)**2*np.pi
ctarr = ct*fov*A #ph/sec/nm

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(wav,ctarr)

#K
Kc = 2190
dK = 390
x1 = Kc - dK/2
x2 = Kc + dK/2
x = wav
y = 1.e7*np.ones_like(wav)
plt.fill_between(x, y, where=(x > x1) & (x < x2), color='gray', alpha=0.5) 

#L
Kc = 3450
dK = 472
x1 = Kc - dK/2
x2 = Kc + dK/2
x = wav
y = 1.e7*np.ones_like(wav)
plt.fill_between(x, y, where=(x > x1) & (x < x2), color='gray', alpha=0.5) 

#M
Kc = 4750
dK = 460
x1 = Kc - dK/2
x2 = Kc + dK/2
x = wav
y = 1.e7*np.ones_like(wav)
plt.fill_between(x, y, where=(x > x1) & (x < x2), color='gray', alpha=0.5) 


plt.yscale("log")
plt.ylabel("ph/sec/nm")
plt.xlabel("nm")
plt.show()
