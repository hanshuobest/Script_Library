
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :select_some_sku.py
@brief       :从VOC数据集中挑选指定类型的图片
@time        :2020/08/28 00:04:40
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import xml.etree.cElementTree as ET
import os
import glob
import shutil
# import click
import argparse


def filter_xml(xml_path, class_id, new_dir):
    et = ET.parse(xml_path)
    element = et.getroot()
    element_objs = element.findall('object')

    dir_path = os.path.dirname(xml_path)

    suffix = None
    if os.path.exists(os.getcwd() + "/" + os.path.basename(xml_path)[:-3] + "jpg"):
        suffix = "jpg"
    elif os.path.exists(os.getcwd() + "/" + os.path.basename(xml_path)[:-3] + "png"):
        suffix = "png"
    # print(dir_path)
    # print(os.path.basename(xml_path))

    if os.path.isdir(new_dir):
        pass
    else:
        os.makedirs(new_dir)

    names = []
    # select the classe of xml all in present_classes
    for element_obj in element_objs:
        class_name = element_obj.find('name').text
        names.append(class_name)
    d = [False for c in names if c not in class_id]
    if not d:
        print("d: " , d)
        import pdb; pdb.set_trace()
        shutil.copyfile(xml_path, new_dir + '/' + os.path.basename(xml_path))
        shutil.copyfile(data_dir + "/" + os.path.basename(xml_path)
                        [:-3] + suffix, new_dir + '/' + os.path.basename(xml_path)[:-3] + suffix)
        print('copyfile:', xml_path)


if __name__ == '__main__':
    present_classes = ['cat', 'dog', 'person',
                       'bottle', 'chair', 'pottedplant']
    data_dir = os.getcwd()
    new_dir = data_dir + '/' + str(len(present_classes)) + 'sku'

    lsts = glob.glob(data_dir + "/*.xml")
    for i in lsts:
        print('i:', i)
        filter_xml(i, present_classes, new_dir)
