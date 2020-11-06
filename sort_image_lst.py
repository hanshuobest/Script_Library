#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :sort_image_lst.py
@brief       :图片逆排序
@time        :2020/11/05 15:37:11
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import os
from glob import glob
import shutil

def main():
    current_dir = os.getcwd()
    image_lst = glob(current_dir + "/*.jpg")
    image_lst = sorted(image_lst , key= lambda item: os.path.basename(item).split('-')[0] , reverse=True)
    for i , name in enumerate(image_lst):
        new_name = str(i) + ".jpg"
        os.rename(name , os.path.join(os.path.dirname(name) , new_name))


if __name__ == '__main__':
    main()
    

