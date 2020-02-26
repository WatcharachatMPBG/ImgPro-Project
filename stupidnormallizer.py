import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import os

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
    return True
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])

img = normalize(img)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()