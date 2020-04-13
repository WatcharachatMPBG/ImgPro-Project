import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import os

def crop_image_only_outside(img):
    height,width,channel = img.shape
    top = 0
    bottom = 0
    left = 0
    right = 0
    for x in range(height):
        for y in range(width):
            if img[x,y,0] == 255:
                top = x-1
                break
        if top != 0:
            break
    Cropimg = img[top:height,0:width]
    cv2.imshow('image',Cropimg)
    height,width,channel = Cropimg.shape
    for y in range(width):
        for x in range(height):
            if Cropimg[x,y,0] == 255:
                left = y
                break
        if left != 0:
            break
    Cropimg = Cropimg[0:height,left:width]
    height,width,channel = Cropimg.shape
    for x in range(height):
        for y in range(width):
            if Cropimg[height-x-1,width-y-1,0] == 255:
                bottom = height-x
                break
        if bottom != 0:
            break
    Cropimg = Cropimg[0:bottom,0:width]
    height,width,channel = Cropimg.shape
    for y in range(width):
        for x in range(height):
            if Cropimg[height-x-1,width-y-1,0] == 255:
                right = width-y
                break
        if right != 0:
            break
    Cropimg = Cropimg[0:height,0:right]
    return Cropimg

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
img = cv2.imread(args["image"])
img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21) #eliminnates noise
ret,binimg = cv2.threshold(img,125,255,cv2.THRESH_BINARY) #turns image into binary
binimg = cv2.bitwise_not(binimg) #inverts image
binimg = crop_image_only_outside(binimg)

#cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()