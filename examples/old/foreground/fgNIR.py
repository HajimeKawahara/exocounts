import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy import constants as const
from astropy import units as u
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import diflimit

emis=1.e-15*u.J/u.s/u.arcsec/u.arcsec/u.micron
aparture = ((diflimit.ld(1.5*u.micron,30.*u.m)))**2*np.pi
print("TMT aperture a=",aparture)
print("e*a=",aparture*emis)

apartureV = ((diflimit.ld(1.5*u.micron,10.*u.m)))**2*np.pi
print("VLT aperture a=",apartureV)
print("e*a2=",apartureV*emis)
