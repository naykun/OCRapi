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


def dirOCR(dirpath):
    '''
        do ocr operation on specific directory
        
        return a list contains tuples which likes (filename,ocrresultstring) 
    '''

    filelist = os.listdir(dirpath)
    results = []
    for filename in filelist:
        if os.path.isfile(filename):
            imagePath = os.path.join(dirpath,filename)
            try:
                image = np.array(PIL.Image.open(imagePath).convert('RGB'))
                result, image_framed = ocr.model(image)
                result_str = ""
                for key in result:
                    result_str += result[key][1]
                    result_str += '\n'
                results.append((filename,result_str))
            except Exception as e:
                print(e)
                continue      
    return results

def fileOCR(imagePath):
    '''
        do ocr operations on a single image file

        return a single string of ocr result
        
        lines split by '\\n'
    '''
    image = np.array(PIL.Image.open(imagePath).convert('RGB'))
    # print(image.shape())
    result, image_framed = ocr.model(image)
    result_str = ""
    for key in result:
        result_str += result[key][1]
        result_str += '\n'
    return result_str

def imgArrOCR(image):
    '''
        do ocr operations on a single image numpy array

        return a single string of ocr result
        
        lines split by '\\n'
    '''
    result, image_framed = ocr.model(image)
    result_str = ""
    for key in result:
        result_str += result[key][1]
        result_str += '\n'
    return result_str


if __name__ == '__main__':
    
    imagePath=sys.argv[1]

    image = np.array(PIL.Image.open(imagePath).convert('RGB'))
    print(image.shape())
    result, image_framed = ocr.model(image)
    for key in result:
        print(result[key][1])
