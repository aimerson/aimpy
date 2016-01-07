#! /usr/bin/env python

import numpy as np
import scipy as sp
from scipy.constants import c,constants
from scipy.integrate import romberg

class cosmology:
    """
    cosmology
    
    This class contains various functions to compute distances and
    times in a Universe with a given cosmology.
    
    List of functions:

    parameters() : report back parameters for specified cosmology
    comoving_distance() : calculates the comoving distance at
                          redshift, z
    redshift_at_distance() : calculates the redshift at comoving
                             disance, r
    age_of_universe() : calculates the age of the Universe at
                        redshift, z
    lookback_time() : calculates lookback time to given redshift,
                      z
    angular_diamater_distance() : calculates the angular diameter
                                  distance a redshift, z
    angular_scale() : calculates the angular scale at redshift, z
    luminosity_distance() : calculates the luminosity distance at
                            redshift, z
    comving_volume() : calculates the comoving volume contained
                       within a sphere extending out to redshift,
                       z
    dVdz() :  calculates dV/dz at redshift, z
    H() : return Hubble constant as measured at redshift, z
    E() : returns Peebles' E(z) function at redshift, z, for
          specified cosmology

    NOTE: this module requires the numpy and scipy libraries.

    Based upon the 'Cosmology Calculator' (Wright, 2006, PASP,
    118, 1711) and Fortran 90 code written by John Helly.
    
    """
    
    def __init__(self,omega0=0.25,lambda0=0.75,omegab=0.045,h0=0.73,\
                 sigma8=0.9,ns=1.0,radiation=False):

        #
        # Store cosmological parameters
        #
        self._WM = omega0
        self._WV = lambda0
        self._WB = omegab
        self._h = h0
        self._sigma8 = sigma8
        self._ns = ns
        if radiation:            
            self._WR = (4.165e-5)/(self._h**2)
        else:
            self._WR = 0.0            
        self._WK = 1.0 - (self._WM + self._WV + self._WR)

        # Define useful constants/conversions
        self._nzmax = 10000
        self._zmax = 20.0
        self._r_comoving = np.zeros(self._nzmax)
        self._dz = self._zmax/float(self._nzmax)
        self._redshift = np.arange(0.0,self._zmax,self._dz)
        self._inv_dz = 1.0/self._dz
        self._Mpc = constants.mega*constants.parsec
        self._H100 = 100.0*constants.kilo/self._Mpc
        self._Gyr = constants.giga*constants.year
        self._invH0 = (self._Mpc/(100.0*constants.kilo))/self._Gyr
        self._kmpersec_to_mpchpergyr = constants.kilo*(self._Gyr/self._Mpc)*self._h
        self._DH = c/self._H100 # Hubble Distance

        # Set up array of redshift vs. comoving distance for
        # interpolation for other properties
        def finit(z):
            a = 1.0/(1.0+z)
            result = self._WK*(a**-2) + self._WV + \
                     self._WM*(a**-3) + self._WR*(a**-4)
            result = (c/self._H100)/np.sqrt(result)/self._Mpc
            return result
        for i in range(1,len(self._redshift)):
            z1 = self._redshift[i-1]
            z2 = self._redshift[i]
            self._r_comoving[i] = self._r_comoving[i-1] + \
                                  romberg(finit,z1,z2)


    def E(self,z=0.0):
        """
        E(z): Peebles' E(z) function.
        
        """
        a = 1.0/(1.0+z)
        result = self._WK*(a**-2) + self._WV + \
                 self._WM*(a**-3) + self._WR*(a**-4)
        return np.sqrt(result)
    

    def H(self,z=0.0):
        """
        H(z): Function to return the Hubble parameter as measured
              by an observer at redshift, z.
        """
        result = 100.0*self.E(z)
        return result
    

    def f(self,z=0.0):
        """
        f(z): Function relating comoving distance to redshift.
              Integrating f(z)dz from 0 to z' gives comoving
              distance r(z'). Result is in Mpc/h.
        
        Note: uses global cosmology variables.          
        """
        a = 1.0/(1.0+z)
        result = self._WK*(a**-2) + self._WV + \
                 self._WM*(a**-3) + self._WR*(a**-4)
        result = (c/self._H100)/np.sqrt(result)/self._Mpc
        return result
    

    def parameters(self):
        """
        parameters(): reports parameters for cosmology

        USAGE: parameters()            
        """
        print "***********************"
        print "COSMOLOGY:"
        print "   Omega_M = {0:5.3f}".format(self._WM)
        print "   Omega_b = {0:5.3f}".format(self._WB)
        print "   Omega_V = {0:5.3f}".format(self._WV)
        print "   h       = {0:5.3f}".format(self._h)
        print "   Omega_R = {0:5.3e}".format(self._WR)
        print "   Omega_k = {0:5.3f}".format(self._WK)
        print "   sigma_8 = {0:5.3f}".format(self._sigma8)
        print "   n_s     = {0:5.3f}".format(self._ns)
        print "***********************"
        return
    
    def comoving_distance(self,z=0.0):
        """
        comoving_distance(): Returns the comoving distance (in Mpc/h)
                             corresponding to redshift, z.
        
        USAGE: comoving_distance(z)
        
        """
        return np.interp(z,self._redshift,self._r_comoving)
    
    def redshift_at_distance(self,r=0.0):
        """
        redshift_at_distance(): Returns the redshift corresponding
                                to comoving distance, r (in Mpc/h).
            
        USAGE: redshift_at_distance(z)
        
        """
        return np.interp(r,self._r_comoving,self._redshift)
    
    
    def age_of_universe(self,z=0.0):
        """
        age_of_universe(): Returns the age of the Universe (in Gyr) at
                           a redshift, z, for the given cosmology.
        
        USAGE: age_of_universe(z)
        
        """
        a = 1.0/(1.0+z)
        if(self._WM >= 0.99999): # Einstein de Sitter Universe
            result = self._invH0*2.0*np.sqrt(a)/(3.0*self._h)
        else:
            if(self._WV <= 0.0): # Open Universe
                zplus1 = 1.0/a
                result1 = self._WM/(2.0*self._h*(1-self._WM)**1.5)
                result2 = 2.0*np.sqrt(1.0-self._WM)*np.sqrt(self._WM*(zplus1-1.0)+1.0)
                result3 = np.arccosh((self._WM*(zplus1-1.0)-self._WM+2.0)/(self._WM*zplus1))
                result = self._invH0*result1*(result2/result3)
            else: # Flat Universe with non-zero Cosmological Constant
                result1 = (2.0/(3.0*self._h*np.sqrt(1.0-self._WM)))
                result2 = np.arcsinh(np.sqrt((1.0/self._WM-1.0)*a)*a)
                result = self._invH0*result1*result2
        return result
            
            
    def lookback_time(self,z=0.0):
        """
        lookback_time(): Returns the lookback time (in Gyr) to 
                         redshift, z.
        
        USAGE: lookback_time(z)
        
        """
        t = self.age_of_universe(0.0) - self.age_of_universe(z)
        return t


    def angular_diameter_distance(self,z=0.0):
        """
        angular_diameter_distance(): Returns the angular diameter
                                     distance (in Mpc/h) corresponding
                                     to redshift, z.
        
        USAGE: angular_diameter_distance(z)    

        """
        dr = self.comoving_distance(z)*self._Mpc/(c/self._H100)
        x = np.sqrt(np.abs(self._WK))*dr
        if np.ndim(x) > 0:
            ratio = np.ones_like(x)*-1.00
            mask = (x > 0.1)
            y = x[np.where(mask)]
            if(self._WK > 0.0):
                np.place(ratio,mask,0.5*(np.exp(y)-np.exp(-y))/y)
            else:
                np.place(ratio,mask,np.sin(y)/y)
            mask = (x <= 0.1)
            y = x[np.where(mask)]**2
            if(self._WK < 0.0): 
                y = -y
            np.place(ratio,mask,1.0 + y/6.0 + (y**2)/120.0)
        else:        
            ratio = -1.0
            if(x > 0.1):
                if(self._WK > 0.0):
                    ratio = 0.5*(np.exp(x)-np.exp(-x))/x
                else:
                    ratio = np.sin(x)/x
            else:
                y = x**2
                if(self._WK < 0.0): 
                    y = -y
                ratio = 1.0 + y/6.0 + (y**2)/120.0
        dt = ratio*dr/(1.0+z)
        dA = (c/self._H100)*dt/self._Mpc
        return dA


    def angular_scale(self,z=0.0):
        """
        angular_scale(): Returns the angular scale (in kpc/arcsec)
                         corresponding to redshift, z.
        
        USAGE: angular_scale(z)
        
        """
        da = self.angular_diameter_distance(z)
        a = da/206.26480
        return a
    

    def luminosity_distance(self,z=0.0):
        """
        luminosity_distance(): Returns the luminosity distance
                               (in Mpc/h) corresponding to a
                               redshift, z.
        
        USAGE: luminosity_distance(z)
        
        """
        da = self.angular_diameter_distance(z)*self._Mpc/(c/self._H100)
        dL = (c/self._H100)*da*((1.0+z)**2)/self._Mpc
        return dL
    

    def comoving_volume(self,z=0.0):
        """
        comoving_volume(): Returns the comoving volume (in Mpc^3)
                           contained within a sphere extending out
                           to redshift, z.
        
        USAGE: comoving_volume(z)
        
        """
        dr = self.comoving_distance(z)*self._Mpc/(c/self._H100)
        x = np.sqrt(np.abs(self._WK))*dr
        if np.ndim(z) > 0:
            ratio = np.ones_like(z)*-1.0
            mask = (x > 0.1)
            y = x[np.where(mask)]
            if(self._WK > 0.0):
                rat = (0.125*(np.exp(2.0*y)-np.exp(-2.0*y))-y/2.0)
            else:
                rat = (y/2.0 - np.sin(2.0*y)/4.0)
            np.place(ratio,mask,rat/((y**3)/3.0))
            mask = (x <= 0.1)
            y = x[np.where(mask)]**2
            if(self._WK < 0.0): 
                y = -y
            np.place(ratio,mask,1.0 + y/5.0 + (y**2)*(2.0/105.0))
        else:  
            ratio = -1.0
            if(x > 0.1):
                if(self._WK > 0.0):
                    ratio = (0.125*(np.exp(2.0*x)-np.exp(-2.0*x))-x/2.0)
                else:
                    ratio = (x/2.0 - np.sin(2.0*x)/4.0)
                ratio = ratio/((x**3)/3.0)
            else:
                y = x**2
                if(self._WK < 0.0): 
                    y = -y
                ratio = 1.0 + y/5.0 + (y**2)*(2.0/105.0)
        vol = 4.0*np.pi*ratio*(((c/self._H100)*dr/self._Mpc)**3)/3.0
        return vol


    def dVdz(self,z=0.0):
        """
        dVdz() : Returns the comoving volume element dV/dz
                 at redshift, z, for all sky.
        
        dV = (c/H100)*(1+z)**2*D_A**2/E(z) dz dOmega
        
        f(z) = (c/H100)/E(z)
        
        ==> dV/dz(z,all sky) = 4*PI*f(z)*(1+z)**2*D_A**2
             
        
        USAGE: dVdz(z)

        """
        dA = self.angular_diameter_distance(z)
        return self.f(z)*(dA**2)*((1.0+z)**2)*4.0*np.pi
    

    def band_corrected_distance_modulus(self,z=0.0):
        """
        band_corrected_distance_modulus(): returns the Band Corrected
                              Distance Modulus (BCDM) at redshift, z.
        
        USAGE: band_corrected_distance_modulus(z)
            
        FURTHER INFORMATION:
        There is no h dependence as we work always in length units of Mpc/h 
        such that our absolute magnitudes are really Mabs-5logh and no 
        additional h dependence is needed here to get apparent magnitudes 
        that are h independent.
        
        In Galform versions 2.5.1 onwards the additional -2.5 * log10(1.0+z)
        is needed to convert from absolute to apparent magnitude as the 
        definition of absolute magnitude in the Galform code has been changed
        by a factor of (1+z). With the new definition a galaxy with a SED in 
        which f_nu is a constant will, quite sensibly, have the same AB 
        absolute magnitude independent wave band range (including whether it 
        is rest or observer frame) and independent of redshift. 
        
        One way of thinking about this is that while the standard luminosity
        distance and corresponding distance modulus applies to bolometric 
        luminosities, for a filter of finite width the flux depends on the
        band width of the filter in the galaxy's rest frame and it is this 
        that we are taking into account when defining this "band corrected"
        distance modulus. 
        """
        dref = 10.0/constants.mega # 10pc in Mpc
        dL = self.luminosity_distance(z)
        bcdm = 5.0*np.log10(dL/dref) - 2.5*np.log10(1.0+z)
        return bcdm


    def realspace(self,ra,dec,z):
        ra = np.radians(ra)
        dec = np.radians(dec)
        r = self.comoving_distance(z)
        XX = r*np.cos(dec)*np.cos(ra)
        YY = r*np.cos(dec)*np.sin(ra)
        ZZ = r*np.sin(dec)
        return XX,YY,ZZ






