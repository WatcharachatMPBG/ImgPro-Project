import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import projectMethod as pm
import sys
import gentestdata
import textdetection
import flatteningtest


def main():
    kbdinput = sys.argv[1]
    gentestdata.main()
    flatteningtest.main()
    textdetection.main()



if __name__ == "__main__":
    main()