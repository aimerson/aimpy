#! /usr/bin/env python

import numpy as np
from scipy.interpolate import interp1d

class Calzetti(object):

    @classmethod
    def angstromsToMicrons(cls,wavelength):
        angstrom = 1.0e-10
        micron = 1.0e-6
        return wavelength*(micron/angstrom)
    
    @classmethod
    def buildInterpolator(cls,Rv=4.05):        
        waveLow = np.linspace(0.12,0.63,10000)
        waveUpp = np.linspace(0.63,2.20,10000)
        lower = 2.659*( -2.156+(1.509/waveLow)-(0.198/waveLow**2)+\
                             (0.011/waveLow**3) )
        upper = 2.659*( -1.857 + (1.040/waveUpp) )
        curve = np.append(lower,upper)
        curve += Rv
        wavelength = np.append(waveLow,waveUpp)
        INTERP = interp1d(wavelength,curve,kind='linear',
                          fill_value="extrapolate")
        return INTERP
    
    @classmethod
    def getCurve(cls,wavelength,Rv=4.05):                
        INTERP = cls.buildInterpolator(Rv=Rv)
        klambda = INTERP(cls.angstromsToMicrons(wavelength))
        return klambda
    
    @classmethod
    def getAttenuation(cls,wavelength,Av,Rv=4.05):
        klambda = cls.getCurve(wavelength,Rv=Rv)
        return klambda*Av/Rv
    

    
