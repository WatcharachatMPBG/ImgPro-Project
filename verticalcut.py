import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import shutil

cntimg = 10
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
        flag = cv2.imwrite('testfile/verticalcutoutput/line{}/cropimage_{}.png'.format(cntimg,cnt), imgCrop)
        print(cnt)
        print(flag)
        cnt += 1
        cropbegin = 0
cv2.imwrite('testfile/paragraphs_out.png',binimg)

#cv2.imshow('image',binimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
