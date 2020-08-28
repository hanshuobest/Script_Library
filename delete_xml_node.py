#coding:utf-8
# 脚本描述
# 删除xml中的指定节点

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import glob
import xml.etree.cElementTree as ET


xml_lsts = glob.glob(os.getcwd() + "/*.xml")

for i in xml_lsts:
	et = ET.parse(i)
	root = et.getroot()
	element_objs = root.findall('object')
	if len(element_objs) == 0:
		os.remove(i)
	
	element_width = int(root.find('size').find('width').text)
	element_height = int(root.find('size').find('height').text)
	
	if element_width == 0 or element_height == 0:
		os.remove(i)
	
	for element_obj in element_objs:
		xmin = int(element_obj.find('bndbox').find('xmin').text)
		ymin = int(element_obj.find('bndbox').find('ymin').text)
		xmax = int(element_obj.find('bndbox').find('xmax').text)
		ymax = int(element_obj.find('bndbox').find('ymax').text)
		
		if (xmax - xmin) * (ymax - ymin) <= 6400 or (xmax - xmin) <= 50 or (ymax - ymin) <= 50:
			print(i)
			root.remove(element_obj)
	
	et.write(i , xml_declaration=True)





