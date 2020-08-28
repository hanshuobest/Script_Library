#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import glob
import os
import xml.etree.cElementTree as ET
import argparse
import shutil
import multiprocessing
import math
import time

def process_sub(dir_lst):
	for i in dir_lsts:
		if os.path.isdir(i):
			xml_lsts = glob.glob(os.path.join(os.getcwd(), i) + "/*.xml")
			jpg_lsts = glob.glob(os.path.join(os.getcwd(), i) + "/*.jpg")
			png_lsts = glob.glob(os.path.join(os.getcwd(), i) + "/*.png")
			suffix = None
			if len(jpg_lsts):
				suffix = "jpg"
				assert len(jpg_lsts) == len(xml_lsts)
			else:
				suffix = "png"
				assert len(png_lsts) == len(xml_lsts)

			id = i.split("-")[0]
			index = 0
			for j in xml_lsts:
				try:
					et = ET.parse(j)
				except:
					continue
				
				element = et.getroot()
				element_objs = element.findall('object')
				for element_obj in element_objs:
					class_name = element_obj.find('name').text
					if class_name == id:
						index += 1
						continue
					else:
						element.remove(element_obj)
				new_xml_name = os.path.basename(j)[:-4] + "-" + str(id) + ".xml"
				new_img_name = os.path.basename(j)[:-4] + "-" + str(id) + "." + suffix
				if index <= num:
					et.write(new_xml_name)
					shutil.copyfile(j[:-3] + suffix, new_img_name)
			# shutil.rmtree(i)
		else:
			continue

if __name__ == '__main__':
	num = 400
	dir_lsts = os.listdir(os.getcwd())
	dir_lsts = [i for i in dir_lsts if os.path.isdir(i)]
	process_lst = []
	num_process = 4
	
	start_time = time.time()
	per_count = int(math.ceil(float(len(dir_lsts)) / num_process))
	for i in range(num_process):
		if i < num_process - 1:
			ps = multiprocessing.Process(target=process_sub , args=(dir_lsts[i * per_count: (i + 1) * per_count] ,))
		else:
			ps = multiprocessing.Process(target=process_sub , args=(dir_lsts[i * per_count:] ,))
		process_lst.append(ps)
	
	for i in range(num_process):
		process_lst[i].start()
	for i in range(num_process):
		process_lst[i].join()
	
	cost_time = time.time() - start_time
	print('cost time:' , cost_time)
	

