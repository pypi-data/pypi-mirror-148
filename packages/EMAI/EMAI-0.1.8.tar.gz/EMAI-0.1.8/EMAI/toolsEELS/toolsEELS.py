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




def CalibrateSI2(EAx,SI,num_spectral_px):
    m,M = np.amax(np.amin(EAx)), np.amin(np.amax(EAx))
    try:
      Eout=np.linspace(m,M,num_spectral_px)[1:]
      Eout=np.linspace(m,M,num_spectral_px,endpoint=True)
    except ValueError:
      Eout=np.linspace(m,M,5000)[1:]
      Eout=np.linspace(m,M,5000,endpoint=True)
    SIout=np.array([[interpolate.interp1d(e,s)(Eout) for e,s in zip(erow,srow)] for erow,srow in zip(EAx,SI)])
    return Eout,SIout

def CalibrateEnergyAxis2(SInc, EAx):
  '''
  For coreloss signals we don't have a "known" peak to reference (like the ZLP)
  Therefore, each (x,y) pixel will have the same energy axis as one another.
  Here we just create an array with the same shape as input SI, where every row/column
  has the same energy axis.
  '''

  EnergyAxes = np.zeros((SInc.shape[0], SInc.shape[1], EAx.shape[0]))
  for row in range(EnergyAxes.shape[0]):
    for col in range(EnergyAxes.shape[1]):
        EnergyAxes[row,col] = EAx
  return EnergyAxes

def organize_data2(filename, num_spectral_px, plot = False):
  SIraw, XY, disp, SIraw_flat, EAx = OrganizeInput2(filename) 
  SInc = CorrectNeg(SIraw, Blur = 20, Neg = -20, Pixrange = 200, plot=plot)
  EnergyAxes=CalibrateEnergyAxis2(SInc,EAx)
  E,SI=CalibrateSI2(EnergyAxes,SInc, num_spectral_px)                # calibrate energies by making all pixels start and end at same energy values
  SIflat=SI.reshape((np.prod(XY),SI.shape[2]))  

  return E, SI, XY, SIflat

def FitPowerlaw(E,S,fst,fen, plot = True):

    ist=np.argmin(np.abs(E-fst));ien=np.argmin(np.abs(E-fen))
    #e,s=np.append(E[is1:ie1],E[is2:ie2]),np.append(S[is1:ie1],S[is2:ie2])
    if plot == True:
      fig=plt.figure(figsize=(20,3))
      ax=fig.add_subplot(131)
      plt.plot(E,S,color='k',label='Data')
      # plt.plot(E[ist:ien],S[ist:ien],marker='o',ms=7,markerfacecolor='none',markeredgecolor='r',lw=0,label='Fit Region')
      plt.axvspan(E[ist],E[ien], color = 'r', alpha = 0.6, label = 'Fit Region')
      plt.legend(frameon=False,fontsize=13)
    else:
      pass
    fite=np.linspace(E[ist+1],E[ien-1],1000)
    f=interpolate.interp1d(E[ist:ien],S[ist:ien],kind='linear')
    elog=np.log(E[ist:ien][np.where(S[ist:ien]>0)])
    slog=np.log(S[ist:ien][np.where(S[ist:ien]>0)])
    # plt.ylim(0,0.002)
    r,A0=np.polyfit(elog,slog,1)

    if plot == True:
      ax=fig.add_subplot(132)
      plt.plot(E[ist:],S[ist:],color='k',label='Data')
      plt.plot(E[ist:],np.exp(A0)*E[ist:]**(r),'b',lw=3,label='Power Law Fit')
      plt.tick_params(labelsize=16)
      plt.legend(frameon=False,fontsize=13)
    else:
      pass
    
    if plot == True:
      ax=fig.add_subplot(133)
      
      plt.axhline(0,color='k')
      plt.plot(E[ist:],S[ist:]-np.exp(A0)*E[ist:]**(r),color='b',label='Powerlaw Subtraction')
      plt.tick_params(labelsize=16)
      ax.set_xlabel(r'Energy Loss ($eV$)',fontsize=16)
      plt.subplots_adjust(top=1,bottom=0.06,right=1,left=0.15)
      plt.legend(frameon=False,fontsize=10,labelspacing=0.3,handlelength=1,handletextpad=0.2)
    else:
      pass
    # plt.ylim(-0.0001,0.001)
    # return fite,0.#,f(fite)-np.exp(a*fite**3+b*fite**2+c*fite+d)
    return E[ist:],S[ist:]-np.exp(A0)*E[ist:]**(r)
    # return S[ist:]-np.exp(A0)*E[ist:]**(r)

