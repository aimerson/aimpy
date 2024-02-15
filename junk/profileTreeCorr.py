#! /usr/bin/env python

import numpy as np
import treecorr
from aimpy.utils.timing import STOPWATCH

def getRandoms(N,Lbox):
    X = np.random.rand(N)*Lbox
    Y = np.random.rand(N)*Lbox
    Z = np.random.rand(N)*Lbox
    return X,Y,Z


WATCH = STOPWATCH()

config = {}
config["nbins"] = 20
config["min_sep"] = 15.0
config["max_sep"] = 150.0


RR = treecorr.NNCorrelation(config=config,verbose=1)
DD = treecorr.NNCorrelation(config=config,verbose=1)
DR = treecorr.NNCorrelation(config=config,verbose=1)
RD = treecorr.NNCorrelation(config=config,verbose=1)

print("Building datasets...")
N = 40000
Lbox = 1500.0
X,Y,Z = getRandoms(N,Lbox)
DATA = treecorr.Catalog(x=X,y=Y,z=Z)
X,Y,Z = getRandoms(N*2,Lbox)
RAND = treecorr.Catalog(x=X,y=Y,z=Z)

PPN = 16

print("Processing RR...")
RR.process_cross(RAND,RAND,num_threads=PPN)
print("Processing DR...")
DR.process_cross(DATA,RAND,num_threads=PPN)
print("Processing RD...")
RD.process_cross(RAND,DATA,num_threads=PPN)
print("Processing DD...")
DD.process_cross(DATA,DATA,num_threads=PPN)
print("Computing xi...")
xi,xiErr = DD.calculateXi(RR,dr=DR,rd=RD)

DD.write("profileTreeCorr.dat")


WATCH.stop()
