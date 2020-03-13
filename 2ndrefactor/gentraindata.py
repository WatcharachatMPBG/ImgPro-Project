import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import projectMethod as pm
import sys


def main():
    kbdinput = 'x'
    cntimagetillnow = 0
    while kbdinput != '':
        print("type your test image name:")
        kbdinput = str(input())
        if kbdinput == '':
            break
        inputImg = cv2.imread(kbdinput)
        binimg = pm.preprocess(inputImg)

        dest = 'trainingImgs'
        pm.horizontal_cut(binimg,dest)
        cntimagetillnow = pm.vertical_cutTraining(dest,cntimagetillnow)
        print('{}'.format(cntimagetillnow),' images now loaded.')

if __name__ == "__main__":
    main()