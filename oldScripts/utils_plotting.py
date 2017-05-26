#! /usr/bin/env python

import sys
import numpy as np
import matplotlib
from utils_statistics import *
from scipy.stats import *

def X11_forwarding():
    import os
    try:
        l = os.environ["DISPLAY"]
    except KeyError:
        return False
    else:
        return True

if not X11_forwarding():
    matplotlib.use('Agg')
    print "WARNING! No X-window detected! Adopting 'Agg' backend..." 
from pylab import *
import matplotlib.pyplot as plt
from decimal import *

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['legend.numpoints'] = 1
#mpl.rcParams['legend.scatterpoints'] = 1
mpl.rcParams['legend.fontsize'] = 'small'
mpl.rcParams['legend.markerscale'] = 1
mpl.rcParams['axes.labelsize'] = 12.0
mpl.rcParams['xtick.labelsize'] = 12.0
mpl.rcParams['ytick.labelsize'] = 12.0


#######################################################################
# FUNCTIONS: LABELS
#######################################################################

def ticklabels_factor(axobj,modify=True,loglimit=4.0):        
    axobj.get_major_formatter().set_useOffset(False)
    offset = axobj.get_major_formatter().get_offset()
    try:
        offset = float(offset)
    except ValueError:
        offset = None
    else:
        offset = float(offset)
    ticks = np.array([float(item.get_text()) for item in axobj.get_ticklabels()])    
    if offset is not None:
        if offset != 0.0:
            ticks = ticks*offset
    if np.nanmax(np.log10(ticks)) > loglimit:
        factor = int(np.floor(np.nanmax(np.log10(ticks)))/2.0)
    elif np.nanmax(np.log10(ticks)) < -loglimit:
        factor = int(np.floor(np.nanmax(np.log10(ticks)))/2.0)
    else:
        factor = 0.0
    if modify:
        axobj.set_ticklabels(ticks/(float(10**factor)))
    return int(10**factor)

def change_axes_fontsize(fs=10.0):
    mpl.rcParams['axes.labelsize'] = fs
    mpl.rcParams['xtick.labelsize'] = fs
    mpl.rcParams['ytick.labelsize'] = fs
    return

def print_rounded_value(x,dx):
    return str(Decimal(str(x)).quantize(Decimal(str(dx))))

def sigfig(x,n,latex=True):
    if n ==0:
        return 0
    fmt = "%."+str(n-1)+"E"
    s = fmt % x
    s = str(float(s))
    if "e" in s:
        s = s.split("e")
        m = n - len(s[0].replace(".","").replace("-","").lstrip("0"))
        s[0] = s[0].ljust(len(s[0])+m,"0")
        if "." in s[0]:
            if len(s[0].split(".")[1].strip("0")) == 0 and len(s[0].split(".")[0]) >= n:
                s[0] = s[0].split(".")[0]
        if latex:
                s[1] = "$\\times 10^{"+str(int(s[1]))+"}$"
        else:
            s[1] = "e" + s[1]
        s = "".join(s)
    else:
        m = n - len(s.replace(".","").replace("-","").lstrip("0"))
        s = s.ljust(len(s)+m,"0")
        if "." in s:
            if len(s.split(".")[1].strip("0")) == 0 and len(s.split(".")[0]) >= n:
                s = s.split(".")[0]
    return s


def get_position(ax,xfrac,yfrac):
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    dx = float(xlims[1]) - float(xlims[0])
    dy = float(ylims[1]) - float(ylims[0])
    xpos = float(xlims[0]) + xfrac*dx
    ypos = float(ylims[0]) + yfrac*dy
    return xpos,ypos

#######################################################################
# FUNCTIONS: LEGENDS
#######################################################################

def Legend(ax,ec='none',fc='none',fontcolor="k",**kwargs):    
    leg = ax.legend(**kwargs)    
    frame = leg.get_frame()
    frame.set_edgecolor(ec)
    frame.set_facecolor(fc)
    for text in leg.get_texts():
        text.set_color(fontcolor)
    return


