import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
#image preprocessing

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
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
        print(cnt)
        print(flag)
        cnt += 1
        cropbegin = 0
cv2.imwrite('testfile/paragraphs_out.png',img)

#cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()



