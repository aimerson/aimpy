#! /usr/bin/env

import numpy as np
from scipy.interpolate import interp1d


class chiSquared(object):

    def __init__(self,obsX,obsY,obsYErr=None):
        # Store observations and error
        self.obsX = np.copy(obsX)
        self.obsY = np.copy(obsY)
        assert(len(self.obsX)==len(self.obsY))
        self.obsYErr = None
        if obsYErr is not None:
            if type(obsYErr) == tuple:
                self.obsYErr = np.copy(np.sqrt(obsYErr[0]**2+obsYErr[1]**2))
            elif np.ndim(obsYErr) == 1:
                self.obsYErr = np.copy(obsYErr)
                assert(len(self.obsYErr)==len(self.obsY))
            elif np.ndim(obsYErr) == 2:
                pass
        return

    def chiSquared(self,modelY):
        # From https://en.wikipedia.org/wiki/Reduced_chi-squared_statistic
        assert(len(self.obsY)==len(modelY))
        result = (self.obsY-modelY)**2
        if self.obsYErr is None:
            result /= modelY
        else:
            result /= self.obsYErr**2
        return np.sum(result)

    def getChiSquared(self,modelX,modelY,reduced=True,dof=None,**kwargs):
        model = interp1d(modelX,modelY,**kwargs)
        result = self.chiSquared(model(self.obsX))
        if reduced:
            if dof is not None:
                result /= float(dof)
            else:
                result /= float(len(self.obsY))*2-2.0
        return result
