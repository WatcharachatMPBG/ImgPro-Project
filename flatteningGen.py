#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import cv2
import numpy as np
import projectmethod as pm
import os

RESIZED_IMAGE_WIDTH = 24
RESIZED_IMAGE_HEIGHT = 24
trainImageFolder = 'testfile/normalizertest/charcomparators'

intClassifications = []
npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

for file in os.listdir(trainImageFolder):
    if file.endswith(".png"):
        pass
    else:
        break
    img = pm.imreadUnicodeGray('{}/{}'.format(trainImageFolder,file))
    ret,binimg = cv2.threshold(img,125,255,cv2.THRESH_BINARY)
    cv2.imshow("img", img)

    print('input key:')
    intChar = cv2.waitKey(0)
    print(intChar)

    intClassifications.append(intChar)
    npaFlattenedImage = img.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
    npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)

fltClassifications = np.array(intClassifications, np.float32)                   # convert classifications list of ints to numpy array of floats
npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))   # flatten numpy array of floats to 1d so we can write to file later


#np.savetxt("classifications.txt", npaClassifications)           # write flattened images to file
#np.savetxt("flattened_images.txt", npaFlattenedImages)

cv2.destroyAllWindows()