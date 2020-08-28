#coding:utf-8
'''
多进程
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import xml.etree.cElementTree as ET
import os
import glob
import shutil
import argparse
import tqdm
import multiprocessing
import math
import time

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

def process_sub(img_lsts):
	for i in img_lsts:
		et = ET.parse(i)
		element = et.getroot()
		element_objs = element.findall('object')
		
		suffix = None
		if os.path.exists(i[:-3] + "jpg"):
			suffix = "jpg"
		elif os.path.exists(i[:-3] + "png"):
			suffix = "png"
		for element_obj in element_objs:
			class_name = int(element_obj.find('name').text)
			if class_name in classes:
				new_dir = os.path.join(os.getcwd(), str(class_name) + "-sku")
				shutil.copyfile(i, new_dir + "/" + os.path.basename(i))
				shutil.copyfile(i[:-3] + suffix, new_dir + "/" + os.path.basename(i)[:-3] + suffix)
			else:
				break

if __name__ == '__main__':
	classes = [5 ,  6 ,  9 ,  10 ,  16 ,  20 ,  24 ,  30 ,  37 ,  40 ,  41 ,  42 ,  44 ,  46 ,  61 ,  63 ,  64 ,  65 ,  66 ,  67 ,  74 ,  75 ,  77 ,  78 ,  85 ,  88 ,  90 ,  91 ,  94 ,  104 ,  105 ,  122 ,  127 ,  139 ,  140 ,  141 ,  142 ,  143 ,  144 ,  145 ,  146]
	
	for i in classes:
		new_dir = str(i) + "-sku"
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
	print(len(lsts))
	
	start_time = time.time()
	
	num_process = 2
	per_count = int(math.ceil(float(len(lsts)) / num_process))
	print(per_count)
	process_lst = []
	for i in range(num_process):
		if i < num_process - 1:
			ps = multiprocessing.Process(target=process_sub , args=(lsts[i * per_count : (i + 1) * per_count] ,))
		else:
			ps = multiprocessing.Process(target=process_sub, args=(lsts[5 * per_count:] ,))
		process_lst.append(ps)
	
	for i in range(num_process):
		process_lst[i].start()
	for i in range(num_process):
		process_lst[i].join()
		
	cost_time = time.time() - start_time
	print('cost time:' , cost_time)
	
	

