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
from tqdm import tqdm

def filter_xml(xml_path , usr_name):
	et = ET.parse(xml_path)
	element = et.getroot()

	dir_path = os.path.dirname(xml_path)
        newdir = os.path.join(dir_path, usr_name)
	name_lst = element.findall('usr')
	if len(name_lst) == 0:
		return
	user_name = element.find('usr').text
	if user_name == usr_name:
		element_objs = element.findall('object')
		if len(element_objs) == 2:
			class_name1 = element_objs[0].find('name').text
			class_name2 = element_objs[1].find('name').text
			if class_name1 == class_name2:
				shutil.copyfile(xml_path , newdir + "/" + os.path.basename(xml_path))
				shutil.copyfile(xml_path[:-3] + "png" , newdir + "/" + os.path.basename(xml_path)[:-3] + "png")
		else:
			shutil.copyfile(xml_path , newdir + "/" + os.path.basename(xml_path))
			shutil.copyfile(xml_path[:-3] + "png" , newdir + "/" + os.path.basename(xml_path)[:-3] + "png")
			
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--name',required=True)
	args = parser.parse_args()
	user = args.name
	
	
        newdir = os.path.join(os.getcwd(), user)
        if os.path.exists(newdir):
                shutil.rmtree(newdir)
        else:
                os.mkdir(newdir)
                pass

        if os.path.isdir(newdir):
                pass
        else:
                os.makedirs(newdir)
	
	xml_dir = os.getcwd()
	lsts = glob.glob(xml_dir + "/*.xml")
	for i in tqdm(range(len(lsts))):
		filter_xml(lsts[i] , user)
  
