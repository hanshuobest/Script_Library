# coding:utf-8

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import xml.etree.cElementTree as ET
import os
import glob
import argparse


def modify_xml(xml_path):
	try:
		et = ET.parse(xml_path)
	except:
		print('xml_path:%s' % (xml_path))
	element = et.getroot()

	element_objs = element.findall('object')
	for element_obj in element_objs:
		class_name = int(element_obj.find('name').text)
		if class_name == args.id1:
			element_obj.find('name').text = str(args.id2)
	et.write(xml_path)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('id1', type=int, help='error label')
	parser.add_argument('id2', type=int, help='right label')
	args = parser.parse_args()
	xml_lsts = glob.glob(os.getcwd() + '/*.xml')
	for i in xml_lsts:
		modify_xml(i)

