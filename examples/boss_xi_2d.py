#! /usr/bin/env python


from aimpy.plotting.utils import *
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.lines import Line2D

########################################################################################
# Classes and functions
########################################################################################

def loadCorrData(datfile,model=False):
    dtype = [("x",float),("y",float),("xi",float)]
    if model:
        usecols = [ 1, 0, 2]
    else:
        usecols = [ 0, 1, 2]
    data = np.loadtxt(datfile,dtype=dtype,usecols=usecols)
    data = data.view(np.recarray)
    X = data.x.reshape(200,200)
    Y = data.y.reshape(200,200)
    Z = data.xi.reshape(200,200)    
    return X,Y,Z


class Xi2DContours(object):
    
    def __init__(self,figsize=(8,8),rmax=200.0):
        self.fig = figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111)
        self.rmax = rmax
        self.extent = [0.0,self.rmax,0.0,self.rmax]
        self.proxy = []
        self.labels = []
        return

    def addData(self,datfile,levelsPOS,levelsNEG,sigma=None,transpose=False,color='k',label="Data"):
        # Load dataset
        X,Y,Z = loadCorrData(datfile,model=False)
        if sigma is not None:        
            Z = gaussian_filter(Z,sigma)
        if transpose:
            Z = Z.transpose()
        # Plot contour data
        DATA1 = self.ax.contour(Z,extent=self.extent,levels=levelsPOS,linewidths=1,colors=color,linestyles='solid')        
        DATA2 = self.ax.contour(Z,extent=self.extent,levels=levelsNEG,linewidths=1,colors=color,linestyles='dotted')       
        # Create proxy datasets for constructing legend
        dummy = np.array([-100,-101,-102])
        self.proxy.append(Line2D(dummy,dummy,c=DATA1.collections[0].get_color()[0]))
        self.labels.append(label+" ($\\xi\,>\,0$)") 
        self.proxy.append(Line2D(dummy,dummy,c=DATA2.collections[0].get_color()[0],ls=DATA2.collections[0].get_linestyle()[0]))
        self.labels.append(label+" ($\\xi\,<\,0$)")
        return
    
    def addModel(self,modfile,levelsPOS,DAbar=0.9866,Hbar=0.989,fac=3.5,sigma=None,transpose=False,color='r',label="Model"):        
        # Load dataset
        X,Y,Z = loadCorrData(modfile,model=True)
        Z *= fac*Hbar/DAbar
        if sigma is not None:        
            Z = gaussian_filter(Z,sigma)
        if transpose:
            Z = Z.transpose()
        # Plot contour data
        MODEL = self.ax.contour(Z,extent=self.extent,levels=levelsPOS,linewidths=1,colors=color,linestyles='dashed')
        # Create proxy dataset for constructing legend
        dummy = np.array([-100,-101,-102])
        self.proxy.append(Line2D(dummy,dummy,c=MODEL.collections[0].get_color()[0],ls=MODEL.collections[0].get_linestyle()[0]))
        self.labels.append(label)
        return

    def addCircle(self,radius,center=(0.0,0.0),**kwargs):
        circle = Circle(center,radius,**kwargs)
        self.ax.add_artist(circle)
        return
    
    def addAnnulus(self,minradius,maxradius,center=(0.0,0.0),angles=(0.0,90.0),**kwargs):        
        wedge = Wedge(center,maxradius,angles[0],angles[1],width=maxradius-minradius,**kwargs)
        self.ax.add_artist(wedge)
        return
    
    def addvline(self,x,**kwargs):
        self.ax.axvline(x,**kwargs)

    def addhline(self,y,**kwargs):
        self.ax.axhline(y,**kwargs)

    def output(self,outfile="xi2D_contours.pdf",legend=True,loc=0,fontsize=14,title=None):        
        # Set axis labels and limits and ticks
        self.ax.set_xlabel("Transverse Separation ($h^{-1}\mathrm{Mpc}$)",fontsize=fontsize)
        self.ax.set_ylabel("Line-of-Sight Separation ($h^{-1}\mathrm{Mpc}$)",fontsize=fontsize)        
        self.ax.set_xlim(0.0,self.rmax)
        self.ax.set_ylim(0.0,self.rmax)
        minor_ticks(self.ax)               
        self.ax.tick_params(axis='both',which='major',labelsize=fontsize)
        # Add title?
        if title is not None:
            self.ax.title(title)
        # Add legend?
        if legend:
            self.ax.legend(self.proxy,self.labels,loc=loc,fontsize=fontsize)
        # Plot to file
        print("Plot written to file: "+outfile)
        savefig(outfile,bbox_inches='tight')


########################################################################################
# Main code
########################################################################################

# Create contours plot object
XI2D = Xi2DContours(figsize=(8,8),rmax=200.0)

# Set positive and negative contour levels
levelsPOS = np.array([0.0025,0.005,0.01,0.025,0.1,0.5,2.0,10.0])
levelsNEG = np.array([-10.0,0.0])

# Plot DR10 data
datfile = 'DR10v8_all_pisi_z43z7_50x_bin1.twod.corr'
XI2D.addData(datfile,levelsPOS,levelsNEG,sigma=2.0,transpose=False,color='black',label="BOSS DR10")

# Plot DR10 data again (different smoothing scale -- for demonstration -- can comment out)
#XI2D.addData(datfile,levelsPOS,levelsNEG,sigma=1.0,transpose=False,color='orange',label="BOSS DR10 $\sigma\,=\,1$")

# Plot model data
modfile = 'modelxi2D_Omd264Obd0456hd7nsd98_zd57_ksd19_bed3_fgd45_sigv263_Q18d4f3.dat'
XI2D.addModel(modfile,levelsPOS,sigma=2.0,transpose=True,color='red',label="Model")

# Add annulus and circle and vertical line
# Note on keyword options:
# fc = face color --> will work with any HTML color name (see: http://www.w3schools.com/colors/colors_names.asp)
# ec = edge color --> also works with any HTML color name
# ls = line style -->  solid (-), dashed (--), dotted (:) or dashdot (-.)
# lw = line weight
# alpha = set transparency between 1=opaque and 0=transparent
XI2D.addAnnulus(50,150,center=(0.0,0.0),angles=(0.0,90.0),fc='LightGrey',ec='none',alpha=0.5) 
XI2D.addCircle(105.0,center=(0.0,0.0),fc='none',ec='blue',ls=':',lw=3.0)
XI2D.addvline(10.0,c='green',ls=':',lw=2.0)

# Finish up plot and output to file
# Note: loc sets position of legend (see http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.legend)
XI2D.output(outfile="BOSS_DR10_xi_2D.pdf",legend=True,loc=1,fontsize=14,title=None)

