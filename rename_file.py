#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :rename_file.py
@brief       :图片重命名
@time        :2020/11/06 17:18:23
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import os
import shutil
from tqdm import tqdm
import argparse
from glob import glob
import xml.etree.cElementTree as ET


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--header', help='header name')
    args = parser.parse_args()

    current_dir = os.getcwd()
    xml_lst = glob(current_dir + "/*.xml")
    img_lst = glob(current_dir + "/*.jpg")

    if len(xml_lst) == 0:
        print("没有xml...")

        for i, name in enumerate(img_lst):
            new_name = args.header + "_" + str(i) + ".jpg"
            os.rename(name, os.path.join(os.path.dirname(name), new_name))
    else:
        for i, name in enumerate(img_lst):
            new_name = args.header + "_" + str(i) + ".jpg"
            os.rename(name, os.path.join(os.path.dirname(name), new_name))
            
            xml_name = name.replace(".jpg" , ".xml")
            et = ET.parse(xml_name)
            element = et.getroot()
            
            
            element.find('filename').text = new_name
            et.write(xml_name)
            
            
            


if __name__ == '__main__':
    main()
