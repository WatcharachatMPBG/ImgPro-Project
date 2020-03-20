#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import cv2
import numpy as np
import projectMethod as pm
import os
import json

RESIZED_IMAGE_WIDTH = 36
RESIZED_IMAGE_HEIGHT = 36
trainImageFolder = 'trainingImgs/verticalcutoutput'

def main():

    intClassifications = []
    npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

    '''
    #init dictionary
    dictionary = {"dictcount":0}
    json.dump(dictionary, open("dictThaitoNum.txt",'w'))
    json.dump(dictionary, open("dictNumtoThai.txt",'w'))
    '''
    
    '''
    #open dictionary
    d2 = json.load(open("text.txt"))
    '''

    dictThaitoNum = json.load(open("dictThaitoNum.txt"))
    dictNumtoThai = json.load(open("dictNumtoThai.txt"))
    dictnumbering = dictThaitoNum['dictcount']

    for file in os.listdir(trainImageFolder):
        if file.endswith(".png"):
            pass
        else:
            break
        img = pm.imreadUnicodeGray('{}/{}'.format(trainImageFolder,file))
        ret,binimg = cv2.threshold(img,125,255,cv2.THRESH_BINARY)
        cv2.imshow("img", img)
        cv2.waitKey(10)
        print('input key:')
        intChar = str(input())
        print("your input is: ",intChar)

        if intChar in dictThaitoNum:
            print("char found!")
            dictnumbering = dictThaitoNum[intChar]

            intClassifications.append(dictnumbering)
            npaFlattenedImage = img.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
            npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)
        elif intChar == '':
            print("char ignored")
        else:
            print("new char!, added to dict")
            dictThaitoNum['dictcount'] += 1
            dictNumtoThai['dictcount'] += 1
            dictThaitoNum[intChar] = dictThaitoNum['dictcount']
            dictnumbering = dictThaitoNum[intChar]
            dictNumtoThai[dictnumbering] = intChar
            intClassifications.append(dictnumbering)
            npaFlattenedImage = img.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
            npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)
        '''
        intClassifications.append(dictnumbering)
        npaFlattenedImage = img.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))  # flatten image to 1d numpy array so we can write to file later
        npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)
        '''

    fltClassifications = np.array(intClassifications, np.float32)                   # convert classifications list of ints to numpy array of floats
    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))   # flatten numpy array of floats to 1d so we can write to file later


    np.savetxt("classificationsV2.txt", npaClassifications)           # write flattened images to file
    np.savetxt("flattened_imagesV2.txt", npaFlattenedImages)
    json.dump(dictThaitoNum, open("dictThaitoNum.txt",'w'))
    json.dump(dictNumtoThai, open("dictNumtoThai.txt",'w'))
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()