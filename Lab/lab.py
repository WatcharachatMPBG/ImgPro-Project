#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import cv2
import numpy as np

RESIZED_IMAGE_WIDTH = 24
RESIZED_IMAGE_HEIGHT = 24

img = cv2.imread("test1.png",0)
ret,binimg = cv2.threshold(img,125,255,cv2.THRESH_BINARY)
cv2.imshow("img", binimg)
#cv2.imshow("img", imgThresh)

intClassifications = []
npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

intChar = cv2.waitKey(0)
intClassifications.append(intChar)


npaFlattenedImage = binimg.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)

fltClassifications = np.array(intClassifications, np.float32)                   # convert classifications list of ints to numpy array of floats
npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))   # flatten numpy array of floats to 1d so we can write to file later


np.savetxt("classifications.txt", npaClassifications)           # write flattened images to file
np.savetxt("flattened_images.txt", npaFlattenedImages)

cv2.waitKey(0)
cv2.destroyAllWindows()
intChar = cv2.waitKey(0)
print(intChar)
