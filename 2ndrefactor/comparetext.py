#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import projectMethod as pm
import sys


def main():
    basetext = str(sys.argv[1])
    comparetext = str(sys.argv[2])
    textstring = (open(basetext,encoding="utf8")).read()
    textstring2 = (open(comparetext,encoding="utf8")).read()
    res1 = {} 
    for keys in textstring: 
        res1[keys] = res1.get(keys, 0) + 1
    print (res1)
    res2 = {} 
    for keys in textstring2: 
        res2[keys] = res2.get(keys, 0) + 1
    print (res2)
    diff = {}
    for keys in res1.keys():
        if keys in res2:
            diff[keys] = res1[keys] - res2[keys]
    print(diff)


if __name__ == "__main__":
    main()