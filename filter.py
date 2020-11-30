#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :filter.py
@brief       :过滤获取baby cry audio
@time        :2020/11/30 15:04:41
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import os
from shutil import rmtree
import shutil

def main():
    cry_dir = "cry"
    if os.path.exists(cry_dir):
        rmtree(cry_dir)
        os.mkdir(cry_dir)
    else:
        os.mkdir(cry_dir)
        
    with open("cry.txt" , "r") as f:
        all_lines = f.readlines()
        all_file = []
        for line in all_lines:
            name = line.strip()
            
            if os.path.exists(name):
                shutil.copyfile(name , os.path.join(cry_dir , name))
            

if __name__ == '__main__':
    main()
    