#######################################################################
# FUNCTIONS: COLOURS
#######################################################################

def colour_array(n=1,i=None,cmap="jet"):
    cm = plt.get_cmap(cmap)
    if cm is None:
        print "*** ERROR: colour_array(): colour map ",cmap," not found!"
        sys.exit(3)
    if n == 1:
        return "k"
    else:
        colarr = np.arange(float(n))/float(n)
        colarr = cm(colarr)
        if i is not None:
            if i in range(n):
                colarr = colarr[i]
        return colarr


def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    import matplotlib.colors as colors
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def get_color(color):
    for hue in range(color):
        hue = 1. * hue / color
        col = [int(x) for x in colorsys.hsv_to_rgb(hue, 1.0, 230)]
        yield "#{0:02x}{1:02x}{2:02x}".format(*col)


def make_colourmap(seq):
    """
    make_colourmap(): Return a LinearSegmentedColormap.

    USAGE: cmap = make_colourmap(seq)

           seq: A sequence of floats and RGB-tuples. The floats should be 
                increasing and be in the interval [0,1].


     e.g.
     import matplotlib.colors as mcolors
     c = mcolors.ColorConverter().to_rgb

     rvb = make_colormap([c('red'), c('violet'), c('blue')])
     
     rvb = make_colormap([c('red'), c('violet'), 0.33, c('violet'),\ 
                         c('blue'), 0.66, c('blue')])

    (From answer in http://stackoverflow.com/questions/16834861/create-own-colormap-using-matplotlib-and-plot-color-scale)

    """
    import matplotlib.colors as mcolors
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return mcolors.LinearSegmentedColormap('CustomMap', cdict)




class MidPointNorm(Normalize):    
    def __init__(self, midpoint=0, vmin=None, vmax=None, clip=False):
        Normalize.__init__(self,vmin, vmax, clip)
        self.midpoint = midpoint

    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        result, is_scalar = self.process_value(value)

        self.autoscale_None(result)
        vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint
        if vmin > 0:
            raise ValueError("minvalue must be less than 0")
        if vmax < 0:
            raise ValueError("maxvalue must be more than 0")       

        if not (vmin < midpoint < vmax):
            raise ValueError("midpoint must be between maxvalue and minvalue.")       
        elif vmin == vmax:
            result.fill(0) # Or should it be all masked? Or 0.5?
        else:
            vmin = float(vmin)
            vmax = float(vmax)
            if clip:
                mask = ma.getmask(result)
                result = ma.array(np.clip(result.filled(vmax), vmin, vmax),
                                  mask=mask)
            # ma division is very slow; we can take a shortcut
            resdat = result.data
            tmp = resdat.copy()

            #First scale to -1 to 1 range, than to from 0 to 1.
            resdat -= midpoint            
            resdat[resdat>0] /= abs(vmax - midpoint)            
            resdat[resdat<0] /= abs(vmin - midpoint)
            #print np.column_stack((resdat, tmp))
            #print vmin, vmax, midpoint
            resdat = resdat/2. + 0.5
            result = np.ma.array(resdat, mask=result.mask, copy=False)

        if is_scalar:
            result = result[0]

        return result

    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until scaled")
        vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint

        if cbook.iterable(value):
            print 'sd', vmin
            val = ma.asarray(value)
            val = 2 * (val-0.5) 
            val[val>0]  *= abs(vmax - midpoint)
            val[val<0] *= abs(vmin - midpoint)
            val += midpoint
            return val
        else:
            val = 2 * (val - 0.5)
            if val<0: 
                return  val*abs(vmin-midpoint) + midpoint
            else:
                return  val*abs(vmax-midpoint) + midpoint


#######################################################################
# FUNCTIONS: TICKS
#######################################################################

