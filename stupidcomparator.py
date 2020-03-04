import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import projectmethod as pm
import sys

filename1 = sys.argv[1]
filename2 = sys.argv[2]
img1 = pm.imreadUnicode(filename1)

print(pm.comparison_split4x4_getleast_error(img1,filename2))

cv2.waitKey(0)
cv2.destroyAllWindows()