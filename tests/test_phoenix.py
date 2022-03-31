




if __name__=="__main__":
    print()
    from gollum.phoenix import PHOENIXSpectrum
    spec = PHOENIXSpectrum(teff=3000, logg=5, wl_lo=5000.0,wl_hi=25000.)
    normalized_spectrum = spec.instrumental_broaden(resolving_power=1_000).normalize()
    flux=normalized_spectrum.flux
    lamb=normalized_spectrum.spectral_axis*1.e-4
    photonflux=flux*lamb
