#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import sys
from matplotlib import pyplot as plt

MIN_CONTOUR_AREA = 10
RESIZED_IMAGE_WIDTH = 10
RESIZED_IMAGE_HEIGHT = 10

def imreadUnicode(imgDirectory): #reads image with unicode chars
    readimg = cv2.imdecode(np.fromfile(u'{}'.format(imgDirectory), np.uint8), cv2.IMREAD_UNCHANGED)
    return readimg

def imreadUnicodeGray(imgDirectory): #reads image with unicode chars
    readimg = cv2.imdecode(np.fromfile(u'{}'.format(imgDirectory), np.uint8), cv2.IMREAD_GRAYSCALE)
    return readimg

def imwriteUnicode(img,imgDir,imgName): #writes image to a file with unicode char name
    cv2.imwrite('{}/tempimg.png'.format(imgDir), img)
    os.rename(r'{}/tempimg.png'.format(imgDir),r'{}/{}.png'.format(imgDir,imgName))

def preprocess(img): #recieve input image and turns it into clean binary
    img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21) #eliminnates noise
    ret,binimg = cv2.threshold(img,125,255,cv2.THRESH_BINARY) #turns image into binary
    binimg = cv2.bitwise_not(binimg) #inverts image
    return binimg

def horizontal_cut(binimg,dest): #cuts binary image into folder 'horizontalcutoutput' by row to dest folder
    
    #finding horizontal partition
    height,width,channel = binimg.shape
    lines = []

    blotcount = 0
    beginsignal = 1

    shutil.rmtree('{}/horizontalcutoutput'.format(dest),ignore_errors=True)
    os.makedirs('{}/horizontalcutoutput'.format(dest),exist_ok=True)

    for x in range(height):
        for y in range(width):
            if binimg[x,y,0] == 255:
                blotcount += 1
        if blotcount > 0 and beginsignal == 1:
            lines.append(x)
            beginsignal = 0
        elif blotcount == 0 and beginsignal == 0:
            lines.append(x)
            beginsignal = 1
        blotcount = 0


    #print(lines_begin[0])
    #discarding close lines
    margin = 3
    linebefore = 0
    thisline = 0

    filteredlines = []

    for x in lines:
        if linebefore == 0 and thisline == 0:
            thisline = x
        elif thisline != 0 and linebefore == 0:
            filteredlines.append(thisline)
            linebefore = thisline
            thisline = x
        else:
            if thisline - linebefore >= margin and x - thisline >= margin:
                filteredlines.append(thisline)
            linebefore = thisline
            thisline = x
    filteredlines.append(thisline)
    #results are stored in filteredlines
    '''
    for x in filteredlines:
        cv2.line(img,(0,x),(width,x),(250,0,0),1)
    '''
    cropbegin = 0
    cnt = 0
    for x in filteredlines:
        if cropbegin == 0:
            cropbegin = x
        else:
            imgCrop = binimg[cropbegin-1:x+1,0:width]
            flag = cv2.imwrite('{}/horizontalcutoutput/cropimage_{}.png'.format(dest,cnt), imgCrop)
            #print(cnt,'H')
            #print(flag)
            cnt += 1
            cropbegin = 0
    #cv2.imwrite('testfile/paragraphs_out.png',img)

    #cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return dest

def vertical_cut(horizontalcutfolder_path): #cuts horizontal cuts outputs into small chars by line into same directory

    cntimg = 0
    path = '{}/horizontalcutoutput'.format(horizontalcutfolder_path)
    for file in os.listdir(path):
        if file.endswith(".png"):
            pass
        else:
            break
        #image preprocessing
        shutil.rmtree('{}/verticalcutoutput/line{}'.format(horizontalcutfolder_path,cntimg),ignore_errors=True)

        os.makedirs('{}/verticalcutoutput/line{}'.format(horizontalcutfolder_path,cntimg),exist_ok=True)
        binimg = cv2.imread('{}/horizontalcutoutput/cropimage_{}.png'.format(horizontalcutfolder_path,cntimg))
        height,width,channel = binimg.shape

        #finding vertical partition
        lines = []

        blotcount = 0
        beginsignal = 1

        for y in range(width):
            for x in range(height):
                if binimg[x,y,0] == 255:
                    blotcount += 1
            if blotcount > 0 and beginsignal == 1:
                lines.append(y)
                beginsignal = 0
            elif blotcount == 0 and beginsignal == 0:
                lines.append(y)
                beginsignal = 1
            blotcount = 0


        #print(lines_begin[0])
        #discarding close lines
        margin = 0
        linebefore = 0
        thisline = 0

        filteredlines = []

        for x in lines:
            if linebefore == 0 and thisline == 0:
                thisline = x
            elif thisline != 0 and linebefore == 0:
                filteredlines.append(thisline)
                linebefore = thisline
                thisline = x
            else:
                if thisline - linebefore >= margin and x - thisline >= margin:
                    filteredlines.append(thisline)
                linebefore = thisline
                thisline = x
        filteredlines.append(thisline)
        #results are stored in filteredlines
        '''
        for x in filteredlines:
            cv2.line(binimg,(x,0),(x,height),(250,0,0),1)
        '''
        cropbegin = 0
        cnt = 0
        for x in filteredlines:
            if cropbegin == 0:
                cropbegin = x
            else:
                imgCrop = binimg[0:height,cropbegin-1:x+1]
                imgCrop = crop_image_only_outside(imgCrop)
                imgCrop = normalize(imgCrop,24)
                flag = cv2.imwrite('testfile/verticalcutoutput/line{}/cropimage_{}.png'.format(cntimg,cnt), imgCrop)
                #print(cnt,'V')
                #print(flag)
                cnt += 1
                cropbegin = 0
        cv2.imwrite('testfile/paragraphs_out.png',binimg)

        #cv2.imshow('image',binimg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cntimg += 1
    return '{}/verticalcutoutput'.format(horizontalcutfolder_path)

