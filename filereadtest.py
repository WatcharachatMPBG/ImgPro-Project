import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import sys


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
    notmatchpix = 0
    #pixdetected = 3600
    #change method at later deate
    for x in range(width):
        for y in range(height):
            if comparator[x,y,0] == 255 and baseimg[x,y,0] == 255:
                matchingpix += 1
            elif comparator[x,y,0] != baseimg[x,y,0]:
                notmatchpix += 1
    match_percent = matchingpix/notmatchpix
    match_percent = str(round(match_percent, 2))
    return match_percent

filename1 = sys.argv[1]
filename2 = sys.argv[2]
img1 = cv2.imread(filename1)
for file in os.listdir(filename2):
    print(file)
    if file.endswith(".png"):
        pass
    else:
        break
    compimg = cv2.imdecode(np.fromfile(u'{}\{}'.format(filename2,file), np.uint8), cv2.IMREAD_UNCHANGED)
    #compimg = cv2.imread(file)
    print(comparison(img1,compimg))

        


cv2.waitKey(0)
cv2.destroyAllWindows()