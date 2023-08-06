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

def align_stack(stack, blur, style = "crop", **kwargs):
  '''
  Aligns a stack of 2D images by cross correlation between each subsequent frame
  In computing the cross correlation between two images, for periodic images,
  it helps to blur each of the images to pick up non-periodic features more easily.
  The final drift corrected image stack will have "dead" cols/rows where pixels are not aligned.
  This can be handled via the style option: Use "crop", "zero", or "none"
  '''
  plot = kwargs.get("plot", "True")
  drift_XY = np.zeros((len(stack), 2), dtype = int)

  ## Get the frame-to-frame drift:
  for ii in range(len(drift_XY)-1):
    if blur == None:
      drift_XY[ii+1] = cross_image(stack[ii], stack[ii+1])
    else:
      drift_XY[ii+1] = cross_image(ndimage.gaussian_filter(stack[ii], sigma = blur), ndimage.gaussian_filter(stack[ii+1], sigma = blur))

  # Add each previous frame's drift to the following frame:
  for ii in range(len(drift_XY)-1):
    drift_XY[ii+1] = drift_XY[ii] + drift_XY[ii+1]

  summed_images = np.zeros((stack.shape[0] - 1, stack.shape[1], stack.shape[2]))
  for ii in range(len(drift_XY)-1):
    summed_images[ii] = np.roll(stack[ii], drift_XY[ii], axis=(0,1)) + np.roll(stack[ii+1], drift_XY[ii], axis=(0,1))
  summed_image = normalize(np.sum(summed_images, axis=0))


  if style == "zero":
    if drift_XY[-1][1] >= 0:
        summed_image[:drift_XY[-1][1], :] = 0
    else:
        summed_image[drift_XY[-1][1]:, :] = 0
    if drift_XY[-1][0] >= 0:
        summed_image[:, :drift_XY[-1][0]] = 0
    else:
        summed_image[:, drift_XY[-1][0]:] = 0

  elif style == "crop":
    if drift_XY[-1][1] >= 0:
        summed_image = summed_image[drift_XY[-1][1]:, :]
    else:
        summed_image = summed_image[:drift_XY[-1][1], :]
    if drift_XY[-1][0] >= 0:
        summed_image = summed_image[:, drift_XY[-1][0]:]
    else:
        summed_image = summed_image[:, :drift_XY[-1][0]]

  elif style == "none":
    pass
  else:
    raise NotImplementedError('Please choose "crop", "zero", "none" as Style')

  if plot:
    plt.figure(figsize=(6,6))
    plt.imshow(summed_image)
    
  return summed_image, drift_XY

def cross_image(image1, image2):
	"""
	Determines the shift in pixels from image1 to image2.
	"""
	image1FFT = np.fft.fft2(image1)
	image2FFT = np.conjugate(np.fft.fft2(image2))
	imageCCor = np.real(np.fft.ifft2((image1FFT * image2FFT)))
	imageCCorShift = np.fft.fftshift(imageCCor)
	row, col = image1.shape
	yShift, xShift = np.unravel_index(np.argmax(imageCCorShift), (row, col))
	yShift -= int(row / 2)
	xShift -= int(col / 2)

	return yShift, xShift



def plot_image(image, imagescale, axisname, scalebar, bar_ratio = 0.15, bar_pos_xy = [0.83, 0.94], colormap = 'gray'):

  axisname.imshow(image, cmap = 'gray')
  plt.setp(axisname,xticks=[], yticks=[])

  length = scalebar / imagescale
  height = bar_ratio * length
  xx,yy = image.shape[0], image.shape[1]

  xfrac, yfrac = bar_pos_xy[0], bar_pos_xy[1]
  p1,p2 = xfrac*xx, yfrac*yy
  axisname.add_patch(patches.Rectangle((p1,p2), length, height, color = 'white', ec='k', lw=1, fill = True))



def get_polar_displacements(neighbors, max_shift = 2, min_shift = 0., fill_val = np.nan):
  '''
  Assumes neighbors is an (N x m x 3) matrix
  where N is number of central atoms,
  number of neighbors + 1, where the first (index 0) is the 
  position of the central atom, and remaining indices of m 
  are the positions of the neighbors
  this has 3 elements for x,y,class

  max_shift is the maximum euclidean distance the central atom
  is allowed to shift relative to its projected unit cell centroid
  - this primary protects against bad neighbor finding

  fill_val replaces the shifts_xy AND neighbor values with this for bad
  fits (i.e., if max_shift is exceeded, the neighbors and shifts are 
  all replaced with fill_val)
  '''
  shifts_xy = np.zeros((len(neighbors), 2))
  centroids = np.zeros_like(shifts_xy)

  for k in range(len(shifts_xy)):
    cx, cy = get_centroid(neighbors[k, 1:, :2])
    centroids[k,0] = cy
    centroids[k,1] = cx
    shifts_xy[k,0] = cy - neighbors[k,0,1]  # consider switching?
    shifts_xy[k,1] = cx - neighbors[k,0,0]

  neighbors_updated = dc(neighbors)
  bads = np.where(np.hypot(shifts_xy[:,0], shifts_xy[:,1]) > max_shift)
  smalls = np.where(np.hypot(shifts_xy[:,0], shifts_xy[:,1]) < min_shift)
  shifts_xy[bads] = fill_val        # set to nan, or ZERO? Deleting is .. hmm
  shifts_xy[smalls] = fill_val
  neighbors_updated[bads] = fill_val

  return shifts_xy, neighbors_updated, centroids

