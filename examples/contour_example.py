#! /usr/bin/env python



from aimpy.plotting.utils import *
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from matplotlib.patches import Circle, Wedge, Polygon

filled_contours = False


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



# Open figure and create axis
fig = figure(figsize=(8,8))
ax = fig.add_subplot(111)

# Set contour levels
levels = np.array([0.0025,0.005,0.01,0.025,0.1,0.5,2.0,10.0])
neg = np.array([-10.0,0.0])
colarr = colour_array(n=len(levels),cmap="binary")
# Set signam for Gaussian smoothing
sigma = 2.0

rmax = 200.0
extent = [0.0,rmax,0.0,rmax]


# Load DR10 correlation data
datfile = 'DR10v8_all_pisi_z43z7_50x_bin1.twod.corr'
X,Y,Z = loadCorrData(datfile)
ZZ = gaussian_filter(Z,sigma)
print(ZZ.min(),ZZ.max())

#extent = [X.min(),X.max(),Y.min(),Y.max()]
#low = np.floor(ZZ.min()*10.0)/10.0
#upp = np.ceil(ZZ.max())
label = "BOSS DR10"
if filled_contours:
    ctrs = ax.contourf(ZZ,extent=extent,levels=levels,linewidths=1,linestyles='solid',colors=colarr,label=label)
    cbar = colorbar(ctrs,pad=0.0)
else:
    ctrs = ax.contour(ZZ,extent=extent,levels=levels,linewidths=1,colors='k',label=label)
    ctrs = ax.contour(ZZ,extent=extent,levels=neg,linewidths=1,colors='k',linestyles='dotted',label=label)
    
# Load model correlation data
datfile = 'modelxi2D_Omd264Obd0456hd7nsd98_zd57_ksd19_bed3_fgd45_sigv263_Q18d4f3.dat'
X,Y,Z = loadCorrData(datfile,model=True)
ZZ = gaussian_filter(Z,sigma)
ZZ = ZZ.transpose()
print(ZZ.min(),ZZ.max())

#extent = [X.min(),X.max(),Y.min(),Y.max()]
#low = np.floor(ZZ.min()*10.0)/10.0
#upp = np.ceil(ZZ.max())
label = "Model"
filled_contours = False
if filled_contours:
    ctrs = ax.contourf(ZZ,extent=extent,levels=levels,linewidths=1,linestyles='solid',colors=colarr,label=label)
    cbar = colorbar(ctrs,pad=0.0)
else:
    ctrs = ax.contour(ZZ,extent=extent,levels=levels,linewidths=1,colors='r',linestyles='dashed',label=label)






wedge = Wedge((0,0),150,0,90,width=100,fc='LightGrey',ec='none')
ax.add_artist(wedge)
circle = Circle((0,0),105.0,fc='none',ec='b',ls=':',lw=3.0)
ax.add_artist(circle)

xpos,ypos = get_position(ax,0.95,0.95)
label = "BOSS DR10 (black) vs model (red)"
ax.text(xpos,ypos,label,ha='right',va='top',bbox=dict(fc='w',ec='k',pad=10.0),fontsize=12)



ax.axvline(10.0,c='g',ls='--',lw=2.0)


ax.set_xlabel("Transverse Separation ($h^{-1}\mathrm{Mpc}$)")
ax.set_ylabel("Line-of-Sight Separation ($h^{-1}\mathrm{Mpc}$)")
minor_ticks(ax)

savefig("boss_2d_corr.pdf",bbox_inches='tight')



quit()


fig = figure(figsize=(6,18))
subplots_adjust(hspace=0.05)

for i in range(3):
    ax = fig.add_subplot(311+i)    

    counts,xbins,ybins=np.histogram2d(x,y,bins=100)
    ax.contour(counts.transpose(),extent=[xbins.min(),xbins.max(),\
                                              ybins.min(),ybins.max()],linewidths=1,colors='k',\
                   linestyles='solid')
    

    circle = Circle((0,0),.5,fc='DarkBlue',ec='none',alpha=0.5)
    ax.add_artist(circle)

    if i == 2:
        ax.set_xlabel("X axis [$h^{-1}\mathrm{Mpc}$]",fontsize=12)
    else:
        setp(ax.xaxis.get_ticklabels(),visible=False)
    ax.set_ylabel("Y axis [$h^{-1}\mathrm{Mpc}$]",fontsize=12)

    ax.set_xlim(0.0,1.0)
    ax.set_ylim(0.0,0.99)

    


savefig("contour_example.pdf",bbox_inches='tight')

