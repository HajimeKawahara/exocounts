import pandas as pd
import matplotlib.pyplot as plt
from exocounts import exocounts
from exocounts import planet
from exocounts import convmag
from astropy import constants as const
from astropy import units as u
import numpy as np
import sys

ts = exocounts.InstClass()
ts.lamb = 2.3 * u.micron  # micron
ts.dlam = 0.001 * u.micron  # 1 nm
ts.dtel = 8.2 * u.m  # telescope diameter m
ts.dstel = 0.00 * u.m  # secondary telescope diameter m

# uses TSHITS setting
ts.throughput = 0.1
ts.ndark = 0.0 / u.s  # dark current [e-/pix/s]
ts.nread = 0.0  # nr [e-/pix/read]
ts.fullwell = 1.0e7


dat = pd.read_csv(
    "../../data/gemini/mk_skybg_zm_10_10_ph.dat", delimiter=";", names=("wav", "ct")
)
wav = dat["wav"] #nm
ct = dat["ct"]  # ph/sec/arcsec^2/nm/m^2

ld = ((ts.lamb.to(u.m) / ts.dtel).value * u.radian).to(u.arcsec)
ldarr = (((1.0 * u.nm).to(u.m) / ts.dtel).value * u.radian).to(u.arcsec) * wav # lambda/D

fov = ldarr * ldarr * np.pi
A = ((ts.dtel.value) / 2) ** 2 * np.pi
ctarr = ct * fov * A  # ph/sec/nm

###
target = exocounts.TargetClass()
target.teff = 4980.0 * u.K  # K
target.rstar = 0.79 * const.R_sun  # Rsolar
target.d = 19.3 * u.pc  # pc

obs = exocounts.ObsClass(ts, target)

obs.texposure = 1 * u.s  # = [sev]
obs.tframe = 1.0 * u.s  # time for one frame [sec]
obs.napix = 1  # number of the pixels in aperture
obs.mu = 1
obs.effnpix = 1.0
obs.target = target
obs.update()
magdict = convmag.get_magdict()
print("magnitude=", convmag.get_mag("V", obs.flux, magdict))
print(obs.nphoton_brightest)
print("photon/pix/frame=", obs.nphoton_frame)

###
from gollum.phoenix import PHOENIXSpectrum

T = 5000
spec = PHOENIXSpectrum(teff=T, logg=5, wl_lo=9000.0, wl_hi=56000.0)

spectrum = spec.instrumental_broaden(resolving_power=1_000)
flux = spectrum.flux  # absolute flux u.erg/u.cm/u.cm/u.cm/u.s, i.e. pi B
lamb = (spectrum.spectral_axis.to(u.m)).value * 1.0e9  # nm


print(lamb)
i = np.searchsorted(lamb, (ts.lamb.to(u.m)).value * 1.0e9)
print(lamb[i])
photonflux = flux * lamb / (flux[i] * lamb[i]) * obs.nphoton_frame
# plt.plot(lamb,photonflux)
# plt.show()
###


fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(wav, ctarr*ts.throughput)
plt.plot(lamb, photonflux, label="HD189933b, V=10")

# K
Kc = 2190
dK = 390
x1 = Kc - dK / 2
x2 = Kc + dK / 2
x = wav
y = 1.0e7 * np.ones_like(wav)
plt.fill_between(x, y, where=(x > x1) & (x < x2), color="gray", alpha=0.5)

# L
Lc = 3450
dL = 472
x1 = Lc - dL / 2
x2 = Lc + dL / 2
x = wav
y = 1.0e7 * np.ones_like(wav)
plt.fill_between(x, y, where=(x > x1) & (x < x2), color="gray", alpha=0.5)

# M
Mc = 4750
dM = 460
x1 = Mc - dM / 2
x2 = Mc + dM / 2
x = wav
y = 1.0e7 * np.ones_like(wav)
plt.fill_between(x, y, where=(x > x1) & (x < x2), color="gray", alpha=0.5)

ylab = 1.0e-2
plt.text(Kc, ylab, "K")
plt.text(Lc, ylab, "L")
plt.text(Mc, ylab, "M")

plt.yscale("log")
plt.ylabel("ph/sec/nm")
plt.xlabel("nm")
plt.title("optimal aperture (defraction limit)")
plt.legend()
plt.show()
