"""Stellar photon count module."""
import numpy as np
from astropy import constants as const
from astropy import units as u


def Blambda(T, lamb):
    """Planck distrintuion.

    Args:
       T: temperature with the astropy.unit of Kelvin, e.g. 1000.0*u.K
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       planck function B_lambda with the astropy unit

    """
    lamb5 = (lamb.to(u.m))**5
    fac = const.h*const.c/(lamb.to(u.m)*const.k_B*T)
    bl = 2.0*(const.c**2)*const.h/lamb5/(np.exp(fac)-1)
    return bl


def photon_Blambda(T, lamb):
    """Photon count Planck distrintuion.

    Args:
       T: temperature with the astropy.unit of Kelvin, e.g. 1000.0*u.K
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       B_lambda/(h nu) with the astropy unit

    """
    pB = Blambda(T, lamb)/(const.h*const.c/(lamb.to(u.m)))

    return pB


def getbbflux(Target, lamb):
    """compute blackbody flux of Target at wavelength of lambda

    Args:
       Target: TargetClass instance 
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       flux

    """
    

    tstar = Target.teff
    d = Target.d
    r = Target.rstar
    flux = np.pi*Blambda(tstar, lamb)*r*r/(d*d)
#    return flux.to(u.erg/u.cm/u.cm/u.micron/u.s)
    return flux.to(u.J/u.m/u.m/u.micron/u.s)


def getbbfluxph(Target, lamb):
    """compute blackbody photon flux of Target at wavelength of lambda

    Args:
       Target: TargetClass instance 
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       photon flux

    """

    tstar = Target.teff
    d = Target.d
    r = Target.rstar
    flux = np.pi*photon_Blambda(tstar, lamb)*r*r/(d*d)
    return flux.to(1/u.m/u.m/u.micron/u.s)


def getbbfluxJy(Target, lamb):
    """compute blackbody flux of Target at wavelength of lambda in the unit of Jansky

    Args:
       Target: TargetClass instance 
       lamb: wavelength with the astropy.unit of length, e.g. 1.0*u.m

    Returns:
       flux in Jansky

    """

    tstar = Target.teff
    d = Target.d
    r = Target.rstar
    flux = np.pi*Blambda(tstar, lamb)*r*r/(d*d)*lamb*lamb/const.c
    flux = flux.to(u.Jy)
    return flux


def Nstar(Inst, Target, Obs, info=True, integrate=True, Nintegrate=128):
    tstar = Target.teff
    lamin = Inst.lamb
    d = Target.d
    r = Target.rstar
    texp = Obs.texposure
    a = np.pi*(Inst.dtel/2.0)**2 - np.pi*(Inst.dstel/2.0)**2
    dl = Inst.dlam
    contrast = Target.contrast
    if integrate:
        ddl = dl/Nintegrate
        lamarr = lamin+np.linspace(-dl/2, dl/2, Nintegrate)
        fluxarr = []
        photonfarr = []
        photonarr = []
        for j, lamlow in enumerate(lamarr[:-1]):
            lamc = (lamarr[j+1]+lamlow)/2.0
            dll = lamarr[j+1]-lamlow
            flux = np.pi*Blambda(tstar, lamc)*r*r/(d*d)*contrast
            photonf = np.pi*photon_Blambda(tstar, lamc)*r*r/(d*d)*contrast
            photon = photonf*a*dll*texp*Inst.throughput
            fluxarr.append(flux)
            photonfarr.append(photonf)
            photonarr.append(photon)

        photon = np.sum(photonarr)
    else:
        flux = np.pi*Blambda(tstar, lamin)*r*r/(d*d)*contrast
        photonf = np.pi*photon_Blambda(tstar, lamin)*r*r/(d*d)*contrast
        photon = photonf*a*dl*texp*Inst.throughput
        photon = photon.to(1)

    flux = np.pi*Blambda(tstar, lamin)*r*r/(d*d)*contrast
    photonf = np.pi*photon_Blambda(tstar, lamin)*r*r/(d*d)*contrast

    if info:
        print('B(lambda) for', tstar, 'at ', lamin)
        print('{:e}'.format(Blambda(tstar, lamin).to(
            u.erg/u.cm/u.cm/u.angstrom/u.s)))
        print('{:e}'.format(Blambda(tstar, lamin).to(
            u.erg/u.cm/u.cm/u.micron/u.s)))
        print('{:e}'.format(Blambda(tstar, lamin).to(u.J/u.m/u.m/u.m/u.s)))
        print('---------------------')
        print('FLUX from a sphere with r=', Target.rstar,
              '[Rsol] and', 'dpc=', d, '[pc]')
        print(flux.to(u.erg/u.cm/u.cm/u.micron/u.s))
        print('Photon FLUX from a sphere with  r=',
              Target.rstar, '[Rsol] and', 'dpc=', d, '[pc]')
        print(photonf.to(1/u.cm/u.cm/u.micron/u.s))
        print('---------------------')
        print('Photon Count with observation:')
        print('  telescope diameter', Inst.dtel, '[m]')
        print('  band width', Inst.dlam, '[micron]')
        print('  exposure', Obs.texposure,
              '[hour] = ', Obs.texposure.to(u.min), ' [min]')
        print('  throughput', Inst.throughput)
        print('N=', '{:e}'.format(photon))
        print('photon noise 1/sqrt(N)=', np.sqrt(1.0/photon)*1e6, '[ppm]')
        print('photon noise 1/sqrt(N)=', np.sqrt(1.0/photon)*1e2, '[%]')
        print('7 sigma depth=', np.sqrt(1.0/photon)*1e2*7.0, '[%]')

    Nphoton = photon
    Obs.nphoton_exposure = Nphoton
    Obs.nphoton_frame = Nphoton*(Obs.tframe/Obs.texposure).to(1)
    Obs.sign = np.sqrt(Nphoton)
    Obs.flux = flux
    Obs.photonf = photonf
    ppm = 1.e6
    Obs.sign_relative = Obs.sign/Obs.nphoton_exposure*ppm
