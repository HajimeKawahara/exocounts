import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy import constants as const
from astropy import units as u
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import diflimit

def Blambdaum(T,lambum):
    lamb5=(lambum)**5    
    fac=const.h*const.c/((1.0*u.um).to(u.m)*const.k_B*T)
    fac=fac/lambum
    bl=2.0*(const.c**2)*const.h/lamb5/((1.0*u.um)**5)/(np.exp(fac)-1)
    return bl.to(u.J/u.m/u.m/u.um/u.s)


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

mask=(wav>10.0)*(wav<12.5)
print("Near filter mean e=",np.mean(emis[mask]))
aparture = ((diflimit.ld(11.0*u.micron,30.*u.m)))**2*np.pi
print("TMT aperture a=",aparture)
print("e*a=",aparture*np.mean(emis[mask]))

apartureV = ((diflimit.ld(11.0*u.micron,10.*u.m)))**2*np.pi
print("VLT aperture a=",apartureV)
print("e*a2=",apartureV*np.mean(emis[mask]))

TAO=True

if TAO:
    tao=pd.read_csv("../data/tao/TAO_MIR_Emission.dat",delimiter=" ",comment="#",names=("WL","Tatm","Fatm","tel1","tel2","tel3"))
    hnu=(const.h*const.c/(1.0*u.micron)).to("J").value
    print(hnu)
    sr2arcsec2=(1.0*u.sr/u.arcsec/u.arcsec).to(1)
    ftao=tao["Fatm"]/tao["WL"]/sr2arcsec2*(hnu/tao["WL"])
    ftel=tao["tel3"]/tao["WL"]/sr2arcsec2*(hnu/tao["WL"])
    ftel2=tao["tel1"]/tao["WL"]/sr2arcsec2*(hnu/tao["WL"])
    ftelg=Blambdaum(280*u.K,tao["WL"])*0.07/sr2arcsec2
#    ftelg=Blambdaum(273*u.K,tao["WL"])/sr2arcsec2

fig=plt.figure(figsize=(10,6))
ax=fig.add_subplot(111)
plt.plot(wav,emis,color="C0",label="Maunakea airmass=1 wvp = 1mm")
plt.plot(wav2,emis2,color="C0")
plt.yscale("log")
plt.xscale("log")
plt.xlim(5,20)
plt.ylim(1.e-13,1.e-9)
plt.xlabel("wavelength [micron]",fontsize=16)
plt.ylabel("Foreground [J/s/arcsec2/m2/um]",fontsize=16)
#plt.title("Maunakea airmass=1 wvp = 1mm",fontsize=16)
if TAO:
    plt.plot(tao["WL"],ftao,color="C1",label="TAO 0.34mm")
    plt.plot(tao["WL"],ftel,color="C2",label="TAO 260K 9% ")
    plt.plot(tao["WL"],ftel2,color="C3",label="TAO 260K 3% ")
    plt.plot(tao["WL"],ftelg,color="C4",label="VLT 280K 7% ",ls="dashed")
    
plt.legend()
plt.tick_params(labelsize=16)
ax.xaxis.set_major_formatter(FormatStrFormatter("%.1f"))
plt.savefig("fg.png")
plt.show()
