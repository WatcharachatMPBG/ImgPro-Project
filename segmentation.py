import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('testfile/testimage.jpg')
ret,binimg = cv2.threshold(img,127,255,cv2.THRESH_BINARY) #turns image into binary
height,width,channel = img.shape


'''
cv2.imshow('image',blur)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
