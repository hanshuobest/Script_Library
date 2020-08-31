# coding:utf-8
# 脚本描述
# 删除xml中的指定节点

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :delete_xml_node.py
@brief       :删除xml中无需的类别信息
@time        :2020/08/28 00:40:31
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import os
import glob
import xml.etree.cElementTree as ET

def filter_xml(xml_path , present_classes):
    et = ET.parse(xml_path)
    root = et.getroot()
    element_objs = root.findall('object')
    if len(element_objs) == 0:
        os.remove(xml_path)
        
    for obj in element_objs:
        class_name = obj.find('name').text
        if class_name not in present_classes:
            root.remove(obj)
    et.write(xml_path , xml_declaration=True)
            
            

if __name__ == '__main__':
    present_classes = ['cat', 'dog', 'person',
                       'bottle', 'chair', 'pottedplant']
    data_dir = os.getcwd()
    xml_lsts = glob.glob(data_dir + "/*.xml")
    for xml in xml_lsts:
        filter_xml(xml, present_classes)
    
    
    
