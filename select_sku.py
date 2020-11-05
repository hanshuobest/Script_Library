#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import xml.etree.cElementTree as ET
import os
import glob
import shutil
import argparse

def filter_xml(xml_path , class_id , newdir):
	et = ET.parse(xml_path)
	element = et.getroot()
	element_objs = element.findall('object')
	
	suffix = None
	if os.path.exists(xml_path[:-3] + "jpg"):
		suffix = "jpg"
	elif os.path.exists(xml_path[:-3] + "png"):
		suffix = "png"
	
	jpg_dir = os.path.dirname(xml_path)
	
	for element_obj in element_objs:
		class_name = element_obj.find('name').text
		if class_name == class_id:
			shutil.copyfile(xml_path , newdir + '/' + os.path.basename(xml_path))
			shutil.copyfile(xml_path[:-3] + suffix , newdir + '/' + os.path.basename(xml_path)[:-3] + suffix)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	# parser.add_argument('--year')
	parser.add_argument('-l' , '--label')
	args = parser.parse_args()
	id = str(args.label)
	new_dir = id + "-sku"
	if os.path.exists(new_dir):
		shutil.rmtree(new_dir)
	else:
		os.mkdir(new_dir)
	if os.path.isdir(new_dir):
		pass
	else:
		os.mkdir(new_dir)
		
	
	xml_dir = os.getcwd()
	lsts = glob.glob(xml_dir + "/*.xml")
	for i in lsts:
		print('i:' , i)
		filter_xml(i , id , new_dir)
  
