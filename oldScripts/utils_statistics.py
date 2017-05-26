#!/usr/bin/env python

import numpy as np
import math
from scipy.stats import *



def count_occurences(x,y=None):
    """
    count_occurencens(): Return unique values in x and number
                         of times each value appears. If provided
                         with an additional array, y, will count
                         the numberof times each value of y appears
                         in x.

    USAGE: u,n = count_occurences(x,y)

           x  = array of integers
           y  = array of unique values to look for in x
           u = array of unique values in x or y
           n = number of times each value in u appears in x
    """
    if y is None:
        ux,inv = np.unique(x,return_inverse=True)
        nx = np.bincount(inv)
        return ux,nx
    else:
        isort = np.argsort(y)
        jsort = np.argsort(isort)
        counts,extent = np.histogram(x,np.append(np.copy(y[isort]),\
                                                 np.max(y)+1))
        return y,counts[jsort]


def histogram_data(x,xbins,weights=None,cumulative=False):
    bw = xbins[1] - xbins[0]
    bins = np.copy(xbins)    
    bins = np.append(bins,np.ones(1)*(xbins[-1]+bw))
    if weights is None:
        weights = np.ones_like(x)
        if not cumulative:
            weights = weights*(1.0/bw)
    hist,dummy = np.histogram(x,bins,weights=weights)
    if cumulative:
        hist = np.cumsum(hist)
    return hist

        
    
def random_sample_mask(n,percent):
    """
    random_sample(): Returns a mask array with single
                     dimension 'n', that will select
                     approximately the specified
                     percentage of data (assuming data
                     is in an array also of size 'n')
    USAGE: mask = random_sample(n,percent)

           n       : length of mask array
           percent : percent to select
           mask    : logical array with specified
                     percentage of values set to True
                      
    """
    import random
    frac = float(percent)/100.0
    frac = int(np.ceil(frac*float(n)))
    index = random.sample(np.arange(int(n)),frac)
    mask = np.zeros(n,bool)
    mask[index] = True
    return mask



def binstats(X,Y,Xbins,statistic="median",weights=None,mask=None):
    
    if weights is None:
        weights = np.ones_like(X)
    if mask is None:
        mask = np.ones(len(X),bool)
    statistic = str(statistic)
    try:
        p = float(statistic)
        def perc(x):
            return np.percentile(x,q=p)
        statistic = perc
    except ValueError:
        if statistic.lower().startswith("perc"):
            statistic = None                
        elif statistic.lower() in ["average","avg"]:
            def avg(x):
                return np.average(x,weights=weights)
            statistic = avg
        elif statistic.lower() == "std":
            statistic = np.std
        elif statistic.lower() == "var":
            statistic = np.var
        elif statistic.lower().startswith("prod"):
            statistic = np.prod
        elif statistic.lower().startswith("min"):
            statistic = np.nanmin
        elif statistic.lower().startswith("max"):
            statistic = np.nanmax
        elif statistic.lower() == "mode":
            def mode_of_data(x):
                return mode(x)[0][0]
            statistic = mode_of_data
        elif statistic.lower() == "mad":
            def mad(x):
                return np.median(np.fabs(x-np.median(x)))
            statistic = mad        
        else:
            pass
    if statistic is None:
        result,bin_edges,binnumber = binned_statistic(X[mask],Y[mask],statistic="count",bins=Xbins)
        result = result*100.0/float(np.sum(result))
    else:
        result,bin_edges,binnumber = binned_statistic(X[mask],Y[mask],statistic=statistic,bins=Xbins)
    return result,bin_edges,binnumber

    
def binstats2D(X,Y,Xbins,Ybins=None,Z=None,statistic="median",weights=None):
    """
    statistic can be: mean,median,sum,product,std,var,percentile,avg,max,min,mode,fraction,percentage

    NB 'avg' is weighted average
    """
    if statistic is None:
        statistic = "count"
    if Ybins is None:
        Ybins = np.copy(Xbins)
    bins = [Xbins,Ybins]
    if Z is None:
        Z = np.ones_like(X)
    statistic = str(statistic)
    try:
        p = float(statistic)
        def perc(x):
            return np.percentile(x,q=p)
        statistic = perc
    except ValueError:
        if statistic.lower().startswith("perc"):
            pass
        elif statistic.lower().startswith("frac"):
            pass
        elif statistic.lower() in ["average","avg"]:
            if weights is None:
                weights = np.ones_like(X)
            def avg(x):
                return np.average(x,weights=weights)
            statistic = avg
        elif statistic.lower() == "std":
            statistic = np.std
        elif statistic.lower() == "var":
            statistic = np.var
        elif statistic.lower().startswith("prod"):
            statistic = np.prod
        elif statistic.lower().startswith("min"):
            statistic = np.nanmin
        elif statistic.lower().startswith("max"):
            statistic = np.nanmax
        elif statistic.lower() == "mode":
            def mode_of_data(x):
                return mode(x)[0][0]
            statistic = mode_of_data
        else:
            pass
    if statistic.lower() == "count":
        stat,xedges,yedges,numb = binned_statistic_2d(X,Y,Z,statistic="count",bins=bins)
        if weights is not None:
            stat,xedges,yedges = np.histogram2d(X,Y,bins=bins,weights=weights)        
    elif any([statistic.lower().startswith("perc"),statistic.lower().startswith("frac")]):
        stat,xedges,yedges,numb = binned_statistic_2d(X,Y,Z,statistic="count",bins=bins)
        stat = stat/float(np.sum(stat))       
        if statistic.lower().startswith("perc"):
            stat = stat*100.0
    else:
        stat,xedges,yedges,numb = binned_statistic_2d(X,Y,Z,statistic=statistic,bins=bins)
    stat = Inf2NaN2D(stat)
    return stat,xedges,yedges,numb


def Inf2NaN2D(arr):
    """
    Inf2NaN2d(): Converts all +/-Inf in a 2D array to NaN.
                 (Useful when plotting images of arrays that
                 have been divided or logged).

    USAGE: arr = Inf2NaN2D(arr)

           arr : input/output array, with +/Inf in input
                 and NaN on output.
                 
    """
    mask = np.isinf(arr)
    arr[mask] = np.NaN
    return arr


def AND(*args):
    return [all(tuple) for tuple in zip(*args)]

def OR(*args):
    return [any(tuple) for tuple in zip(*args)]

    
def chi_squared(ex,ob,er):
    chi_sq = np.sum(((ob-ex)/er)**2)
    return chi_sq


def weighted_percentile(y,w,p,sorted=False,axis=None):
    from scipy import interpolate
    if not sorted:
        isort = np.argsort(w,axis=axis)
        y = y[isort]
        w = w[isort]
    wp = np.percentile(w,p,axis=axis)
    f = interpolate.interp1d(w,y,axis=axis)
    return f(wp)
