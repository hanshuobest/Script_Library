#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import xml.etree.cElementTree as ET
import os
import glob
import shutil
# import click
import argparse



def filter_xml(xml_path , class_id, new_dir):
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
		class_name = int(element_obj.find('name').text)
		names.append(class_name)
	d = [False for c in names if c not in class_id]
	if not d:
		shutil.copyfile(xml_path , new_dir + '/' + os.path.basename(xml_path))
		shutil.copyfile(data_dir + "/" + os.path.basename(xml_path)[:-3] + suffix , new_dir + '/' + os.path.basename(xml_path)[:-3] + suffix)
		print('copyfile:',xml_path)
		
if __name__ == '__main__':
	#parser = argparse.ArgumentParser()
	#parser.add_argument('--id')
	#args = parser.parse_args()
	#id = str(args.id)
	
	# select the sku in present_classes
	present_classes = [5 ,  6 ,  9 ,  10 ,  16 ,  20 ,  24 ,  30 ,  37 ,  40 ,  41 ,  42 ,  44 ,  46 ,  61 ,  63 ,  64 ,  65 ,  66 ,  67 ,  74 ,  75 ,  77 ,  78 ,  85 ,  88 ,  90 ,  91 ,  94 ,  104 ,  105 ,  122 ,  127 ,  139 ,  140 ,  141 ,  142 ,  143 ,  144 ,  145 ,  146]	
	#present_classes = ['5', '6', '9', '37', '61']	
	data_dir = os.getcwd()
	new_dir = data_dir + '/' + str(len(present_classes)) + 'sku' 
	
	#xml_dir = os.getcwd()
	lsts = glob.glob(data_dir + "/*.xml")
	for i in lsts:
		print('i:' , i)
		filter_xml(i ,present_classes, new_dir)
  
