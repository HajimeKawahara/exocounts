"""test for nstar.

"""

import pytest
from exocounts.nstar import Blambda
from astropy import units as u
import numpy as np

def test_Blamba():
    b=Blambda(3000.0*u.K, 1.0*u.micron)
    refs=99240.33330070703
    val=b.to(u.erg/u.cm/u.cm/u.angstrom/u.s).value
    assert val-refs == 0.0


if __name__ == "__main__":
    test_Blamba()

    