def FitPowerlaw2R(E,S,fs1,fe1,fs2,fe2, plot = True):
    is1=np.argmin(np.abs(E-fs1));ie1=np.argmin(np.abs(E-fe1))
    is2=np.argmin(np.abs(E-fs2));ie2=np.argmin(np.abs(E-fe2))
    e,s=np.append(E[is1:ie1],E[is2:ie2]),np.append(S[is1:ie1],S[is2:ie2])

    if plot:
      fig=plt.figure(figsize=(20,3))
      
      ax=fig.add_subplot(131)
      
      plt.plot(E*1000,S,color='k',label='Data')
      plt.axvspan(E[ist],E[ien], color = 'r', alpha = 0.6, label = 'Fit Region')
      # plt.plot(e*1000,s,marker='o',ms=7,markerfacecolor='none',markeredgecolor='r',lw=0,label='Fit Region')
      plt.legend(frameon=False,fontsize=13)
    else:
      pass
    fite=np.linspace(E[is1+1],E[ie2-1],300)
    f=interpolate.interp1d(E[is1:ie2],S[is1:ie2],kind='linear')
    nozeros=s[np.where(s>0)]
    nozeroe=e[np.where(s>0)]
    elog=np.log(nozeroe)
    slog=np.log(nozeros)
    plt.ylim(0,0.02)
    r,A0=np.polyfit(elog,slog,1)
    
    if plot:
      ax=fig.add_subplot(132)
      
      plt.plot(E[is1:]*1000,S[is1:],color='k',label='Data')
      plt.plot(E[is1:]*1000,np.exp(A0)*E[is1:]**(r),'b',label='Power Law Fit')
      plt.tick_params(labelsize=16)
      plt.legend(frameon=False,fontsize=13)
    
      ax=fig.add_subplot(133)
      
    # plt.plot(fite,f(fite)-np.exp(a*fite**3+b*fite**2+c*fite+d),color='r',label='Exponential Subtraction')
      plt.plot(E[is1:],S[is1:]-np.exp(A0)*E[is1:]**(r),color='b',label='Powerlaw Subtraction')
      plt.tick_params(labelsize=16)
      ax.set_xlabel(r'Energy Loss ($eV$)',fontsize=16)
      plt.subplots_adjust(top=1,bottom=0.06,right=1,left=0.15)
      plt.axhline(0,color='k')
      plt.legend(frameon=False,fontsize=10,labelspacing=0.3,handlelength=1,handletextpad=0.2)
    else:
      pass
      # plt.ylim(-0.0001,0.001)
    
    return E[is1:],S[is1:]-np.exp(A0)*E[is1:]**(r)