def imshow_components(labels):
    # Map component labels to hue val
    label_hue = np.uint8(170*labels/np.max(labels))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue==0] = 0

    cv2.imshow('labeled.png', labeled_img)
    cv2.waitKey()

def crop_image_only_outside(img): #crop image to reduce all blackspace outside
    height,width,channel = img.shape
    top = 0
    bottom = 0
    left = 0
    right = 0
    for x in range(height):
        for y in range(width):
            if img[x,y,0] == 255:
                top = x
                break
        if top != 0:
            break
    Cropimg = img[top:height,0:width]
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


baseimg = imreadUnicode("testverticalcut.png")
baseimg = crop_image_only_outside(baseimg)
#baseimg = preprocess(baseimg)

img = baseimg.copy()
height,width,channel = img.shape

#ส่วนนี้เป็นการตีกรอบพยัญชนะ
blotcountsAlongHeight = np.zeros(height)
maxblotcountsAlongHeight = 0
for x in range(height):
    for y in range(width):
        if img[x,y,0] == 255:
            blotcountsAlongHeight[x] += 1
    if blotcountsAlongHeight[x] > maxblotcountsAlongHeight:
        maxblotcountsAlongHeight = blotcountsAlongHeight[x]
trimlines = []
beginsignal = 1
for x in range(height):
    #cv2.line(img,(0,cnt),(int(x),cnt),(250,0,0),1)
    if blotcountsAlongHeight[x] > 0 and blotcountsAlongHeight[x] / maxblotcountsAlongHeight > 0.5 and beginsignal == 1:
        cv2.line(img,(0,x),(width,x),(0,0,250),1)
        beginsignal = 0
        cropbegin = x-1
        trimlines.append(x)
    elif blotcountsAlongHeight[x] > 0 and blotcountsAlongHeight[x] / maxblotcountsAlongHeight <= 0.5 and beginsignal == 0:
        cv2.line(img,(0,x-1),(width,x-1),(0,0,250),1)
        beginsignal = 1
        cropend = x-1
        trimlines.append(x-1)
print('trim points =',trimlines)
####end

###ส่วนนี้เป็นการแยกสระบน-ล่างออกมาให้ได้
lines = []
croppedImg = baseimg[cropbegin:cropend,0:width]
trimheight,trimwidth,channel = croppedImg.shape
blotcount = 0
for y in range(trimwidth):
    for x in range(trimheight):
        if croppedImg[x,y,0] == 255:
            blotcount += 1
    if blotcount > 0 and beginsignal == 1:
        lines.append(y)
        beginsignal = 0
    elif blotcount == 0 and beginsignal == 0:
        lines.append(y)
        beginsignal = 1
    blotcount = 0

for x in lines:
    cv2.line(img,(x,0),(x,height),(0,240,0),1)
###end
neo = baseimg
neogray = cv2.cvtColor(neo, cv2.COLOR_BGR2GRAY)
ret,binneoimg = cv2.threshold(neogray,125,255,cv2.THRESH_BINARY)
print(binneoimg.shape)
num_labels, labels_im, stats, centroids = cv2.connectedComponentsWithStats(binneoimg)
label_height,label_width = labels_im.shape

#####label rearrange

newlabeldict = {}
newlabelcount = 0
for x in range(label_width):
    for y in range(label_height):
        if labels_im[y,x] in newlabeldict :
            labels_im[y,x] = newlabeldict[labels_im[y,x]]
        else:
            newlabeldict[labels_im[y,x]] = newlabelcount
            newlabelcount += 1
            labels_im[y,x] = newlabeldict[labels_im[y,x]]
            
######end
binary = labels_im == 1
plt.imshow(binary)
plt.show()
######label seperation into images
for label in range(1,num_labels):
    tlabel = newlabeldict[label]
    width = stats[tlabel, cv2.CC_STAT_WIDTH]
    height = stats[tlabel, cv2.CC_STAT_HEIGHT]
    x = stats[tlabel, cv2.CC_STAT_LEFT]
    y = stats[tlabel, cv2.CC_STAT_TOP]
    roi = baseimg[y:y + height, x:x + width]
    cv2.imwrite(r'laboutput/{}.png'.format(tlabel), roi)
###end

'''
kernel = np.ones((1,10),np.uint8)
img = cv2.dilate(img,kernel,iterations = 1)
'''
#imgCrop = img[cropbegin:cropend,0:width]
if True:
    imshow_components(labels_im)
    cv2.imshow("baseimg",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()