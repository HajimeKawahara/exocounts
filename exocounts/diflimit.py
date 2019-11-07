from astropy import constants as const
from astropy import units as u
import numpy as np
def ld(lamb,d):
    return (lamb/d).to(1)/np.pi*180.0*3600*u.arcsec

print((1.0*u.h.to(u.s)))