def FitPowerlaw_v2(E,S,fst,fen):
    ist=np.argmin(np.abs(E-fst));ien=np.argmin(np.abs(E-fen))
    #e,s=np.append(E[is1:ie1],E[is2:ie2]),np.append(S[is1:ie1],S[is2:ie2])
    fig=plt.figure(figsize=(20,3))
    
    ax=fig.add_subplot(131)
    
    plt.plot(E,S,color='k',label='Data')
    plt.plot(E[ist:ien],S[ist:ien],marker='o',ms=7,markerfacecolor='none',markeredgecolor='r',lw=0,label='Fit Region')
    plt.legend(frameon=False,fontsize=13)
    fite=np.linspace(E[ist+1],E[ien-1],1000)
    f=interpolate.interp1d(E[ist:ien],S[ist:ien],kind='linear')
    elog=np.log(E[ist:ien][np.where(S[ist:ien]>0)])
    slog=np.log(S[ist:ien][np.where(S[ist:ien]>0)])
    # plt.ylim(0,0.002)
    r,A0=np.polyfit(elog,slog,1)
    
    ax=fig.add_subplot(132)
    
    plt.plot(E[ist:],S[ist:],color='k',label='Data')
    plt.plot(E[ist:],np.exp(A0)*E[ist:]**(r),'b',lw=3,label='Power Law Fit')
    plt.tick_params(labelsize=16)
    plt.legend(frameon=False,fontsize=13)
    
    ax=fig.add_subplot(133)
    
    plt.axhline(0,color='k')
    plt.plot(E[ist:],S[ist:]-np.exp(A0)*E[ist:]**(r),color='b',label='Powerlaw Subtraction')
    plt.tick_params(labelsize=16)
    ax.set_xlabel(r'Energy Loss ($eV$)',fontsize=16)
    plt.subplots_adjust(top=1,bottom=0.06,right=1,left=0.15)
    plt.legend(frameon=False,fontsize=10,labelspacing=0.3,handlelength=1,handletextpad=0.2)
    # plt.ylim(-0.0001,0.001)
    fit_spec = np.exp(A0)*E[ist:]**(r)
    # return fite,0.#,f(fite)-np.exp(a*fite**3+b*fite**2+c*fite+d)
    return fit_spec


def BlurSpectra_single(SIraw, sigma = 10):
    SIraw_blur_single = ndimage.filters.gaussian_filter(SIraw, sigma = sigma)
    return SIraw_blur_single

def BlurSpectra(SIraw, sigma = 10):
    SIraw_blur = np.zeros((SIraw.shape[0],SIraw.shape[1],SIraw.shape[2]))
    for i in range(SIraw.shape[0]):
        for j in range(SIraw.shape[1]):
            SIraw_blur[i,j] = ndimage.filters.gaussian_filter(SIraw[i,j,:], sigma = sigma)
    return SIraw_blur

def BlurSpectra_flat(SI, sigma = 10):
    SI_blur = np.zeros_like(SI)
    for ii in range(SI_blur.shape[0]):
        SI_blur[ii] = ndimage.filters.gaussian_filter(SI[i,:], sigma = sigma)
    return SI_blur

