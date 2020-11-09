#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :modify_xml_annotation.py
@brief       :修改所有图片的分辨率，以及xml信息
@time        :2020/10/26 16:27:54
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import xml.etree.cElementTree as ET
import os
import glob
import argparse
import cv2
import sys


resolution = [720, 1280]


def modify_xml(xml_path):
    et = ET.parse(xml_path)
    element = et.getroot()
    
    

    image_name = xml_path.replace(".xml", ".jpg")
    if not os.path.exists(image_name):
        image_name = xml_path.replace(".xml", ".png")

    img = cv2.imread(image_name)
    src_h, src_w = img.shape[:2]

    resize_img = cv2.resize(img, (resolution[1], resolution[0]))
    cv2.imwrite(image_name, resize_img)

    size_obj = element.find('size')
    size_obj.find('width').text = str(resolution[1])
    size_obj.find('height').text = str(resolution[0])

    height_r = resolution[0]/src_h
    width_r = resolution[1]/src_w

    element_objs = element.findall('object')
    for element_obj in element_objs:
        xmin = int(element_obj.find('bndbox').find('xmin').text)
        ymin = int(element_obj.find('bndbox').find('ymin').text)
        xmax = int(element_obj.find('bndbox').find('xmax').text)
        ymax = int(element_obj.find('bndbox').find('ymax').text)

        element_obj.find('bndbox').find('xmin').text = str(int(xmin * width_r))
        element_obj.find('bndbox').find(
            'ymin').text = str(int(ymin * height_r))
        element_obj.find('bndbox').find('xmax').text = str(int(xmax * width_r))
        element_obj.find('bndbox').find(
            'ymax').text = str(int(ymax * height_r))

    et.write(xml_path)


if __name__ == '__main__':
    current_dir = os.getcwd()
    xml_lsts = glob.glob(current_dir + "/*.xml")
    for xml_name in xml_lsts:
        print(xml_name)
        modify_xml(xml_name)