def minor_ticks(axObj):
    """
    minor_ticks(): display minor tick marks on plot.

    USAGE: minor_ticks(axObj)

           axObj : axis object e.g. ax or ax.xaxis or ax.yaxis
                  (If ax, will plot ticks on both X and Y axes)

    """
    if str(axObj).startswith("Axes"):
        axObj =[axObj.xaxis,axObj.yaxis]
    else:
        axObj =[axObj]
    for ax in axObj:
        # Determine major tick intervals
        major_tick_locations = ax.get_majorticklocs()
        major_tick_interval = major_tick_locations[1] - major_tick_locations[0]
        # Create dummy figure
        dummyfig = plt.figure()
        dummyax = dummyfig.add_subplot(111)
        # Create dummy data over range of major tick interval
        dummyx = np.arange(0,np.fabs(major_tick_interval) + \
                               np.fabs(major_tick_interval)/10.0, \
                               np.fabs(major_tick_interval)/10.0)
        dummyax.plot(dummyx,dummyx)
        # Get minor tick interval by using automatically generated
        # major tick intervals from dummy plot
        minor_tick_locations = dummyax.xaxis.get_majorticklocs()
        minor_tick_interval = minor_tick_locations[1] - minor_tick_locations[0]
        plt.close(dummyfig)
        ax.set_minor_locator(MultipleLocator(base=minor_tick_interval))
    return

#######################################################################
# FUNCTIONS: VISUALISE STATISTICS
#######################################################################

def ImageStats2D(ax,X,Y,Xbins,Ybins,Z=None,statistic="count",\
                           weights=None,func=None,**kwargs):
    """
    statistic can be: mean,median,sum,product,std,var,percentile,avg,max,min,mode
    NB 'avg' is weighted average
    """
    # Calculate statistic in 2-dimension bins
    data,xedges,yedges,numb = binstats2D(X,Y,Xbins,Ybins=Ybins,Z=Z,\
                                             statistic=statistic,weights=weights)
    if func is not None:
        data = func(data)
    if np.any(np.isinf(data)):
        np.place(data,np.isinf(data),np.NaN)
    extent = [xedges[0],xedges[-1],yedges[0],yedges[-1]]
    # Set default preferences for selected keyword arguments
    if "extent" not in kwargs.keys():
        kwargs["extent"] = extent
    if "interpolation" not in kwargs.keys():
        kwargs["interpolation"] = "nearest"
    if "aspect" not in kwargs.keys():
        kwargs["aspect"] = "auto"
    if "origin" not in kwargs.keys():
        kwargs["origin"] = "lower"
    axim = ax.imshow(np.transpose(data),**kwargs)
    return axim


def plot_medians(ax,x,y,xbins,prange=(10,90),shade=False,**kwargs):
    med,bins,binnumb = binstats(x,y,xbins,statistic="median")
    low,bins,binnumb = binstats(x,y,xbins,statistic=prange[0])
    upp,bins,binnumb = binstats(x,y,xbins,statistic=prange[1])
    bw = bins[1] - bins[0]
    if shade:
        line, = ax.plot(bins[:-1]+bw/2.0,med,**kwargs)
        ax.fill_between(bins[:-1]+bw/2.0,low,upp,alpha=0.5,edgecolor='none',
                        facecolor=line.get_color())
    else:
        ax.errorbar(bins[:-1]+bw/2.0,med,yerr=[med-low,upp-med],**kwargs)
    return



