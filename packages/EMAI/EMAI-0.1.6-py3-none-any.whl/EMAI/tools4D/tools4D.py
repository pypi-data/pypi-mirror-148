import numpy as np
import matplotlib.pyplot as plt
from skimage import draw
from scipy.ndimage import gaussian_filter
import glob
import os
from typing import List, Tuple, Type
import json
import matplotlib.gridspec as gridspec
from scipy import ndimage
from scipy import signal
import operator
from scipy import interpolate
import matplotlib.patches as patches
from skimage.transform import resize
import cv2

# Basic ML modules
from sklearn.decomposition import NMF
from sklearn.decomposition import PCA
from scipy.signal import find_peaks

# Helps with FFT analysis
import scipy.fft
from skimage.feature import peak_local_max
from skimage.transform import resize
from scipy.spatial import cKDTree
from skimage.feature import blob_log

# For polarization maps
from scipy import spatial
from copy import deepcopy as dc
from scipy.interpolate import griddata

import atomai as aoi



def COM(nysamp, nxsamp, nypix, nxpix, duin, dvin,CBED_in):
    from scipy import ndimage
    import math
    
    com_mag = np.zeros((nysamp, nxsamp))
    com_y = np.zeros((nysamp, nxsamp))
    com_x = np.zeros((nysamp, nxsamp))
    angle = np.zeros((nysamp, nxsamp))
    xyzero = np.zeros(2)
    xyzero = ndimage.measurements.center_of_mass(np.mean(CBED_in, axis=(0,1)) )   
#    xyzero[0] = nypix/2
#    xyzero[1] = nxpix/2
    
    for y in range(nysamp):
        for x in range(nxsamp):
            xycbed = ndimage.measurements.center_of_mass(CBED_in[y,x,:,:])
            com_x[y,x] = (xycbed[1]-xyzero[1])*duin
            com_y[y,x] = (xycbed[0]-xyzero[0])*dvin
            com_mag[y,x] = math.sqrt(com_y[y,x]*com_y[y,x]+com_x[y,x]*com_x[y,x])  
            
    angle = np.arctan2(com_y,com_x)  
    
    return com_y, com_x, angle, com_mag


def COM_full(nysamp, nxsamp, nypix, nxpix, duin, dvin,CBED_in):
    from scipy import ndimage
    import math
    
    com_mag = np.zeros((nysamp, nxsamp))
    com_y = np.zeros((nysamp, nxsamp))
    com_x = np.zeros((nysamp, nxsamp))
    angle = np.zeros((nysamp, nxsamp))
    xyzero = np.zeros(2)
    xyzero = ndimage.measurements.center_of_mass(np.mean(CBED_in, axis=(0,1)) )   
#    xyzero[0] = nypix/2
#    xyzero[1] = nxpix/2
    
    for y in range(nysamp):
        for x in range(nxsamp):
            xycbed = ndimage.measurements.center_of_mass(CBED_in[y,x,:,:])
            com_x[y,x] = (xycbed[1]-xyzero[1])*duin
            com_y[y,x] = (xycbed[0]-xyzero[0])*dvin
            com_mag[y,x] = math.sqrt(com_y[y,x]*com_y[y,x]+com_x[y,x]*com_x[y,x])  
            
    angle = np.arctan2(com_y,com_x)  
    
    return com_y, com_x, angle, com_mag



def virtual_annular(r1,r2,data4Din):
    d1,d2,d3,d4 = data4Din.shape
    virtualimg = np.zeros((d1,d2))

    mask = np.zeros_like(data4Din[0,0])
    c1,c2 = int(data4Din[0,0].shape[0]/2), int(data4Din[0,0].shape[1]/2)
    rr1,cc1 = draw.disk((c1,c2),r1,shape = data4Din[0,0].shape)
    rr2,cc2 = draw.disk((c1,c2),r2,shape = data4Din[0,0].shape)
    mask[rr2,cc2] = 1
    mask[rr1,cc1] = 0

    for ii in range(virtualimg.shape[0]):
    for jj in range(virtualimg.shape[1]):
      virtualimg[ii,jj] = np.sum(mask*data4Din[ii,jj])

    return virtualimg, mask
  
