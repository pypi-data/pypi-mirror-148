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


def get_atom_classes(coordinates, n_classes = 2):
  coord_dict = {}
  for ii in range(n_classes):
    coord_dict["{}".format(ii)] = np.empty((0,2))
  
  for kk,c in enumerate(coordinates[0]):
    c1,c2,c3 = c

    for NC in range(n_classes):
      if c3 == NC:
        coord_dict["{}".format(NC)] = np.append(coord_dict["{}".format(NC)], [c1,c2])

  for ii in range(n_classes):
      coord_dict["{}".format(ii)] = coord_dict["{}".format(ii)].reshape(-1,2)

  return coord_dict

def atom_classify(coord_dict_pred, imgdata, method="gmm_local", n_components=2, window_size=48, coord_class=0, thresh = 0.5):
  coordinates = aoi.stat.update_classes(coord_dict_pred, imgdata, method=method,
    n_components=n_components, window_size=window_size, coord_class=coord_class, thresh = thresh) # other methods: kmeans, meanshift, threshold
  return coordinates


def compute_NMF(specim, eax, N, plot = True):
  specimflat = np.reshape(specim, (specim.shape[0]*specim.shape[1],specim.shape[2]))
  SIdecon=np.copy(specimflat)
  SIdecon=np.copy(specimflat[:,:])
  SIdecon[np.where(SIdecon<0)]=0
  XY = specim.shape[0:2]

  model=NMF(n_components=N, random_state = 42)
  NMFIm=model.fit_transform(SIdecon[:,:])
  NMFSpec=model.components_
  NMFIm=NMFIm.reshape(XY+(N,)).transpose(2,0,1)

  if plot:
    rows = int(np.ceil(float(N)/3))
    cols = int(np.ceil(float(N)/rows))

    fig1,ax1 = plt.subplots(figsize = (10,4))

    for jj in range(N):
        try:
          ax1.plot(eax[:],NMFSpec[jj],color = colorlist[jj], label = jj+1)
        except IndexError:
          rollover = int(jj/len(colorlist))
          ax1.plot(eax[:],NMFSpec[jj],color = colorlist[int(jj - len(colorlist)*rollover)], label = jj+1)
        ax1.grid(True)
        ax1.tick_params(labelsize=10)
        ax1.legend()
    plt.show()
    gs2 = gridspec.GridSpec(rows, cols)
    fig2 = plt.figure(figsize = (5*cols, 4*(1+rows//2)))
    for jj in range(N):
        ax2 = fig2.add_subplot(gs2[jj])
        try:
          ax2.imshow(NMFIm[jj],cmap = Cmap_list[jj])
        except IndexError:
          rollover = int(jj/len(colorlist))
          ax2.imshow(NMFIm[jj],cmap = Cmap_list[int(jj - len(colorlist)*rollover)])
        ax2.set_title('Component ' + str(jj+1))
        plt.setp([ax2],xticks=[], yticks=[])
                 
  return NMFIm, NMFSpec

def ShowUnmixed(n_comp,Eaxis,Spec,Im,rowfactor=3,cmap = 'jet'):
  rows = int(np.ceil(float(n_comp)/rowfactor))
  cols = int(np.ceil(float(n_comp)/rows))

  fig1,ax1 = plt.subplots(figsize = (10,4))

  for i in range(n_comp):
      ax1.plot(Eaxis,Spec[i], label = i+1)
      ax1.grid(True)
      ax1.tick_params(labelsize=10)
      ax1.legend()
  plt.show()

  gs2 = gridspec.GridSpec(rows, cols)
  fig2 = plt.figure(figsize = (5*cols, 4*(1+rows//2)))

  for i in range(n_comp):
      ax2 = fig2.add_subplot(gs2[i])
      ax2.imshow(Im[i], cmap = cmap)
      ax2.set_title('Component ' + str(i+1))
      plt.setp([ax2],xticks=[], yticks=[])