def xyhistsubplots_axes(subplot=111,xsubplot="top",ysubplot="right",\
                        fig=None,xlim=None,ylim=None,xlabel=None,ylabel=None):
    """
    xyhistsubplots_axes(): Set up the axes for a three panel plot with
                           a large central panel and smaller subpanels
                           attached to the x/y axes. Returns the axis
                           objects for the various panels so that user
                           can add data, add labels, add colorbar,
                           add legend, change limits, etc.

    USAGE: ax,axsubx,axsuby = xyhistsubplots_axes(subplot,xsubplot,ysubplot,\
                        [fig],[xlim],[ylim],[xlabel],[ylabel])

           subplot  : 3 digit code for subplot (Default = 111)
           xsubplot : define location of x-axis subpanel [ = 'top' | 'bottom' ]
                      Default = 'top'
           ysubplot : define location of y-axis subpanel [ = 'left' | 'right' ]
                      Default = 'right'
               fig  : figure object
               xlim : 2 element array/list to control x limits of main panel and
                      x-subpanel [xmin,xmax] (If None, no limits will be set)
               ylim : 2 element array/list to control y limits of main panel and
                      y-subpanel [ymin,ymax] (If None, no limits will be set)
             xlabel : string containing x-axis label (If None, no label will be printed)
             ylabel : string containing y-axis label (If None, no label will be printed)          

                 ax : axis object for main panel
             axsubx : axis object for x-axis subpanel
             axsuby : axis object for y-axis subpanel

       N.B. a) When limits are specified, minor tick marks will be displayed.
            b) If no limits/labels are specified for x,y then will need to be set 
               manually outside of function.
            c) No y,x labels printed for x,y-subpanels

    """
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    if fig is None:
        fig = figure(figsize=(8,8))

    # Use figure size to set height/width og x/y subpanels
    w = fig.get_figwidth()
    h = fig.get_figheight()
    subw = ((w+h)/2.0)*0.18
    
    # Make axes -- divide up to make subpanels
    ax = fig.add_subplot(subplot)
    divider = make_axes_locatable(ax)

    axsuby = divider.append_axes(ysubplot,subw,pad=0.0,sharey=ax)
    axsubx = divider.append_axes(xsubplot,subw,pad=0.0,sharex=ax)

   
    # Hide appropriate axis labels depending on position of subpanels
    if xsubplot == "top":
        plt.setp(axsubx.get_xticklabels(),visible=False)
        if xlabel is not None:
            ax.set_xlabel(xlabel)
    if xsubplot == "bottom":
        plt.setp(ax.get_xticklabels(),visible=False)
        if xlabel is not None:
            axsubx.set_xlabel(xlabel)
    if ysubplot == "right":
        plt.setp(axsuby.get_yticklabels(),visible=False)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
    if ysubplot == "left":
        plt.setp(ax.get_yticklabels(),visible=False)
        if ylabel is not None:
            axsuby.set_ylabel(ylabel)

    # If limits specified, set limits and show minor ticks
    # for that axis
    if xlim is not None:
        ax.set_xlim(xlim[0],xlim[1])
        axsubx.set_xlim(xlim[0],xlim[1])
        minor_ticks(ax.xaxis)
        minor_ticks(axsubx.xaxis)
    if ylim is not None:
        ax.set_ylim(ylim[0],ylim[1])
        axsuby.set_ylim(ylim[0],ylim[1])
        minor_ticks(ax.yaxis)
        minor_ticks(axsuby.yaxis)
        
    return ax,axsubx,axsuby


def multi_residuals_axes(fig=None,ratio=3,nplots=2,wspace=0.2,\
                   x_lim=None,y_lim=None,sub_ylim=None,\
                   x_label=None,y_label=None,sub_ylabel=None):
    
    import matplotlib.gridspec as gridspec

    if fig is None:
        fig = figure(figsize=(8*nplots,8))
    gs = gridspec.GridSpec(2, nplots,
                           height_ratios=[ratio,1]
                           )
    ax = list()
    for i in range(nplots):
        if i == 0 or ((i>0)and(np.fabs(wspace-0.0)>1.0e-6)):
            ax.append([fig.add_subplot(gs[0,i]),fig.add_subplot(gs[1,i])])
            if ylabel is not None:
                ax[i][0].set_ylabel(y_label)
            if y_lim is not None:
                ax[i][0].set_ylim(y_lim[0],y_lim[1])
                minor_ticks(ax[i].yaxis)
            if sub_ylabel is not None:
                ax[i][1].set_ylabel(sub_ylabel)
            if sub_ylim is not None:
                ax[i][1].set_ylim(sub_ylim[0],sub_ylim[1])
                minor_ticks(ax[i][1].yaxis)
        else:
            ax.append([fig.add_subplot(gs[0,i],sharey=ax[i-1][0]),\
                       fig.add_subplot(gs[1,i],sharey=ax[i-1][1])])
            plt.setp(ax[i][0].get_xticklabels(),visible=False)
            plt.setp(ax[i][0].get_yticklabels(),visible=False)
            plt.setp(ax[i][1].get_yticklabels(),visible=False)
            if y_lim is not None:
                minor_ticks(ax[i][0].yaxis)
                minor_ticks(ax[i][1].yaxis)
        if xlabel is not None:
            ax[i][1].set_xlabel(x_label)
        if x_lim is not None:
            ax[i][0].set_xlim(x_lim[0],x_lim[1])
            ax[i][1].set_xlim(x_lim[0],x_lim[1])
            minor_ticks(ax[i][0].xaxis)
            minor_ticks(ax[i][1].xaxis)
        plt.setp(ax[i][0].get_xticklabels(),visible=False)
            
    subplots_adjust(hspace=0.0,wspace=wspace)
    return ax

