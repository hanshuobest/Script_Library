# -*- coding:utf-8 -*-
# author:hanshuo

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import glob
import shutil
import imghdr
import xml.etree.cElementTree as ET
import argparse


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--suffix',required=True)
	args = parser.parse_args()
	suffix = str(args.suffix)
        aa = 0
	# 1:put all files in one dir
	for fpath , dirs , fs in os.walk(os.getcwd()):
		for f in fs:
			tmp = os.path.join(fpath , f)
			if os.path.dirname(tmp) == os.getcwd():
				continue
			if not os.path.isfile(tmp):
				continue
                        aa += 1
			if os.path.basename(tmp)[-3:] == "xml" or os.path.basename(tmp)[-3:] == suffix:
				# if aa % 10 == 0:
                                print(tmp)
				shutil.copyfile(tmp , os.getcwd() + "/" + os.path.basename(tmp))
				# os.remove(tmp)

	# 2:filter file that only have xml or png
	xml_lsts = glob.glob(os.getcwd() + "/*.xml")
	jpg_lsts = glob.glob(os.getcwd() + "/*." + suffix)

	for bmp in jpg_lsts:
		base_name = os.path.basename(bmp)[:-4]
		full_xml_name = os.path.join(os.getcwd() , base_name + ".xml")
		if os.path.exists(full_xml_name):
			continue
		else:
			print('delete the pc:%s' % (bmp))
			os.remove(bmp)
	for xml in xml_lsts:
		base_name = os.path.basename(xml)[:-4]
		full_png_name = os.path.join(os.getcwd() , base_name + "." + suffix)
		if os.path.exists(full_png_name):
			continue
		else:
			os.remove(xml)

	# 3:filter file that have errors!
	xml_lsts = glob.glob(os.getcwd() + "/*.xml")
    	for i in xml_lsts:
        	try:
            		et = ET.parse(i)
        	except:
                	os.remove(i)
                	os.remove(i[:-3] + suffix)
			print('delete the bad xml and png:' , os.path.basename(i))
    	png_lsts = glob.glob(os.getcwd() + "/*." + suffix)
    	for i in png_lsts:
        	if imghdr.what(i):
                	continue
        	else:
                	os.remove(i)
                	os.remove(i[:-3] + "xml")
                	print('delete the bad png and xml:' , os.path.basename(i))

	print('finished!')


	# 4 filter the xml that have no annotation
	xml_lsts = glob.glob(os.getcwd() + "/*.xml")
	for i in xml_lsts:
		et = ET.parse(i)
		element = et.getroot()
		element_objs = element.findall('object')
		if len(element_objs) == 0:
			os.remove(i)
			os.remove(os.path.basename(i)[:-4] + "." + suffix)	
			print('delete the xml that do not annotaion:' , os.path.basename(i))	
