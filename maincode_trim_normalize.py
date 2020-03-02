import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil

def normalize(img,dimensioncrop):
    blank_image = np.zeros((dimensioncrop,dimensioncrop,3), np.uint8)
    width,height,channel = img.shape
    if width > dimensioncrop or height > dimensioncrop:
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

def crop_image_only_outside(img):
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


def horizontal_cut(img):
    
    img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21) #eliminnates noise
    ret,binimg = cv2.threshold(img,125,255,cv2.THRESH_BINARY) #turns image into binary
    binimg = cv2.bitwise_not(binimg) #inverts image
    #finding horizontal partition
    height,width,channel = binimg.shape
    lines = []

    blotcount = 0
    beginsignal = 1

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

    for x in filteredlines:
        cv2.line(img,(0,x),(width,x),(250,0,0),1)

    cropbegin = 0
    cnt = 0
    for x in filteredlines:
        if cropbegin == 0:
            cropbegin = x
        else:
            imgCrop = binimg[cropbegin-1:x+1,0:width]
            flag = cv2.imwrite('testfile/horizontalcutoutput/cropimage_{}.png'.format(cnt), imgCrop)
            #print(cnt,'H')
            #print(flag)
            cnt += 1
            cropbegin = 0
    cv2.imwrite('testfile/paragraphs_out.png',img)

    #cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return 'testfile/horizontalcutoutput/'

def vertical_cut(horizontalcutimg_path):

    cntimg = 0
    path = horizontalcutimg_path
    for file in os.listdir(path):
        if file.endswith(".png"):
            pass
        else:
            break
        #image preprocessing
        shutil.rmtree('testfile/verticalcutoutput/line{}'.format(cntimg),ignore_errors=True)

        os.makedirs('testfile/verticalcutoutput/line{}'.format(cntimg),exist_ok=True)
        binimg = cv2.imread('testfile/horizontalcutoutput/cropimage_{}.png'.format(cntimg))
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
                imgCrop = normalize(imgCrop,40)
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
    return 'testfile/verticalcutoutput'

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
img = cv2.imread(args["image"])

HCutOutputPath = horizontal_cut(img)
VCutOutputPath = vertical_cut(HCutOutputPath)