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
from fuzzywuzzy import fuzz

text_file = open("filtered.txt", "wb")

def main():
    basetext = str((sys.argv[1]))
    comparetext = str(sys.argv[2])
    textstring = (open(basetext,encoding="utf8")).read().replace("ำ","ํา")
    textstring2 = (open(comparetext,encoding="utf8")).read()
    res1 = {} 
    for keys in textstring: #กรองมาคิดเฉพาะ text ไทยเท่านั้น
        if keys in "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮฯะัาำิีึืฺุู฿เแโใไๅๆ็่้๊๋์ํ๎๏๐๑๒๓๔๕๖๗๘๙๚๛":
            res1[keys] = res1.get(keys, 0) + 1
    print (res1)
    res2 = {} 
    for keys in textstring2: 
        res2[keys] = res2.get(keys, 0) + 1
    print (res2)

    charcount = 0
    diffcount = 0
    diff = {}
    res1['ํ'] = 0
    for keys in res1.keys():
        charcount += res1[keys]
        if keys == 'ำ':
            res1['ํ'] += res1[keys]
            res1['า'] += res1[keys] 
        if keys in res2:
            diff[keys] = abs(res1[keys] - res2[keys])
        else:
            diff[keys] = res1[keys]
        diffcount += diff[keys]
    print("charcount = {}".format(charcount))
    print("diffcount = {}".format(diffcount))
    print("error = ",((abs(charcount - (charcount - diffcount)))/charcount)*100,'%')
    print("Simple Ratio = ",fuzz.ratio(basetext,comparetext))
    print("Partial Ratio = ",fuzz.partial_ratio(basetext,comparetext))
    print("Token Sort Ratio = ",fuzz.token_sort_ratio(basetext,comparetext))
    print("Token Set Ratio = ",fuzz.token_set_ratio(basetext,comparetext))
    text_file.write(textstring.encode("utf8"))
    text_file.close()


if __name__ == "__main__":
    main()