# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import glob
import shutil
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--iter")
	args = parser.parse_args()
	
	iters = int(args.iter)
	xml_lsts = glob.glob(os.getcwd() + "/*.xml")
	num_xml = len(xml_lsts)
	for i in range(1 , iters):
		for j in range(num_xml):
			new_xml_name = os.getcwd() + "/" + os.path.basename(xml_lsts[j])[:-4] + "-copy-" + str(i) + ".xml"
			new_png_name = os.getcwd() + "/" + os.path.basename(xml_lsts[j])[:-4] + "-copy-" + str(i) + ".png"
			png_name = os.getcwd() + "/" + os.path.basename(xml_lsts[j])[:-4] + ".png"
			shutil.copyfile(xml_lsts[j] , new_xml_name)
			shutil.copyfile(png_name , new_png_name)
			
			print(new_xml_name)
			
		
