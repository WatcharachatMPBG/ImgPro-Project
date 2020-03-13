import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import projectMethod as pm
import sys


def main():
    kbdinput = sys.argv[1]
    inputImg = cv2.imread(kbdinput)
    binimg = pm.preprocess(inputImg)
    dest = 'testtingImgs'
    pm.horizontal_cut(binimg,dest)
    pm.vertical_cut(dest)

if __name__ == "__main__":
    main()