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
    basetext = sys.argv[1]
    comparetext = sys.argv[2]
    res = {} 
    for keys in test_str: 
        res[keys] = res.get(keys, 0) + 1

if __name__ == "__main__":
    main()