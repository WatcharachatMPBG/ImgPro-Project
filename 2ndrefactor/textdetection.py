import numpy as np
from persistence1d import RunPersistence
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import projectMethod as pm
import sys


def main():
    kbdinput = sys.argv[1]
    inputImg = cv2.imread("docs/{}".format(kbdinput))
    binimg = pm.preprocess(inputImg)
    dest = 'testfolder'
    height,width,channel = binimg.shape
    print(height,width,channel)
    cv2.imshow("img",inputImg)

    changeMeasure = 10
    pixFreqData = []
    box = 0
    total = 0
    for x in range(height):
        for y in range(width):
            if binimg[x,y,0] != 0:
                box += 1
                total += 1
        pixFreqData.append(box)
        box = 0
    avgblot = total//height
    
    for x in range(height):
        inputImg = cv2.line(inputImg, (0,x),(pixFreqData[x],x),(255,0,0),1)
    
    graphData = np.array(pixFreqData)
    ExtremaAndPersistence = RunPersistence(InputData)

    '''
    for x in range(height):
        if x+1 < height:
            if abs(pixFreqData[x] - pixFreqData[x+1]) >= changeMeasure:
                inputImg = cv2.line(inputImg, (0,x),(200,x),(0,255,0),1)
    '''
    '''
    for x in range(height):
        if pixFreqData[x] > avgblot:
                inputImg = cv2.line(inputImg, (0,x),(200,x),(0,0,255),1)
    '''
    cv2.imshow("img",inputImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()