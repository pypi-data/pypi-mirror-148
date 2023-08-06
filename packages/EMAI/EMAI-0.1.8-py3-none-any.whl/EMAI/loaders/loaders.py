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



def OrganizeInput_TimeSpectra(self,numpy):
    TimeSpecRaw = np.load(numpy)
    TimeSpecj = json.load(open(numpy[:-3]+'json','r'))
    disp = TimeSpecj['spatial_calibrations'][1]['scale']
    E_offset = TimeSpecj['spatial_calibrations'][1]['offset']
    E = np.linspace(E_offset,TimeSpecRaw.shape[1]*disp+E_offset,TimeSpecRaw.shape[1])
    return TimeSpecRaw, disp, E

def organize_data(filename, num_spectral_px, plot = False):
  SIraw, XY, disp, SIraw_flat = OrganizeInput(filename) 
  SInc = CorrectNeg(SIraw, Blur = 20, Neg = -20, Pixrange = 200, plot = plot)
  SIncflat = SInc.reshape((np.prod(XY),SInc.shape[2]))
  EnergyAxes=CalibrateEnergyAxis(SInc,disp)                  # align ZLP & use dispersion to go from pixel -> eV
  Eaxflat=EnergyAxes.reshape((np.prod(XY),SInc.shape[2]))    # flatten
  E,SI=CalibrateSI(EnergyAxes,SInc, num_spectral_px)                # calibrate energies by making all pixels start and end at same energy values
  SIflat=SI.reshape((np.prod(XY),SI.shape[2]))  
  return E, SI, XY, SIflat

def OrganizeInput(numpy):
    SIraw = np.load(numpy)
    XY = SIraw.shape[:2]
    SIj = json.load(open(numpy[:-3]+'json','r'))
    disp = SIj['spatial_calibrations'][2]['scale']
    SIraw_flat=SIraw.reshape((np.prod(XY),SIraw.shape[2]))
    return SIraw, XY, disp, SIraw_flat
    

def OrganizeInput2(numpy):
    SIraw = np.load(numpy)
    XY = SIraw.shape[:2]
    SIj = json.load(open(numpy[:-3]+'json','r'))
    disp = SIj['spatial_calibrations'][2]['scale']
    SIraw_flat=SIraw.reshape((np.prod(XY),SIraw.shape[2]))
    E_offset = SIj['spatial_calibrations'][2]['offset']
    E = np.linspace(E_offset,SIraw.shape[2]*disp+E_offset,SIraw.shape[2])
    return SIraw, XY, disp, SIraw_flat, E


def LoadADF(filename):
    ADF1    = np.load(filename)
    ADF1j = json.load(open(filename[:-3]+'json','r'))
    ADF1_scale = ADF1j['spatial_calibrations'][0]['scale']
    return ADF1, ADF1_scale

def LoadMovie(filename):
    mov    = np.load(filename)
    movj = json.load(open(filename[:-3]+'json','r'))
    mov_scale = movj['spatial_calibrations'][1]['scale']
    return mov, mov_scale

def Load4D(filename):

  file4D = np.load(filename)
  json4D = json.load(open(filename[:-3]+'json','r'))
  mradpx = json4D['spatial_calibrations'][2]['scale']*1000

  return file4D, mradpx

def LoadCCD(filename, angle_correction = 1E3, return_metric = True):
    img = np.load(filename)
    img_j = json.load(open(filename[:-3]+'json','r'))
    try:
      defocus = img_j['metadata']['hardware_source']['autostem']['defocus_m']
    except KeyError:
      try:
        defocus = img_j['metadata']['instrument']['defocus']  # New MACSTEM location
      except KeyError:
        print('figure this json out...')
    mrad_scale = img_j['spatial_calibrations'][0]['scale']*angle_correction  # angle correction is just for whatever reason, swift has all angles in mrad off by 1000
    # deg_scale = mrad_scale*180/(1000*np.pi)
    metric_scale = defocus*np.tan(mrad_scale/1000)  # divide by 1000 to get to RADIANS now
    if return_metric:
      return img, metric_scale
    else:
      return img, mrad_scale