def CorrectNeg(SIraw, Blur = 10, Neg = -20, Pixrange = 250, plot = True):
    """
    Args:
       SI = Accepts any 3-dim SI as the operated-on SI, normally raw
       Blur =   gaussian blur sigma value. Should be set 10-30
                range to avoid false peaks due to noise
       Neg =    value which is considered to be negative. 
                Generally shouldn't be set to exactly 0 (or very close,
                like -1), due to noise effects
                **this also prevents spectra which are not negative at
                all from being artificially offset**
       Pixrange = number of pixels to average (centered around most 
                negative pixel located after blurring) over for sub-
                tracting from raw data
    Returns:
       - Original SI with offset
       - Blurred SI with offset
       - Plot of original + blurred offset 
    """  
    # blurs each pixels' spectrum
    SIraw_blur = np.zeros((SIraw.shape[0],SIraw.shape[1],SIraw.shape[2]))
    for i in range(SIraw.shape[0]):
        for j in range(SIraw.shape[1]):
            SIraw_blur[i,j] = ndimage.filters.gaussian_filter(SIraw[i,j,:], sigma = Blur)
    
    # local min peak search:
    # performs scipy findpeaks function (inverts signal to find MIN), then picks out most negative
    # again, should be OK due to the blurring previously
    # Derp, I think this could've been done much easier with np.min() and np.argmin()...
    # Actually maybe not, because I set a height parameter with findpeaks.
    
    MN = np.zeros((SIraw.shape[0],SIraw.shape[1]))
    posmaxpixel = np.zeros((SIraw.shape[0],SIraw.shape[1]))     
    for i in range(SIraw_blur.shape[0]):
        for j in range(SIraw_blur.shape[1]):
            if np.amax(SIraw[i,j])<5000:
                MN[i,j] = np.nan
            else:
                posmaxpixel[i,j]= np.argmax(SIraw_blur[i,j,:])
        
                peaks,props = signal.find_peaks(-1*SIraw_blur[i,j,int(posmaxpixel[i,j]):],height = -20)
                keys = peaks.tolist()
                values = props['peak_heights'].tolist()
                peakdict = dict(zip(keys, values))     
                sorted_peakdict = sorted(peakdict.items(), key=operator.itemgetter(1))
                mostneg = np.array(sorted_peakdict[-1:])
                mostnegT = mostneg.T
                try:
                    MN[i,j] = posmaxpixel[i,j]+mostnegT[0][0] # this is the most negative pixel, value that we need   
                except IndexError:
                    MN[i,j] = np.nan # if sample TOO THICK, spectrum is noise, so will produce index error; 
                                     # this just gives that the bird by setting to NaN.

      
            
    SInc =  np.zeros_like(SIraw)      
    SInegmean = np.zeros((SIraw.shape[0],SIraw.shape[1]))        
    for i in range(SIraw_blur.shape[0]):
         for j in range(SIraw_blur.shape[1]):
            if np.isnan(MN[i,j]) == True:     # handling if sample too thick
                SInc[i,j] = SIraw[i,j]
            elif np.isnan(MN[i,j]) == False:
                SInegmean[i,j] = np.mean(SIraw_blur[i,j,int(MN[i,j]-Pixrange/2):int(MN[i,j]+Pixrange/2)])
                SInc[i,j] = SIraw[i,j] - SInegmean[i,j]
            
                
            
    # for plotting (finding scatter XY coordinates)
    if plot == True:

      x_pos, y_pos = np.zeros_like(MN), np.zeros_like(MN)
      for i in range(SIraw_blur.shape[0]):
          for j in range(SIraw_blur.shape[1]):
              if np.isnan(MN[i,j]) == True:
                  x_pos[i,j] = 0
                  y_pos[i,j] = 0
              else:
                  x_pos[i,j] = int(MN[i,j])
                  y_pos[i,j] = SIraw_blur[i,j,int(x_pos[i,j])]
      
      i,j = np.random.randint(SIraw.shape[0]), np.random.randint(SIraw.shape[1])
                                                                            
      fig = plt.figure(figsize=(16,4))
      gs = gridspec.GridSpec(1,2)
      ax1 = plt.subplot(gs[0,0])
      ax2 = plt.subplot(gs[0,1])
      
      ax1.plot(SIraw_blur[i,j,:])
      ax1.plot(SIraw[i,j], alpha = 0.5)
      ax1.set_ylim(-100,1000)
      ax1.axhline(0,color='k',ls='--',lw=1.5)
      
      if x_pos[i,j] == 0:
          ax1.annotate('No offset performed: \nCould not find negative enough value', xy = (0.5,0.7), xycoords = 'axes fraction')
      else:
          ax1.scatter(x_pos[i,j], y_pos[i,j], color = 'r')
          patch1 = patches.Rectangle((x_pos[i,j]-Pixrange/2, y_pos[i,j]-30), Pixrange, 60, linewidth = 1, edgecolor = 'red', facecolor = 'red', fill = False)
          ax1.add_patch(patch1)
      
      
      ax2.plot(SInc[i,j])
      ax2.set_ylim(-100,1000)
      ax2.axhline(0,color='k',ls='--',lw=1.5);
    
    # r'$\bf{fixed \ data}$
    
      ax1.set_title(r'$\bf{XY} = $' + r'$\bf[{},{}]$: Raw SI, blurred SI, region of averaging'.format(i,j))
      ax2.set_title(r'$\bf{XY} = $' + r'$\bf[{},{}]$: Corrected SI'.format(i,j))
    
    else:
      pass
    
    return SInc