def get_centroid(coord_list):
  centroid = coord_list.mean(0)
  return centroid

def get_neighbors(all_coords, query_coords, num_neighbors = 4, upper_bound = None):
  # Construct a tree using ALL coordinates, but only query the A sites

  tree = spatial.cKDTree(all_coords[0][:, :2])
  d, nn = tree.query(query_coords, k=num_neighbors+1, distance_upper_bound=upper_bound)
  idx_to_del = np.where(d == np.inf)[0]
  nn = np.delete(nn, idx_to_del, axis=0)
  d = np.delete(d, idx_to_del, axis=0)

  return all_coords[0][nn]


# Something odd about this, so just using means from now on.
def centroid_poly(X, Y):
    """https://en.wikipedia.org/wiki/Centroid#Of_a_polygon"""
    N = len(X)
    # minimal sanity check
    if not (N == len(Y)): raise ValueError('X and Y must be same length.')
    elif N < 3: raise ValueError('At least 3 vertices must be passed.')
    sum_A, sum_Cx, sum_Cy = 0, 0, 0
    last_iteration = N-1
    # from 0 to N-1
    for i in range(N):
        if i != last_iteration:
            shoelace = X[i]*Y[i+1] - X[i+1]*Y[i]
            sum_A  += shoelace
            sum_Cx += (X[i] + X[i+1]) * shoelace
            sum_Cy += (Y[i] + Y[i+1]) * shoelace
        else:
            # N-1 case (last iteration): substitute i+1 -> 0
            shoelace = X[i]*Y[0] - X[0]*Y[i]
            sum_A  += shoelace
            sum_Cx += (X[i] + X[0]) * shoelace
            sum_Cy += (Y[i] + Y[0]) * shoelace
    A  = 0.5 * sum_A
    factor = 1 / (6*A)
    Cx = factor * sum_Cx
    Cy = factor * sum_Cy
    # returning abs of A is the only difference to
    # the algo from above link
    return Cx, Cy

def plot_all_images(imgs, imgscales, sblength_fraction = (1/8), sbheight_fraction = 0.15, posxy = (0.8,0.9), imperrow = 3, figsize_r = 8):

  num_im = len(imgs)
  rows = int(np.ceil(float(num_im)/imperrow))
  cols = int(np.ceil(float(num_im)/rows))

  gs = gridspec.GridSpec(rows, cols)
  fig = plt.figure(figsize = (figsize_r*cols, figsize_r*(1+rows)))   
  for kk in range(num_im):
      ax = fig.add_subplot(gs[kk])
      ax.imshow(imgs[kk], cmap = 'gray')
      ax.set_title("index: {}".format(kk), fontsize = 16)
      plt.setp([ax],xticks=[], yticks=[])

      length = sblength_fraction*imgs[kk].shape[0]
      height = sbheight_fraction*length
      scalebar = round(length * imgscales[kk],2)
      xx,yy = imgs[kk].shape[0], imgs[kk].shape[1]
      xfrac, yfrac = posxy[0], posxy[1]
      p1,p2 = xfrac*xx, yfrac*yy
      ax.add_patch(patches.Rectangle((p1,p2), length, height, color = 'white', ec='k', lw=1, fill = True))

      midpointx = int(p1+length/2)
      midpointy = int(p2-height/2)
      ax.annotate("{} nm".format(scalebar), (midpointx,midpointy), color = 'w', fontsize = figsize_r*2.5 ,ha = 'center')


def convert_fftpixel(fft_img, calibration, pixel_value):
  freq_axis = np.fft.fftshift(np.fft.fftfreq(fft_img.shape[1], calibration))
  distance = 1/freq_axis[int((freq_axis.shape[0]/2) + pixel_value)]
  return distance
  
def remove_close_points(points, min_distance = 2):
  tree = cKDTree(points)
  close = tree.query_pairs(r = min_distance, output_type = 'ndarray')
  points = np.delete(points, close[:,0], axis = 0)
  points = points.reshape(-1,2)
  return points

