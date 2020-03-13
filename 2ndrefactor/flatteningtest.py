#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import cv2
import numpy as np
import operator
import os
import projectMethod as pm
import sys
import json

RESIZED_IMAGE_WIDTH = 36
RESIZED_IMAGE_HEIGHT = 36

def main():
    #thString = 'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮฯะัาำิีึืฺุู฿เแโใไๅๆ็่้๊๋์ํ๎๏๐๑๒๓๔๕๖๗๘๙๚๛'
    dictThaitoNum = json.load(open("dictThaitoNum.txt"))
    dictNumtoThai = json.load(open("dictNumtoThai.txt"))
    try:
        npaClassifications = np.loadtxt("classificationsV2.txt", np.float32)                  # read in training classifications
    except:
        print ("error, unable to open classifications.txt, exiting program\n")
        os.system("pause")
    # end try

    try:
        npaFlattenedImages = np.loadtxt("flattened_imagesV2.txt", np.float32)                 # read in training images
    except:
        print ("error, unable to open flattened_images.txt, exiting program\n")
        os.system("pause")
    # end try

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train
    kNearest = cv2.ml.KNearest_create()                   # instantiate KNN object
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    VCutOutputPath = 'testtingImgs/verticalcutoutput'
    strFinalString = ""
    folderCount = 0
    for folder in os.listdir(VCutOutputPath):
        count = 0
        strFinalString = strFinalString + '\n'
        for file in os.listdir('{}/line{}'.format(VCutOutputPath,folderCount)):
            if file.endswith(".png"):
                pass
            else:
                break
            img = pm.imreadUnicodeGray('{}/line{}/cropimage_{}.png'.format(VCutOutputPath,folderCount,count))
            count += 1

            ret,imgROIResized = cv2.threshold(img,125,255,cv2.THRESH_BINARY)

            npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))      # flatten image into 1d numpy array

            npaROIResized = np.float32(npaROIResized)       # convert from 1d numpy array of ints to 1d numpy array of floats

            retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)     # call KNN function find_nearest

            ordofCurrentchar = int(npaResults[0][0])
            strCurrentChar = dictNumtoThai[str(ordofCurrentchar)]                                       # get character from results

            strFinalString = strFinalString + strCurrentChar           # append current char to full string
        folderCount += 1
        # end for
    print ("\n" + strFinalString + "\n")
    #ก =161 กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮฯะัาำิีึืฺุู฿เแโใไๅๆ็่้๊๋์ํ๎๏๐๑๒๓๔๕๖๗๘๙๚๛

if __name__ == "__main__":
    main()