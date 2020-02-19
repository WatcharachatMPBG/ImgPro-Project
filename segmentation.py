import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('testfile/testimage.jpg')
ret,binimg = cv2.threshold(img,127,255,cv2.THRESH_BINARY) #turns image into binary
height,width,channel = img.shape

line_height_estimate = 60
lines_begin = []
lines_end = []

blotcount = 0
beginsignal = 1

for x in range(height):
    for y in range(width):
        if binimg[x,y,0] == 0:
            blotcount += 1
    if blotcount > 0 and beginsignal == 1:
        lines_begin.append(x)
        beginsignal = 0
    elif blotcount == 0 and beginsignal == 0:
        lines_end.append(x)
        beginsignal = 1
    blotcount = 0


#print(lines_begin[0])

for x in lines_begin:
    cv2.line(img,(0,x),(width,x),(0,250,0),1)
for x in lines_end:
    cv2.line(img,(0,x),(width,x),(250,0,0),1)



cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('testfile/paragraphs_out.png',img)

