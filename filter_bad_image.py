#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :filter_bad_image.py
@brief       :过滤掉损坏的图片
@time        :2020/10/14 15:51:44
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

from PIL import Image
import os
from imutils.paths import list_images
from tqdm import tqdm


def is_valid_image(path):
    try:
        bValid = True
        fileObj = open(path, 'rb')  # 以二进制形式打开
        buf = fileObj.read()
        if not buf.startswith(b'\xff\xd8'):  # 是否以\xff\xd8开头
            bValid = False
        elif buf[6:10] in (b'JFIF', b'Exif'):  # “JFIF”的ASCII码
            if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):  # 是否以\xff\xd9结尾
                bValid = False
        else:
            try:
                Image.open(fileObj).verify()
            except Exception as e:
                bValid = False
                print(e)
    except Exception as e:
        return False
    return bValid


def is_valid(file):
    valid = True
    try:
        Image.open(file).load()
    except OSError:
        valid = False
    return valid


if __name__ == '__main__':
    data_dir = os.getcwd()
    image_lsts = list(list_images(data_dir))

    for name in tqdm(image_lsts):
        if is_valid_image(name):
            continue
        else:
            os.remove(name)
    print("finished")