def CalibrateEnergyAxis(SI,disp,style='fwhm',subfitwidth=8):
    Einit=np.arange(0,SI.shape[2])*disp
    if style=='pixel': ZLPC=np.array([[Einit[np.argmax(s)] for s in row] for row in SI])
    if style=='fwhm':
        lh,uh=[],[]
        avspec=np.average(SI,axis=(0,1))
        for row in SI:
            lh.append([]);uh.append([])
            for s in row:
                if np.amax(s)<1000: # This line is for thick samples when ZLP drops to noise levels
                    s=avspec
                lh[-1].append(Einit[np.argmin(np.abs(s[:np.argmax(s)]/np.amax(s)-0.5))])
                uh[-1].append(Einit[np.argmin(np.abs(s[np.argmax(s):]/np.amax(s)-0.5))+np.argmax(s)])
        lh=np.asarray(lh)        
        uh=np.asarray(uh)
        ZLPC=np.average([uh,lh],axis=0)
    if style=='subpixel':
        def gauss(x,a,x0,s): return a*np.exp(-(x-x0)**2/s**2)
        from scipy.optimize import curve_fit
        ZLPC=np.array([[curve_fit(gauss,Einit[np.argmax(s)-W:np.argmax(s)+W],
                               s[np.argmax(s)-W:np.argmax(s)+W]/np.amax(s))[0][1] for s in row] for row in SI])
    return np.array([[Einit-c for c in row] for row in ZLPC])
    
def CalibrateSI(EAx,SI,num_spectral_px):
    m,M = np.amax(np.amin(EAx,axis=(2))), np.amin(np.amax(EAx,axis=(2)))
    try:
      Eout=np.linspace(m,M,num_spectral_px)[1:]
      Eout=np.linspace(m,M,num_spectral_px,endpoint=True)
    except ValueError:
      Eout=np.linspace(m,M,5000)[1:]
      Eout=np.linspace(m,M,5000,endpoint=True)
    SIout=np.array([[interpolate.interp1d(e,s)(Eout) for e,s in zip(erow,srow)] for erow,srow in zip(EAx,SI)])
    return Eout,SIout


## background subtraction using either 1 region or 2 regions:

def RemoveBackgroundSI(E,S,fst,fen):
    ist=np.argmin(np.abs(E-fst));ien=np.argmin(np.abs(E-fen))
    f=interpolate.interp1d(E[ist:ien],S[ist:ien],kind='linear')
    elog=np.log(E[ist:ien][np.where(S[ist:ien]>0)])
    slog=np.log(S[ist:ien][np.where(S[ist:ien]>0)])
    if len(np.where(S[ist:ien]>0)[0]) == 0.: 
        plt.plot(E[ist:],S[ist:])
        return E[ist:],np.zeros(E[ist:].shape)
    r,A0=np.polyfit(elog,slog,1)
    return E[ist:],S[ist:]-np.exp(A0)*E[ist:]**(r),

def RemoveBackgroundSI_THICK(E,S,fst,fen, threshold = 5000):
    ist=np.argmin(np.abs(E-fst));ien=np.argmin(np.abs(E-fen))
    f=interpolate.interp1d(E[ist:ien],S[ist:ien],kind='linear')
    elog=np.log(E[ist:ien][np.where(S[ist:ien]>0)])
    slog=np.log(S[ist:ien][np.where(S[ist:ien]>0)])
    if len(np.where(S[ist:ien]>0)[0]) == 0.: 
        plt.plot(E[ist:],S[ist:])
        return E[ist:],np.zeros(E[ist:].shape)
    if np.max(S) > threshold:
      r,A0=np.polyfit(elog,slog,1)
      return E[ist:],S[ist:]-np.exp(A0)*E[ist:]**(r),
    else:
      print("Too thick sir or ma'am")
      return E[ist:],S[ist:]
  
def RemoveBackgroundSI2R(E,S,fs1,fe1,fs2,fe2):
    is1=np.argmin(np.abs(E-fs1));ie1=np.argmin(np.abs(E-fe1))
    is2=np.argmin(np.abs(E-fs2));ie2=np.argmin(np.abs(E-fe2))
    e,s=np.append(E[is1:ie1],E[is2:ie2]),np.append(S[is1:ie1],S[is2:ie2])
    elog=np.log(e[np.where(s>0)])
    slog=np.log(s[np.where(s>0)])
    r,A0=np.polyfit(elog,slog,1)
    return E[is1:],S[is1:]-np.exp(A0)*E[is1:]**(r)

