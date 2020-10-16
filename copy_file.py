
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :copy_file.py
@brief       :复制文件
@time        :2020/10/16 14:11:07
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''



import sys
import os
import glob
import shutil
import argparse
from imutils.paths import list_images
from tqdm import tqdm


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image", help='input image dir')
    args = vars(parser.parse_args())
    
    current_dir = os.getcwd()
    image_lst = list(list_images(args['image']))
    for name in tqdm(image_lst):
        new_name = os.path.join(current_dir , os.path.basename(name))
        shutil.copyfile(name , new_name)


