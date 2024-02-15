#! /usr/bin/env python

import numpy as np
from aimpy.plotting.utils import *
from matplotlib.ticker import MultipleLocator


class HaloOccupationDistribution(object):

    def __init__(self,Mmin=None,sigmaM=None,Mcut=None,M1=None,alpha=None):
        self.Mmin = Mmin
        self.sigmaM = sigmaM
        self.Mcut = Mcut
        self.M1 = M1
        self.alpha = alpha
        return

    def centrals(self,M,Mmin=None,sigmaM=None):
        from scipy.special import erf
        if Mmin is None:
            Mmin = self.Mmin
        if Mmin is None:
            raise ValueError("No value provided for Mmin.")
        if sigmaM is None:
            sigmaM = self.sigmaM
        if sigmaM is None:
            raise ValueError("No value provided for sigmaM.")
        hod = 1.0 + erf((np.log10(M)-np.log10(Mmin))/sigmaM)
        hod *= 0.5
        return hod
    
    def satellites(self,M,Mcut=None,M1=None,alpha=None):        
        if Mcut is None:
            Mcut = self.Mcut
        if Mcut is None:
            raise ValueError("No value provided for Mcut.")
        if M1 is None:
            M1 = self.M1
        if M1 is None:
            raise ValueError("No value provided for M1.")
        if alpha is None:
            alpha = self.alpha
        if alpha is None:
            raise ValueError("No value provided for alpha.")
        hod = ((M-Mcut)/M1)**alpha
        np.place(hod,np.isnan(hod),1.0e-50)
        return hod
        
    def total(self,M,Mmin=None,sigmaM=None,Mcut=None,M1=None,alpha=None):        
        return self.centrals(M,Mmin=Mmin,sigmaM=sigmaM) + \
            self.satellites(M,Mcut=Mcut,M1=M1,alpha=alpha)
    
    
alpha = 1.08
Mcut = 10.0**11.85
Mmin = 10.0**11.72
M1 = 10.0**12.78
sigmaM = 0.276
HOD = HaloOccupationDistribution(Mmin=Mmin,Mcut=Mcut,M1=M1,sigmaM=sigmaM,alpha=alpha)

mass = np.linspace(10.0,15.0,1000)
fig = figure(figsize=(6,5))
ax = fig.add_subplot(111,yscale='log')

ax.plot(mass,HOD.centrals(10.0**mass),c='b',lw=2.5,ls=":",label="Centrals")
ax.plot(mass,HOD.satellites(10.0**mass),c='r',lw=2.0,ls="--",label="Satellites")
ax.plot(mass,HOD.total(10.0**mass),c='k',lw=2.0,label="All galaxies")

ax.set_ylim(bottom=1.0e-4)
ax.set_xlabel("$\log_{10}\left (^{}{\\rm halo\,\,mass_{}}\\right )\,\,\,\left [h^{-1}{\\rm M_{\odot}}\\right ]$",fontsize=14)
ax.set_ylabel("Mean number of galaxies per halo")

majorLocator = MultipleLocator(1.0)
ax.set_xlim(10.6,15.0)
ax.xaxis.set_major_locator(majorLocator)

minor_ticks(ax.xaxis)
Legend(ax,loc=2)


savefig("haloOccupationDistribution.pdf",bbox_inches='tight')