def RemoveBackgroundSI2R_THICK(E,S,fs1,fe1,fs2,fe2, threshold = 5000):
    is1=np.argmin(np.abs(E-fs1));ie1=np.argmin(np.abs(E-fe1))
    is2=np.argmin(np.abs(E-fs2));ie2=np.argmin(np.abs(E-fe2))
    e,s=np.append(E[is1:ie1],E[is2:ie2]),np.append(S[is1:ie1],S[is2:ie2])
    if np.max(S)>threshold:
      elog=np.log(e[np.where(s>0)])
      slog=np.log(s[np.where(s>0)])
      r,A0=np.polyfit(elog,slog,1)
      return E[is1:],S[is1:]-np.exp(A0)*E[is1:]**(r)
    else:
      print('too thick? Consider adjusting threshold')
      return E[is1:], S[is1:]

def FitPowerlaw_THICK(E,S,fst,fen, threshold = 5000):
    ist=np.argmin(np.abs(E-fst));ien=np.argmin(np.abs(E-fen))
    #e,s=np.append(E[is1:ie1],E[is2:ie2]),np.append(S[is1:ie1],S[is2:ie2])

    if np.max(S) > threshold:
      fig=plt.figure(figsize=(20,3))
      
      ax=fig.add_subplot(131)
      
      plt.plot(E,S,color='k',label='Data')
      plt.plot(E[ist:ien],S[ist:ien],marker='o',ms=7,markerfacecolor='none',markeredgecolor='r',lw=0,label='Fit Region')
      plt.legend(frameon=False,fontsize=13)
      fite=np.linspace(E[ist+1],E[ien-1],1000)
      f=interpolate.interp1d(E[ist:ien],S[ist:ien],kind='linear')
      elog=np.log(E[ist:ien][np.where(S[ist:ien]>0)])
      slog=np.log(S[ist:ien][np.where(S[ist:ien]>0)])
      # plt.ylim(0,0.002)
      r,A0=np.polyfit(elog,slog,1)
      
      ax=fig.add_subplot(132)
      
      plt.plot(E[ist:],S[ist:],color='k',label='Data')
      plt.plot(E[ist:],np.exp(A0)*E[ist:]**(r),'b',lw=3,label='Power Law Fit')
      plt.tick_params(labelsize=16)
      plt.legend(frameon=False,fontsize=13)
      
      ax=fig.add_subplot(133)
      
      plt.axhline(0,color='k')
      plt.plot(E[ist:],S[ist:]-np.exp(A0)*E[ist:]**(r),color='b',label='Powerlaw Subtraction')
      plt.tick_params(labelsize=16)
      ax.set_xlabel(r'Energy Loss ($eV$)',fontsize=16)
      plt.subplots_adjust(top=1,bottom=0.06,right=1,left=0.15)
      plt.legend(frameon=False,fontsize=10,labelspacing=0.3,handlelength=1,handletextpad=0.2)
      # plt.ylim(-0.0001,0.001)

      return E[ist:],S[ist:]-np.exp(A0)*E[ist:]**(r)

    else: # if max signal is <5000 counts, too thick for fitting
      S = S # Then don't perform any fitting, leave pixel as-is
      fig=plt.figure(figsize=(8,5))
      ax=fig.add_subplot(131)
      plt.plot(E*1000,S,color='k',label='Data')
      plt.title("Too thick for fitting")

      return E[ist:],S[ist:]

