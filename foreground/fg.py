import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy import constants as const
from astropy import units as u
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

fac=(const.h*const.c/u.m).value
dat=pd.read_csv("../data/gemini/mk_skybg_nq_10_10_ph.dat",names=("lam","ph"),delimiter=";")
wav=dat["lam"]*1.e-3
#dat["ph"] ph/sec/arcsec2/nm/m2
emis=(fac/(dat["lam"]*1.e-9)*dat["ph"]*1.e3)

dat2=pd.read_csv("../data/gemini/mk_skybg_zm_10_10_ph.dat",names=("lam","ph"),delimiter=";")
print(dat2["lam"])
wav2=dat2["lam"]*1.e-3
#dat["ph"] ph/sec/arcsec2/nm/m2
emis2=(fac/(dat2["lam"]*1.e-9)*dat2["ph"]*1.e3)


fig=plt.figure()
ax=fig.add_subplot(111)
plt.plot(wav,emis,color="C0")
plt.plot(wav2,emis2,color="C0")
plt.yscale("log")
plt.xscale("log")
plt.xlabel("wavelength [micron]",fontsize=16)
plt.ylabel("Foreground [J/s/arcsec2/m2/um]",fontsize=16)
plt.title("Maunakea airmass=1 wvp = 1mm",fontsize=16)
plt.tick_params(labelsize=16)
ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
plt.show()
