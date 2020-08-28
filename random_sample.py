#coding:utf-8

import os
import random
import glob
import shutil

def random_sample(xml_path , save_path):
	sample_percent = 0.5
	total_xml = glob.glob(xml_path + "/*.xml")
	num = len(total_xml)
	lst = range(num)
	jpg_lst = glob.glob(os.getcwd() + "/*.jpg")
	png_lst = glob.glob(os.getcwd() + "/*.png")
	suffix = None
	if len(jpg_lst):
		suffix = "jpg"
	else:
		suffix = "png"

	retain_xmls = random.sample(lst , int(sample_percent * num))
	
	for i in retain_xmls:
		shutil.copyfile(total_xml[i] , os.path.join(save_path , os.path.basename(total_xml[i])))
		shutil.copyfile(total_xml[i][:-3] + suffix , os.path.join(save_path , os.path.basename(total_xml[i][:-3] + suffix)))
	
	print('finished!')


if __name__ == '__main__':
	dir_path = os.getcwd()
	retain_dir = "Retain_save"
	if os.path.isdir(retain_dir):
		pass;
	else:
		os.mkdir(retain_dir)
	random_sample(dir_path , retain_dir)

		
