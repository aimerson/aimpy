#! /usr/bin/env python

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import fmin
from scipy.stats import chi2
import scipy

class chiSquared(object):

    def __init__(self,obsX,obsY,obsYErr):
        # Store observations and error
        self.obsX = np.copy(obsX)
        self.obsY = np.copy(obsY)
        if np.ndim(obsYErr)==1:
            self.obsYErr_negative = np.copy(obsYErr)
            self.obsYErr_positive = np.copy(obsYErr)
        else:
            self.obsYErr_negative = np.copy(obsYErr[:,0])
            self.obsYErr_positive = np.copy(obsYErr[:,1])
        return

    def chiSquared(self,modelY):
        result = (self.obsY-modelY)**2
        errors = np.copy(self.obsYErr_positive)
        mask = self.obsY-modelY > 0.0
        np.place(errors,mask,self.obsYErr_negative[mask])
        result /= errors**2
        return np.sum(result)

    def getChiSquared(self,modelX,modelY,DOF=1.0,**kwargs):
        model = interp1d(modelX,modelY,**kwargs)
        result = self.chiSquared(model(self.obsX))/DOF
        return result

    def getPDF(self,X,redChiSq,DOF):
        P = np.exp(-float(DOF)*redChiSq/2.0)
        maxP = P.max()
        return interp1d(X,P/maxP)
        
    def samplePDF(self,Ns,X,redChiSq,DOF):
        PDF = self.getPDF(X,redChiSq,DOF)
        samples = []
        while len(samples) < Ns:
            dX = X.max() - X.min()
            x = np.random.rand(Ns)*dX + X.min()
            prob = PDF(x)
            mask = np.random.rand(Ns) <= prob
            samples = samples + list(x[mask])
        return np.array(samples)

    def getMinimumChiSq(self,chiSq,returnIndex=True):
        imin = np.argmin(chiSq)
        if returnIndex:
            return chiSq[imin],imin
        return chiSq[imin]

    def getSigmaErrorDifference(self,DOF,sigma=1.0):
        conf_int = chi2.cdf(sigma**2,1)
        return chi2.ppf(conf_int,DOF)

    def getParameterMinimum(self,X,chiSq,returnChiSq=True,**kwargs):
        C = interp1d(X,chiSq,fill_value=np.nan,bounds_error=False)
        minC,imin = self.getMinimumChiSq(chiSq)
        Xmin = fmin(C,X[imin],**kwargs)[0]
        if returnChiSq:
            return Xmin,float(C(Xmin))
        return Xmin
    
    def getParameterRange(self,X,chiSq,DOF,sigma=1.0,**kwargs):
        Xmin,Cmin = self.getParameterMinimum(X,chiSq,**kwargs)
        diff = self.getSigmaErrorDifference(DOF,sigma=sigma)
        Cdiff = Cmin + diff/DOF
        mask = X<Xmin
        f = interp1d(chiSq[mask][::-1],X[mask][::-1],bounds_error=False,fill_value='extrapolate')
        Xlow = float(f(Cdiff))
        mask = X>Xmin
        f = interp1d(chiSq[mask],X[mask],bounds_error=False,fill_value='extrapolate')
        Xupp = float(f(Cdiff))
        return Xlow,Xupp

   
def ConfidenceLevelsTable():    
    # stand deviations to calculate
    sigma = [   1.0,
                np.sqrt(chi2.ppf(0.8,1)),
                np.sqrt(chi2.ppf(0.9,1)),
                np.sqrt(chi2.ppf(0.95,1)),
                2.0,
                np.sqrt(chi2.ppf(0.99,1)),
                3.0,
                np.sqrt(chi2.ppf(0.999,1)),
                4.0   ]    
    # confidence intervals these sigmas represent:
    conf_int = [ chi2.cdf( s**2,1) for s in sigma ]
    # degrees of freedom to calculate
    dof = range(1,21)
    print("sigma     \t" + "\t".join(["%1.2f"%(s) for s in sigma]))
    print("conf_int  \t" + "\t".join(["%1.2f%%"%(100*ci) for ci in conf_int]))
    print("p-value   \t" + "\t".join(["%1.5f"%(1-ci) for ci in conf_int]))    
    for d in dof:
        chi_squared = [ chi2.ppf( ci, d) for ci in conf_int ]
        print("chi2(k=%d)\t"%d + "\t".join(["%1.2f" % c for c in chi_squared]))
    return
        
        
    
    
        