# Set cosmology for Millennium simulation
def Millennium(radiation=False):    
    return cosmology(omega0=0.25,lambda0=0.75,omegab=0.045,h0=0.73,\
                 sigma8=0.9,ns=1.0,radiation=radiation)


def WMAP(year=7,radiation=False):
    if year == 1:
        omega0 = 0.25
        lambda0 = 0.75
        omegab = 0.045
        h0 = 0.73
        sigma8 = 0.9
        ns = 1.0
    elif year == 3:
        pass
    elif year == 5:
        pass
    elif year == 7:
        omega0 = 0.272
        lambda0 = 0.728
        omegab = 0.045
        h0 = 0.702
        sigma8 = 0.807
        ns = 0.961
    elif year == 9:
        pass
    else:
        print "*** ERROR: WMAP(): please select one of the following years: 1,3,5,7,9."
        return None
    return cosmology(omega0=omega0,lambda0=lambda0,omegab=omegab,h0=h0,\
                     sigma8=sigma8,ns=ns,radiation=radiation)



def hod(bins,haloid,mhalo,mask=None):
    from utilities_statistics import outside_range
    # If no additional mask supplied, assume using
    # all galaxies
    if mask is None:
        mask = np.ones(len(haloid),bool)
    # Find location of unique halos in arrayof IDs
    id,index,inv = np.unique(haloid[np.where(mask)],\
                             return_index=True,return_inverse=True)
    # Count number of galaxies in each halo
    ngals = np.bincount(inv)
    # Extract masses of halos
    masses = mhalo[np.where(mask)]
    mass = masses[index]
    # Only use halos with masses inside range spanned
    # by mass bins
    mlow = bins[0]
    dm = bins[1] - bins[0]
    mupp = bins[-1] + dm
    hod = np.zeros_like(bins)
    err = np.zeros_like(bins)
    binmask = outside_range(mass,low=mlow,upp=mupp)
    ibins = np.digitize(mass,bins)
    np.place(ibins,binmask,-999)
    # Calculate halo occupation distribution
    for i in range(len(bins)):
        hod[i] = np.mean(ngals[np.where(ibins==i)])
        err[i] = np.std(ngals[np.where(ibins==i)])
    return hod,err

