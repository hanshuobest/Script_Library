#coding:utf-8
import glob
import os
import argparse

if __name__=='__main__':
	xml_lsts = glob.glob(os.getcwd() + "/*.xml")
	jpg_lsts = glob.glob(os.getcwd() + "/*.jpg")

	for xml in xml_lsts:
        	jpg_name = xml[:-4] +  ".jpg"
        	if os.path.exists(jpg_name):
                	continue
        	else:
                	print('delete the xml:%s' %(xml))
                	os.remove(xml)
	for jpg in jpg_lsts:
		xml_name = jpg[:-4] + ".xml"
		if os.path.exists(xml_name):
			continue
		else:
			os.remove(jpg)
