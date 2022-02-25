# exocounts

Exocounts computes various statistical noises of astronomical photon counts observations. Very easy task? Yes, I know, but people sometimes make mistakes in photon number calculations, which can have serious consequences.

Exocounts defines InstClass, TargetClass, ObsClass, something like that.

```python
ejas=exocounts.InstClass()
ejas.lamb = 1.35*u.micron #micron
ejas.dlam = 0.5*u.micron #micron
ejas.dtel = 0.35*u.m #telescope diameter m
ejas.dstel = 0.14*u.m #secondary telescope diameter m or 12.4 (3 tels)
ejas.throughput = 0.8
ejas.ndark = 15.5/u.s #dark current
ejas.nread = 15.0 #nr
ejas.fullwell = 150000.

target=exocounts.TargetClass()
target.teff = 3000.0*u.K #K
target.rstar = 0.2*const.R_sun #Rsolar
target.d = 15.0*u.pc #pc

obs=exocounts.ObsClass(ejas,target) 
obs.texposure = 0.0833*u.h #cadence [hour]
obs.tframe = 12.5*u.s  #time for one frame [sec]
obs.napix = 15 # number of the pixels in aperture 
S=1.8*1.8*np.pi #core size
obs.effnpix = S/3.0 #3 is an approx. increment factor of PSF
```

and then you can compute noises like that.
```python
print("photon/pix/frame=",obs.nphoton_frame)
print("shot noise (sigma) in total [ppm]=",obs.sign_relative*1.e-6)
print("dark in total  [ppm]=",obs.sigd_relative*1.e-6)
print("readout in total  [ppm]=",obs.sigr_relative*1.e-6)
```