def take_FFT(img, zoom, power = 1, blur = 0, center_remove = 1, blur_subtract = 1, hamming=True):
  fftimg = np.log(
    np.abs(
        np.fft.fftshift(
            np.fft.fft2(img**power)
            )
        )
    )
  c1,c2 = int(fftimg.shape[0]/2), int(fftimg.shape[1]/2)
  if center_remove > 0:
    fftimg[int(c1-center_remove):int(c1+center_remove),
           int(c2-center_remove):int(c2+center_remove)] = 0
  Z = int(fftimg.shape[0]/zoom/2)
  fftimg = fftimg[int(c1-Z):int(c1+Z),
                  int(c2-Z):int(c2+Z)]
  if blur_subtract > 0:
    fftblur = ndimage.gaussian_filter(fftimg, sigma = blur_subtract)
    fftimg = fftimg - fftblur
  if hamming:
    fftimg = ApplyHamming(fftimg,fftimg.shape[0])
  fftimg = ndimage.gaussian_filter(fftimg, blur)
  fftimg = normalize(fftimg)

  return fftimg

def truncate_spectrum(ENB, cutoffenergy):
  truncate = (np.abs(ENB-cutoffenergy)).argmin()
  return truncate 

def normalize(image):
  return (image - np.min(image))/(np.ptp(image))

def MakeCompositeImage(ims,colors):
    """
    Adds and averages different maps to form a composite map
    
    Input:  ims    - list of images of same dimension (numpy array)
            colors - a list of colors in rgb format (triple of fractional values)
            labels - labels for the different images (tuple of strings)
    Output: out_im - Composite image (RGB image)
    """
    ims=np.asarray(ims)
    dims=ims.shape
    print(dims)
    out_im=np.zeros(dims[1:]+(3,))
    for i in range(dims[1]):
      for j in range(dims[2]):
        out_im[i,j]=np.sum([v*np.asarray(c) for v,c in zip(ims[:,i,j],colors)],axis=0)/np.sum(ims[:,i,j])
    return out_im


def ApplyHamming(imgsrc, winsize):
    #Applies a Hamming window to the input imgsec, returns the window after filter applied.
    bw2d = np.outer(np.hamming(winsize), np.ones(winsize))
    bw2d = np.sqrt(bw2d * bw2d.T) 
    imgsrc *= bw2d
    return imgsrc

def ADF_mask(nxpix,nypix,du,dv,rout,rin):
    ixcent = int(nxpix/2)
    iycent = int(nypix/2)
    mask = np.zeros((nypix,nxpix))
    for i in range(nypix):
        for j in range(nxpix):
            ry = abs(iycent-i)*dv
            rx = abs(ixcent-j)*du
            r2 =rx*rx+ry*ry
            if r2 <rout**2 and r2> rin**2:
                mask[i,j] = 1.0
    return mask

def SlidingFFT(image, winsize, stepsize, zoom, interpolate, ham = True):
  # Get coords for slicing
  x_positions = np.arange(0, image.shape[0] - winsize, stepsize)
  y_positions = np.arange(0, image.shape[0] - winsize, stepsize)
  x_pos = np.tile(x_positions, len(x_positions)).reshape(len(x_positions)**2,1)
  y_pos = np.repeat(y_positions, len(y_positions)).reshape(len(y_positions)**2,1)
  positions = np.concatenate((x_pos, y_pos),axis = 1)

  # Do slicing
  FFTstack = np.zeros((len(positions), int(winsize*upscale/zoom), int(winsize*upscale/zoom)))
  for ii in range(len(positions)):
    crop = image[int(positions[ii,0]) : int(positions[ii,0]+winsize),
                int(positions[ii,1]) : int(positions[ii,1]+winsize)]
    if ham == True:
      crop_clean = ApplyHamming(np.copy(crop),winsize)
    else:
      crop_clean = np.copy(crop)
    
    # FFT on each slice
    FFT_ = scipy.fft.fft2(crop_clean)
    FFT = np.abs(scipy.fft.fftshift(FFT_))

    # Zoom the FFT by cropping around center and upscaling the image
    zoom_in = winsize/2/zoom
    FFT_zoom_ = FFT[int(winsize/2 - zoom_in) : int(winsize/2 + zoom_in),
                    int(winsize/2 - zoom_in) : int(winsize/2 + zoom_in)]
    FFT_zoom = ndimage.zoom(FFT_zoom_, upscale)
    FFTstack[ii] = FFT_zoom

  # Reshape the image stack such that it coincides with 2 spatial dimensions (becomes a 2D image!)
  FFTdeconvolve = np.reshape(FFTstack, (
                            int(np.sqrt(FFTstack.shape[0])),
                            int(np.sqrt(FFTstack.shape[0])),
                            int(winsize*upscale/zoom),
                            int(winsize*upscale/zoom))
                            )
  return FFTdeconvolve