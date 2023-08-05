#  CASA Next Generation Infrastructure
#  Copyright (C) 2021 AUI, Inc. Washington DC, USA
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from numba import jit, types
import numba
import numpy as np

@jit(numba.float64[::1](types.Array(types.float64, 2, 'A', readonly=True), numba.float64[::1], numba.float64[::1]), nopython=True,cache=True,nogil=True)
def _bilinear_interpolate(im, x, y):
    """Interpolates image values. 
    Inputs 
    -------------- 
    im: 2-d numpy array (complex?)
    x: 1-d numpy array of fractional indices (float)
    y: 1-d numpy array of fractional indices (float)
    Notes: x and y must be same length. Negative indices not allowed (automatically set to 0).
    -------------- 
    Outputs: 
    -------------- 
    1-d numpy array of interpolated values (float)"""
    
    #x0 rounds down, x1 rounds up. Likewise for y
    x0 = np.floor(x).astype(numba.intc)
    x1 = x0 + 1
    y0 = np.floor(y).astype(numba.intc)
    y1 = y0 + 1
    
    #Safety: makes sure no indices out of bounds
    x0 = np.minimum(im.shape[1]-1, np.maximum(x0, 0))
    x1 = np.minimum(im.shape[1]-1, np.maximum(x1, 0))
    y0 = np.minimum(im.shape[0]-1, np.maximum(y0, 0))
    y1 = np.minimum(im.shape[0]-1, np.maximum(y1, 0))
    
    #Four values around value to be interpolated
    Ia1 = im[y0]
    Ia = Ia1.flatten()[x0]
    Ib1 = im[y1]
    Ib = Ib1.flatten()[x0]
    Ic1 = im[y0]
    Ic = Ic1.flatten()[x1]
    Id1 = im[y1]
    Id = Id1.flatten()[x1]
    
    #See https://en.wikipedia.org/wiki/Bilinear_interpolation
    wa = (x1-x) * (y1-y)
    wb = (x1-x) * (y-y0)
    wc = (x-x0) * (y1-y)
    wd = (x-x0) * (y-y0)

    return wa*Ia + wb*Ib + wc*Ic + wd*Id


#@jit(types.Array(types.complex128, 2, 'A')(types.Array(types.complex128, 3, 'C'), types.Array(types.float64, 1, 'C'), types.Array(types.float64, 1, 'C'), types.float64, types.float64), nopython=True,cache=False,nogil=True)
#@jit(types.Array(types.complex128, 2)(types.Array(types.complex128, 3), types.Array(types.float64, 1), types.Array(types.float64, 1), types.float64, types.float64), nopython=True,cache=True,nogil=True)
@jit(types.Array(types.complex128, 2, 'A')(types.Array(types.complex128, 3, 'A'), types.Array(types.float64, 1, 'C'), types.Array(types.float64, 1, 'C'), types.float64, types.float64), nopython=True,cache=False,nogil=True)
def _interp_array(im_array, l, m, delta_l, delta_m):
    """Interpolates image values.
    Inputs 
    -------------- 
    im_array: 3-d numpy array of shape (pol, image, image)
    l: 1-d numpy array of fractional indices (float)
    m: 1-d numpy array of fractional indices (float)
    delta_l: pixel size for l coordinates (float)
    delta_m: pixel size for m coordinates (float)
    Notes: l and m must be same length.
    -------------- 
    Outputs: 
    -------------- 
    2-d numpy array of interpolated values (float) with shape (pol, len(l))"""
    
    #Length of image along l 
    n_l = len(im_array[0, :, 0]) #Change to shape?
    #Length of image along m
    n_m = len(im_array[0, 0, :]) 
    #Fractional pixel along l
    x_frac = (l/delta_l) + n_l//2 
    #Fractional pixel along m
    y_frac = (m/delta_m) + n_m//2 
    #Numba-style array creation. Shape is (polarization, coordinates)
    results = np.zeros((len(im_array), len(l)), dtype = numba.complex128) 
    for i in range(len(im_array)):
        #Complex interpolation
        results[i] = _bilinear_interpolate(im_array[i].real, x_frac, y_frac) +    1j*_bilinear_interpolate(im_array[i].imag, x_frac, y_frac)
    return results.astype(numba.complex128)


