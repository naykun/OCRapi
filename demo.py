#-*- coding:utf-8 -*-

import sys

import os
import ocr
import time
import shutil
import numpy as np
import PIL.Image
from glob import glob
import csv

if __name__ == '__main__':
    
    imagePath=sys.argv[1]

    image = np.array(PIL.Image.open(imagePath).convert('RGB'))

    result, image_framed = ocr.model(image)
    for key in result:
        print(result[key][1])
