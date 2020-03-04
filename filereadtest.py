import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import sys

def imreadUnicode(imgDirectory):
    readimg = cv2.imdecode(np.fromfile(u'{}'.format(imgDirectory), np.uint8), cv2.IMREAD_UNCHANGED)
    return readimg

def imwriteUnicode(img,imgDir,imgName):
    cv2.imwrite('{}/tempimg.png'.format(imgDir), img)
    os.rename(r'{}/tempimg.png'.format(imgDir),r'{}/{}.png'.format(imgDir,imgName))

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

def comparison_split4x4(baseimg,comparator,blocksize):
    width,height,channel = baseimg.shape
    width2,height2,channel2 = comparator.shape
    if width == width2 and height == height2:
        print('image dimension matched')
    else:
        print('invalid dimension')
        return 0
    
    splitbase = [0,0,0,0]
    splitcompare = [0,0,0,0]
    for x in range(blocksize):
        for y in range(blocksize):
            if baseimg[x,y,0] == 255:
                splitbase[0] += 1
            if comparator[x,y,0] == 255:
                splitcompare[0] += 1
            if baseimg[x+blocksize,y,0] == 255:
                splitbase[1] += 1
            if comparator[x+blocksize,y,0] == 255:
                splitcompare[1] += 1
            if baseimg[x,y+blocksize,0] == 255:
                splitbase[2] += 1
            if comparator[x,y+blocksize,0] == 255:
                splitcompare[2] += 1
            if baseimg[x+blocksize,y+blocksize,0] == 255:
                splitbase[3] += 1
            if comparator[x+blocksize,y+blocksize,0] == 255:
                splitcompare[3] += 1
    error = [0,0,0,0]
    for x in range(4):
        if splitcompare[x] == 0:
            if splitbase == 0:
                error[x] = 0
            else:
                error[x] = 100
        else:
            error[x] = abs((splitcompare[x]-splitbase[x])/splitcompare[x])*100
    match_percent = (error[0]+error[1]+error[2]+error[3])/4
    return match_percent

filename1 = sys.argv[1]
filename2 = sys.argv[2]
img1 = imreadUnicode(filename1)
for file in os.listdir(filename2):
    print(file)
    if file.endswith(".png"):
        pass
    else:
        break
    compimg = imreadUnicode('{}/{}'.format(filename2,file))
    print('error =',comparison_split4x4(img1,compimg,8))

cv2.waitKey(0)
cv2.destroyAllWindows()