def FitPowerlaw2R_THICK(E,S,fs1,fe1,fs2,fe2, threshold = 5000, plot = True):
    is1=np.argmin(np.abs(E-fs1));ie1=np.argmin(np.abs(E-fe1))
    is2=np.argmin(np.abs(E-fs2));ie2=np.argmin(np.abs(E-fe2))
    
    if np.max(S) > threshold: 
      S = S/np.amax(S)
      e,s=np.append(E[is1:ie1],E[is2:ie2]),np.append(S[is1:ie1],S[is2:ie2])
      if plot:

        fig=plt.figure(figsize=(20,3))
        ax=fig.add_subplot(131)
        
        plt.plot(E,S,color='k',label='Data')
        plt.axvspan(E[is1],E[ie1], color = 'r', alpha = 0.6, label = 'Fit Region 1')
        plt.axvspan(E[is2],E[ie2], color = 'b', alpha = 0.6, label = 'Fit Region 2')
        # plt.plot(e*1000,s,marker='o',ms=7,markerfacecolor='none',markeredgecolor='r',lw=0,label='Fit Region')
        plt.legend(frameon=False,fontsize=13)
      else:
        pass
      fite=np.linspace(E[is1+1],E[ie2-1],300)
      f=interpolate.interp1d(E[is1:ie2],S[is1:ie2],kind='linear')
      nozeros=s[np.where(s>0)]
      nozeroe=e[np.where(s>0)]
      elog=np.log(nozeroe)
      slog=np.log(nozeros)
      # plt.ylim(0,0.02)
      r,A0=np.polyfit(elog,slog,1)
      
      if plot:
        ax=fig.add_subplot(132)
        
        plt.plot(E[is1:],S[is1:],color='k',label='Data')
        plt.plot(E[is1:],np.exp(A0)*E[is1:]**(r),'b',label='Power Law Fit')
        plt.tick_params(labelsize=16)
        plt.legend(frameon=False,fontsize=13)
        
        ax=fig.add_subplot(133)
        
      # plt.plot(fite,f(fite)-np.exp(a*fite**3+b*fite**2+c*fite+d),color='r',label='Exponential Subtraction')
        plt.plot(E[is1:],S[is1:]-np.exp(A0)*E[is1:]**(r),color='b',label='Powerlaw Subtraction')
        plt.tick_params(labelsize=16)
        ax.set_xlabel(r'Energy Loss ($eV$)',fontsize=16)
        plt.subplots_adjust(top=1,bottom=0.06,right=1,left=0.15)
        plt.axhline(0,color='k')
        plt.legend(frameon=False,fontsize=10,labelspacing=0.3,handlelength=1,handletextpad=0.2)
      
      # plt.ylim(-0.001,0.001)

      return E[is1:],S[is1:]-np.exp(A0)*E[is1:]**(r)

    else: # if max signal is <5000 counts, too thick for fitting
      S = S # Then don't perform any fitting, leave pixel as-is
      fig=plt.figure(figsize=(20,3))
      ax=fig.add_subplot(131)
      plt.plot(E*1000,S,color='k',label='Data')
      plt.title("Too thick for fitting")

      return E[is1:],S[is1:]  # Still return with the truncated energy and spectra, to align with the rest

def plot_spectrum(eaxis, spectrum, axisname, color = 'dodgerblue'):
    axisname.plot(eaxis, spectrum, color = color, lw=3)
    axisname.set_xlabel("Energy loss (eV)", fontsize = 16, labelpad = 15, weight = 'bold')
    axisname.set_ylabel("Intensity (a.u.)", fontsize = 16, labelpad = 15, weight = 'bold')
    axisname.tick_params(labelsize = 16, length = 8, width = 2)

    for axis in ['top','bottom','left','right']:
        axisname.spines[axis].set_linewidth(3)
        axisname.axhline(0,c='k')
def force_SI_zero(specim, e1, e2):
  '''
  Offsets an entire spectrum image (for each (x,y) pixel individually),
  such that the range from e1 to e2 averages to zero.
  This must be used with care, and only when it is known 
  a spectral region **should** be zero
  '''
  new_SI = np.zeros_like(specim)
  for ii in range(specim.shape[0]):
    for jj in range(specim.shape[1]):
        spec = specim[ii,jj]
        offset = np.mean(spec[e1:e2])
        new_SI[ii,jj] = spec - offset
  return new_SI

  # Integrating the spectral regions...

def integrate_specim(specim, energy_axis, energy1, energy2, method = 'average'):
  e1,e2 = np.abs(energy1-energy_axis).argmin(), np.abs(energy2-energy_axis).argmin()
  
  if method == 'average':
    integrated = np.mean(specim[:,:,e1:e2],axis=2)
  elif method == 'sum':
    integrated = np.sum(specim[:,:,e1:e2])
  else:
    raise NameError("Method not recognized. Please use either 'average' or 'sum'")

  return integrated  
