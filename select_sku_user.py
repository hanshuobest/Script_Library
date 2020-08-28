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
	user_name = element.find('usr').text
	if user_name == usr_name:
		shutil.copyfile(xml_path , newdir + "/" + os.path.basename(xml_path))
		shutil.copyfile(xml_path[:-3] + "png" , newdir + "/" + os.path.basename(xml_path)[:-3] + "png")
		
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--name')
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
  
