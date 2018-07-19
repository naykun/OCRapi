#-*- coding:utf-8 -*-

import sys

import os
import ocr
import time
import shutil
import numpy as np
import os.path
from PIL import Image
from glob import glob
import csv
import imghdr
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy

from multiprocessing import Pool, Queue, Process, Manager

def hasBlackAround(x, y, distance, img):
    w, h = img.size
    startX = 0 if x - distance < 0 else x - distance
    startY = 0 if y - distance < 0 else y - distance
    endX = w - 1 if x + distance > w - 1 else x + distance
    endY = h - 1 if y + distance > h - 1 else y + distance
    hasBlackAround = False
    for j in range(startX, endX):
        for k in range(startY, endY):
            r, g, b = img.getpixel((j, k))
            if r < 130 and g < 130 and b < 130:
                return True
    return False


def OCRconsumer(q,targetPath):
    result_str = ""
    while True:
        # if q.empty():
        #     print(1)
        #     continue
        
        res = q.get()
        if res is None : break
        tic = time.time()
        id,image = res
        result, image_framed = ocr.model(image)
        toc = time.time()
        print("one pic predict complete, it took {:.3f}s".format(toc - tic))
        j=0        
        result_str+=str(id)
        result_str+='\n'

        for key in result:
            if j==0 or j==1:
                str_tmp=str(result[key][1])
                result_str+=str_tmp
                result_str+='\n'
            else:
                break
            j+=1
        result_str+="###\n"
    txt_path=targetPath+"/OnlineShopLicense.txt"
    writer=open(txt_path,'a')
    writer.write(result_str)


def preprocess(id,imagePath,q):
    img = Image.open(imagePath)
    # print(img.size)
    w_tmp, h_tmp = img.size
    print(h_tmp)
    if h_tmp>620:
        img=img.crop((0,0,w_tmp,500))
        h_tmp=500
        print(img.size[1])
    img_blender=img
    print(img_blender.size)
    if str(imghdr.what(imagePath))=='png':
        try:
            img_blender = Image.new('RGBA', img.size, (255,255,255,0))
            img_blender.paste(img,(0,0),mask = img)
        except  Exception as e:
            print("error")
    rgb_im = img_blender.convert('RGB')
    w,h=rgb_im.size
    for x in range(0, w - 1):
        for y in range(0, h - 1):
            if not hasBlackAround(x, y, 1, rgb_im):
                rgb_im.putpixel((x, y), (255, 255, 255))
    # rgb_im.save('/home/wuxingzhe/wu.png')
    image = np.array(rgb_im.convert('RGB'))
    out = (id,image)
    q.put(out)


if __name__ == '__main__':
    
    sstart = time.time()
    sourcePath=sys.argv[1]
    targetPath=sys.argv[2]
    txt_path=targetPath+"/OnlineShopLicense.txt"

    manager = Manager()
    imageQueue = manager.Queue()
    preprocess_pool = Pool()

    for dirpath,dirnames,filenames in os.walk(sourcePath):
        fir_arr=filenames
        for fir in filenames:
            pos=fir.find('.')
            type_str=fir[pos+1:]
            a=[ ch for ch in fir if ch>='0' and ch<='9']
            id=""
            for ch in a:
                id+=ch
            id=int(id)

            imagePath=os.path.join(dirpath,fir)
            preprocess_pool.apply_async(func=preprocess,args = (id,imagePath,imageQueue,))

    
    preprocess_pool.close()
    preprocess_pool.join()
    print(imageQueue.qsize())
    # ocr_consumer = Process(target=OCRconsumer,args = (imageQueue,targetPath))
    imageQueue.put(None)
    # ocr_consumer.start()
    # ocr_consumer.join()
    OCRconsumer(imageQueue,targetPath)

    file = open(txt_path)
    lines=file.readlines()
    j=0
    id=0

    workbook = xlwt.Workbook(encoding = 'utf-8')
    worksheet = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
    worksheet.col(0).width = 5120
    worksheet.col(1).width = 5120
    worksheet.write(0, 1, '企业注册号')
    worksheet.write(0, 0, '企业名称')

    for line in lines:
        if line.strip()=="###":
            j=0
            continue
        if j%3==0:
            id=int(line.strip())
        elif j%3==1:
            index_tmp=line.find(':')
            if index_tmp>=0:
                worksheet.write(id, 1, line[index_tmp+1:-1])
        else:
            index_tmp=line.find(':')
            if index_tmp>=0:
                worksheet.write(id, 0, line[index_tmp+1:-1])
        j+=1


    excel_path=targetPath+"/OnlineShopLicense.xls"
    workbook.save(excel_path)
    eend = time.time()
    print("Mission complete, it took {:.3f}s".format(eend - sstart))

        
    
    
    #result_txt.write(imagePath)
    #result_txt.write("\n")