def residuals_axes(fig=None,ratio=3,nplots=1,\
                   x_lim=None,y_lim=None,sub_ylim=None,\
                   x_label=None,y_label=None,sub_ylabel=None):
    
    import matplotlib.gridspec as gridspec
    if fig is None:
        fig = figure(figsize=(8,8))

    gs = gridspec.GridSpec(2, 1,
                       height_ratios=[ratio,1]
                       )
    
    ax = fig.add_subplot(gs[0])
    axSub = fig.add_subplot(gs[1],sharex=ax)
    subplots_adjust(hspace=0.0)

    plt.setp(ax.get_xticklabels(),visible=False)
    if x_lim is not None:
        ax.set_xlim(x_lim[0],x_lim[1])
        axSub.set_xlim(x_lim[0],x_lim[1])
        minor_ticks(ax.xaxis)
        minor_ticks(axSub.xaxis)
    if y_lim is not None:
        ax.set_ylim(y_lim[0],y_lim[1])
        minor_ticks(ax.yaxis)
    if sub_ylim is not None:
        axSub.set_ylim(sub_ylim[0],sub_ylim[1])
        minor_ticks(axSub.yaxis)
    if xlabel is not None:
        axSub.set_xlabel(x_label)
    if ylabel is not None:
        ax.set_ylabel(y_label) 
    if sub_ylabel is not None:
        axSub.set_ylabel(sub_ylabel)  
 
    return ax,axSub


#######################################################################
# FUNCTIONS: MISC
#######################################################################

def one2one(ax,X,Y,Xbins,Ybins=None,cmap="jet",vmin=None,vmax=None,\
            inc_colorbar=True):

    if Ybins is None:
        Ybins = np.copy(Xbins)
    data,xedges,yedges = np.histogram2d(X,Y,bins=[Xbins,Ybins])
    extent = [xedges[0],xedges[-1],yedges[0],yedges[-1]]
    data /= float(np.sum(data))
    if vmin is not None or vmax is not None:
        norm = matplotlib.colors.Normalize(vmin=vmin,vmax=vmax)
    else:
        norm = None
    cm = get_cmap(cmap)
    axim = ax.imshow(np.transpose(data),extent=extent,interpolation='nearest',\
                     cmap=cm,aspect='auto',origin='lower',norm=norm)
    if colorbar:
        cbar = colorbar(axim,pad=0.01)
        cbar.set_label("Fraction of catalogue")
    return axim

def add_1to1_line(ax,xmin=None,xmax=None,**kwargs):
    xlims = ax.get_xlim()
    ylims = ax.get_ylim()
    if xmin is None:
        xmin = np.minimum(xlims[0],ylims[0])
    if xmax is None:
        xmax = np.maximum(xlims[1],ylims[1])
    x = np.arange(xmin,10.0*xmax,(10.0*xmax-xmin)*0.2)
    ax.plot(x,x,**kwwargs)
    return

