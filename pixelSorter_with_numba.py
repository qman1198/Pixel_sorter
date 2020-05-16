# -*- coding: utf-8 -*-
"""
Created on Wed May 13 22:04:23 2020

@author: Gianna
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import numba
from numba import njit


img = mpimg.imread('C:/Users/Gianna/.spyder-py3/ImageTest/Zohar-Sunflower.png')
width = len(img[0,:,:])
height = len(img)
crop_bounds = [0,height, 0, width]
crop_set = [list(range(crop_bounds[0],crop_bounds[1])), list(range(crop_bounds[2],crop_bounds[3]))]
crop_img = img[min(crop_set[0]):max(crop_set[0])+1,min(crop_set[1]):max(crop_set[1])+1,:]
cropW = len(crop_img[0,:,:])
cropH = len(crop_img)

row_set = range(0,cropH)
col_set = range(0,cropW)
ver_sort = False 
hor_sort = !ver_sort
rev = True

print("height: ", height, "width: ", width)
@njit
def bri(pix):
    
    R = pix[0]
    G = pix[1]
    B = pix[2]
    return (R+G+B)/3
    B = pix[2]
    return (R+G+B)/3

@njit
def pixsort(row):
    row = sorted(row,reverse = rev, key=bri) 
    return row


def horSort(c_img, row_set, sorted_img): #TODO: Use Numbas to make more efficient

    y = 0
    for row in c_img:
        if y in row_set : #TODO: is this if statement actually necessary?           
            sorted_img[y,:,:] = pixsort(row)
        else:
            sorted_img[y,:,:] = row
        y += 1
    return sorted_img


def verSort(c_img, col_set, sorted_img): #TODO: Use Numbas to make more efficient
    x = 0
    for col in c_img.swapaxes(1,0):
        if x in col_set :            
            sorted_img[:,x,:] = pixsort(col)
        else:
            sorted_img[:,x,:] = c_img[:,x,:]
        x += 1
    return sorted_img

def imgSort(c_img, row_set, col_set, ver_sort, hor_sort):    
    
    sorted_img = np.zeros_like(c_img)
    
    if hor_sort:
        sorted_img = horSort(c_img, row_set, sorted_img)
    if ver_sort:    
        sorted_img = verSort(c_img, col_set, sorted_img)
    return sorted_img

@njit
def imgCombine(img, c_img, sorted_img, crop_bounds):
    crop_set = [list(range(crop_bounds[0],crop_bounds[1])), list(range(crop_bounds[2],crop_bounds[3]))]
    out_img = img[:,:,:]
    if c_img.size != img.size:
        for y in crop_set[0]:
            for x in crop_set[1]:
                out_img[y,x,:] = sorted_img[y-crop_set[0][0],x-crop_set[1][0],:]
        return out_img
    else:
         return sorted_img

sorted_img = imgSort(crop_img, row_set, col_set, ver_sort, hor_sort)
plt.rcParams['savefig.pad_inches'] = 0

imgplot = plt.imshow(imgCombine(img, crop_img, sorted_img, crop_bounds))

plt.axis('off')
ddppii = (height + width)//10
plt.savefig("test.png", dpi = ddppii, bbox_inches="tight") #TODO: Autoset dpi so sizes match, or set using an image scale factor