"""
@jit(nopython=True,cache=True,nogil=True)
def interp_ndim(ndim_array, x, y, dims = (0, 1)):
    Interpolates coordinates of an image defined by specified dimensions of an n-d array.
    Inputs:
    ndim_array: n-dimensional array
    dims: tuple of size 2 containing dimensions which comprise the image
    Outputs:
    Interpolated values
    #Gets the shape of the images which are to be interpolated
    shape = ndim_array.shape
    shape_image = np.zeros(2, dtype = int)
    for i in range(2):
        shape_image[i] = shape[dims[i]]
    
    #Gets the shape of the container of the images
    shape_image_array = np.delete(ndim_array.shape, dims)
    shape_image_tuple = (shape_image_array[0], )
    for i in range(1, len(shape_image_array)):
        shape_image_tuple = shape_image_tuple + (shape_image_array[i], )
    #print(shape_image_tuple)
    
    #Creates flattened container with images inside
    length_flat = 1
    for i in range(len(shape_image_array)):
        length_flat = length_flat*shape_image_array[i]
    flat_shape = np.zeros(1, dtype = int)
    flat_shape = (length_flat, shape_image[0], shape_image[1])
    f_image_array = ndim_array.reshape(flat_shape)
    
    #Creates container with results of interpolation as the innermost dimension
    results = np.zeros((len(f_image_array), len(x)), dtype = float)
    for i in range(len(f_image_array)):
        results[i] = _bilinear_interpolate(f_image_array[i], x, y)
    shape_results = shape_image_tuple + (len(x), )
    results = results.reshape(shape_results)
    return results
            
"""

@jit(numba.float64[:, :](numba.float64[:,:], numba.int64), nopython=True, cache=True, nogil=True)
def _powl2(base_arr, in_exp):
    #print(base,exp)
    #base can be any real and exp must be positive integer
    # base**exp
    """
    Algorithm taken from https://stackoverflow.com/questions/2198138/calculating-powers-e-g-211-quickly
    https://en.wikipedia.org/wiki/Exponentiation_by_squaring
    """
    #exp_int = np.zeros(base_arr.shape)
    exp_int = np.zeros(base_arr.shape,numba.f8)
    
    for i in range(base_arr.shape[0]):
        for j in range(base_arr.shape[1]):
            base = base_arr[i,j]
            
            exp = in_exp
            r = 0.0
            if exp == 0:
                r = 1.0
            else:
                if exp < 0 :
                    base = 1.0 / base
                    exp = -exp
                 
                y = 1.0;
                while exp > 1:
                    if (exp % 2) == 0:  #exp is even
                    #if (exp & 1) == 0:
                        base = base * base
                        #exp = exp / 2
                    else:
                        y = base * y
                        base = base * base
                    #exp = (exp – 1) / 2
                    exp = exp//2
                r = base * y
            exp_int[i,j] = r
    
    return exp_int

#@jit(types.Array(types.float64, 2, 'C')(types.Array(types.float64, 2, 'C'), numba.int64), nopython=True, cache=True, nogil=True)
def _powl(base, exp):
    #print(base,exp)
    #base can be any real and exp must be positive integer
    """
    Algorithm taken from https://stackoverflow.com/questions/2198138/calculating-powers-e-g-211-quickly
    https://en.wikipedia.org/wiki/Exponentiation_by_squaring
    """
    if exp == 0:
        return np.ones(base.shape)
    elif exp == 1:
        return base
    elif (exp & 1) != 0: #is even
        return base * _powl(base * base, exp // 2)
    else:
        return _powl(base * base, exp // 2)


@jit(numba.float64(numba.float64[:,:], numba.float64[:,:]), nopython=True,cache=True,nogil=True)
def mat_dis(A,B):
    return(np.sum(np.abs(A-B)))


