# coding:utf-8
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :change_label2.py
@brief       :
@time        :2020/08/27 15:45:32
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''



import sys

reload(sys)
sys.setdefaultencoding('utf8')

import xml.etree.cElementTree as ET
import os
import glob
import argparse

map_dict = {'1':'head' , '2':'hand' , 'head':'head' , 'hand':'hand' , '3':'person' , 'person':'person'}

def modify_xml(xml_path):
	try:
		et = ET.parse(xml_path)
	except:
		print('xml_path:%s' % (xml_path))
	element = et.getroot()

	element_objs = element.findall('object')
	for element_obj in element_objs:
		class_name = element_obj.find('name').text
		element_obj.find('name').text = map_dict[class_name]
		#if class_name == args.id1:
		#	element_obj.find('name').text = str(args.id2)
	et.write(xml_path)


if __name__ == '__main__':
	xml_lsts = glob.glob(os.getcwd() + '/*.xml')
	for i in xml_lsts:
		modify_xml(i)