def plotStrain(strain, **kwargs):
    figuresize  = kwargs.get("figsize", (18,7))
    scalebar    = kwargs.get("scalebar", True)

    plt.figure(figsize=figuresize)
    gs = gridspec.GridSpec(2,6, width_ratios = [1,1,1,0.075,1,0.075])
    aximg = plt.subplot(gs[0:2,0:2])
    ax00,cax00,ax01,cax01 = plt.subplot(gs[0,2]), plt.subplot(gs[0,3]), plt.subplot(gs[0,4]), plt.subplot(gs[0,5])
    ax10,cax10,ax11,cax11 = plt.subplot(gs[1,2]), plt.subplot(gs[1,3]), plt.subplot(gs[1,4]), plt.subplot(gs[1,5])

    img,scale = NBEDimage[k], NBEDimscale[k]
    aximg.imshow(img, cmap = 'gray')

    d1,d2 = img.shape
    origin = (0.03*d1, 0.9*d2)
    FOV = scale*d1
    barlength = d1/4
    length = barlength*scale
    height = barlength/10
    if scalebar:
        aximg.add_patch(patches.Rectangle((origin),barlength, height, color = 'w', ec='k'))
        tx,ty = origin[0]+barlength/2, origin[1]-height*0.5
        aximg.annotate("{} nm".format(length), (tx,ty), ha = 'center', fontsize = 20, color = 'k', weight = 'bold')

    im00 = ax00.imshow(strain[0], cmap = 'RdBu')
    im01 = ax01.imshow(strain[1], cmap = 'RdBu')
    im10 = ax10.imshow(strain[2], cmap = 'RdBu')
    im11 = ax11.imshow(strain[3], cmap = 'RdBu')

    cbar00 = plt.colorbar(im00, ax=cax00, aspect = 10, fraction = 3, format="%.2f")
    cbar01 = plt.colorbar(im01, ax=cax01, aspect = 10, fraction = 3, format="%.2f")
    cbar10 = plt.colorbar(im10, ax=cax10, aspect = 10, fraction = 3, format="%.2f")
    cbar11 = plt.colorbar(im11, ax=cax11, aspect = 10, fraction = 3, format="%.2f")

    cbar00.ax.tick_params(labelsize = 15, width = 3, length = 5)
    cbar01.ax.tick_params(labelsize = 15, width = 3, length = 5)
    cbar10.ax.tick_params(labelsize = 15, width = 3, length = 5)
    cbar11.ax.tick_params(labelsize = 15, width = 3, length = 5)

    ax00.set_title("e$_{xx}$ strain")
    ax01.set_title("e$_{xy}$ strain")
    ax10.set_title(r"e$_\theta$ strain")
    ax11.set_title("e$_{yy}$ strain")
    axes = [aximg, ax00, ax01, ax10, ax11, cax00, cax01, cax10, cax11]
    for ax in axes:
        ax.axis('off')

def plotDPC(**kwargs):
    figuresize  = kwargs.get("figsize", (18,7))
    scalebar    = kwargs.get("scalebar", True)

    fig = plt.figure(figsize = figuresize)
    gs = gridspec.GridSpec(2,5)
    ax1 = plt.subplot(gs[0:2, 0:2])
    ax12,ax13,ax14 = plt.subplot(gs[0,2]), plt.subplot(gs[0,3]), plt.subplot(gs[0,4])
    ax22,ax23,ax24 = plt.subplot(gs[1,2]), plt.subplot(gs[1,3]), plt.subplot(gs[1,4])

    ax1.imshow(img, cmap = 'gray')
    d1,d2 = img.shape
    origin = (0.03*d1, 0.9*d2)
    FOV = scale*d1
    barlength = d1/4
    length = barlength*scale
    height = barlength/10

    if scalebar:
        ax1.add_patch(patches.Rectangle((origin),barlength, height, color = 'w', ec='k'))
        tx,ty = origin[0]+barlength/2, origin[1]-height*0.5
        ax1.annotate("{} nm".format(length), (tx,ty), ha = 'center', fontsize = 20, color = 'k', weight = 'bold')

    ax12.imshow(com_x, cmap = 'magma')
    ax13.imshow(com_y, cmap = 'magma')
    ax14.imshow(angle, cmap = 'RdBu')

    ax22.imshow(com_mag, cmap = 'magma')
    ax23.imshow(charge_rel, cmap = 'RdBu')
    ax24.imshow(phase, cmap = 'RdBu')

    ax12.set_title("CoM x")
    ax13.set_title("CoM y")
    ax14.set_title("CoM angle")
    ax22.set_title("CoM magnitude")
    ax23.set_title("relative charge")
    ax24.set_title("relative potential")

    axes = [ax1,ax12,ax13,ax14,ax22,ax23,ax24]
    for ax in axes:
        ax.axis('off')