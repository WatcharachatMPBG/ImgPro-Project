import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil

def normalize(img):
    blank_image = np.zeros((60,60,3), np.uint8)
    width,height,channel = img.shape
    if width > 60 or height > 60:
        return blank_image
    for x in range(width):
        for y in range(height):
            blank_image[x,y,0] = img[x,y,0]
            blank_image[x,y,1] = img[x,y,1]
            blank_image[x,y,2] = img[x,y,2]
    return blank_image
def comparison(baseimg,comparator):
    width,height,channel = baseimg.shape
    width2,height2,channel2 = comparator.shape
    if width == width2 and height == height2:
        print('image dimension matched')
    else:
        print('invalid dimension')
        return 0
    matchingpix = 0
    pixdetected = 3600
    for x in range(width):
        for y in range(height):
            if comparator[x,y,0] == baseimg[x,y,0]:
                matchingpix += 1
    match_percent = matchingpix/pixdetected
    match_percent = str(round(match_percent, 2))
    return match_percent

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

img = normalize(img)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()