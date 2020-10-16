#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :convert_heic_2_jpg.py
@brief       :将heic图片格式转为jpg
@time        :2020/10/15 18:04:05
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import subprocess
import os
import io
import whatimage
import pyheif
import traceback
from PIL import Image
from glob import glob


def decodeImage(bytesIo , save_name):
    try:
        fmt = whatimage.identify_image(bytesIo)
        if fmt in ['heic']:
            i = pyheif.read_heif(bytesIo)
            pi = Image.frombytes(mode=i.mode, size=i.size, data=i.data)
            
            pi.save(save_name, format="jpeg")
    except:
        traceback.print_exc()


def read_image_file_rb(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    return file_data


if __name__ == "__main__":
    current_dir = os.getcwd()
    heic_lst = glob(current_dir + "/*.HEIC")
    for i in heic_lst:
        print(i)
        data = read_image_file_rb(i)
        decodeImage(data , i.replace("HEIC" , "jpg"))
    
