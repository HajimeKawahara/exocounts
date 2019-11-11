import hz 
import pandas as pd
import numpy as np
from astroquery.simbad import Simbad
from time import sleep

Simbad.SIMBAD_URL = "http://simbad.u-strasbg.fr/simbad/sim-script"
#Simbad.add_votable_fields("parallax","flux(V)","flux(R)","flux(J)","flux(H)","flux(K)","pmra","pmdec")

#def read_rawnearbystar():
dat=pd.read_csv("nearby.txt",delimiter=";")
pc2ly=3.261563777

for i in range(0,len(dat["Name"]))[34:]:
    try:
    #if True:
        f=open("nearby_updateA.txt","a")        
        name=str(dat["Name"][i])
        pname=str(dat["ProperName"][i])
        sptype=str(dat["Type"][i])
        ### compute HZ ###
        try:
            rstar=float(dat["R(SU)"][i])
            teff=float(dat["Teff(K)"][i])
            Lstar=rstar**2*(teff/5772.0)**4
            amin,amax=hz.gethz(teff,Lstar)
        except:
            amin,amax=None,None
        d=str(dat["D(ly)"][i]/pc2ly)
        m=str(dat["M(SU)"][i])
        r=str(dat["R(SU)"][i])
        t=str(dat["Teff(K)"][i])
        if dat["Planets"][i]=="":
            p=str("0")
        else:
            p=str(dat["Planets"][i])
        sleep(1)
        print(name)
        result_table = Simbad.query_object(name)    
        rasimbad=result_table["RA"][0]
        decsimbad=result_table["DEC"][0]
        com=(str(i)+"|"+name+"|"+str(rasimbad)+"|"+str(decsimbad)+"|"+\
             pname+"|"+sptype+"|"+\
             d+"|"+m+"|"+r+"|"+t+"|"+p+"|"+\
             str(amin)+"|"+str(amax)+"\n")
        f.write(com)
        f.close()
    except:
        rstar=float(dat["R(SU)"][i])
        teff=float(dat["Teff(K)"][i])
        print("Error: "+str(dat["Name"][i]),rstar,teff)
