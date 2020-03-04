import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil

def imreadUnicode(imgDirectory): #reads image with unicode chars
    readimg = cv2.imdecode(np.fromfile(u'{}'.format(imgDirectory), np.uint8), cv2.IMREAD_UNCHANGED)
    return readimg

def imwriteUnicode(img,imgDir,imgName): #writes image to a file with unicode char name
    cv2.imwrite('{}/tempimg.png'.format(imgDir), img)
    os.rename(r'{}/tempimg.png'.format(imgDir),r'{}/{}.png'.format(imgDir,imgName))

def preprocess(img): #recieve input image and turns it into clean binary
    img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21) #eliminnates noise
    ret,binimg = cv2.threshold(img,125,255,cv2.THRESH_BINARY) #turns image into binary
    binimg = cv2.bitwise_not(binimg) #inverts image
    return binimg

def normalize(img,dimensioncrop): #extend image with black spaces to the desired dimension
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

def normalize_byresize(img,dimensioncrop): #extend image by scaling to the desired dimension: loses scale property
    blank_image = np.zeros((dimensioncrop,dimensioncrop,3), np.uint8)
    width,height,channel = img.shape
    dim = (dimensioncrop,dimensioncrop)
    if width > dimensioncrop or height > dimensioncrop:
        return blank_image
    blank_image = cv2.resize(img, dim, interpolation = cv2.INTER_NEAREST)
    return blank_image

def comparison(baseimg,comparator): #recieve 2 image outputs matching percentage by pixel
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

def comparison_split4x4(baseimg,comparator): #recieve 2 image and blocksize returns error percent
    width,height,channel = baseimg.shape
    width2,height2,channel2 = comparator.shape
    splitsize = 8
    if width == width2 and height == height2:
        #print('image dimension matched')
        pass
    else:
        print('invalid dimension')
        return 0
    if width % splitsize != 0 or height % splitsize != 0:
        print('indivisible to {} block'.format(splitsize))
        return 0
    blocksize = width//splitsize
    blockMatrix = (splitsize,splitsize)
    splitbase = np.zeros(blockMatrix)
    splitcompare = np.zeros(blockMatrix)
    for x in range(splitsize):
        for y in range(splitsize):
            for h in range(blocksize):
                for k in range(blocksize):
                    if baseimg[(x*blocksize)+h,(y*blocksize)+k,0] == 255:
                        splitbase[x,y] += 1
                    if comparator[(x*blocksize)+h,(y*blocksize)+k,0] == 255:
                        splitcompare[x,y] += 1
    error = np.zeros(blockMatrix)
    for x in range(splitsize):
        for y in range(splitsize):
            if splitcompare[x,y] == 0:
                if splitbase[x,y] == 0:
                    error[x,y] = 0
                else:
                    error[x,y] = 100
            else:
                error[x,y] = abs((splitcompare[x,y]-splitbase[x,y])/splitcompare[x,y])*100
    error_percent = 0
    for x in range(splitsize):
        for y in range(splitsize):
            error_percent += error[x,y]
    error_percent = error_percent/(splitsize*splitsize)
    return error_percent

def comparison_split4x4_getleast_error(baseimg,comparefolderPath): #recieve base image to compare to most fit img in folderPath
    leastError = 100
    fileWithLeastErrror = None
    errorPercent = 0
    for file in os.listdir(comparefolderPath):
        if file.endswith(".png"):
            pass
        else:
            continue
        compimg = imreadUnicode('{}/{}'.format(comparefolderPath,file))
        errorPercent = comparison_split4x4(baseimg,compimg)
        if errorPercent < leastError:
            leastError = errorPercent
            fileWithLeastErrror = '{}'.format(file)
    leastErrorImgComparedto = fileWithLeastErrror
    if fileWithLeastErrror == 'blank.png':
        leastErrorImgComparedto = 'X'
    else:
        leastErrorImgComparedto = leastErrorImgComparedto[0]
    return leastErrorImgComparedto

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