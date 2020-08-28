#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import xml.etree.cElementTree as ET
import os
import glob
import shutil
import tqdm



one_dir = "one_object"
two_dir = "two_object"

if os.path.exists(one_dir):
	shutil.rmtree(one_dir)
else:
	pass

if os.path.exists(two_dir):
	shutil.rmtree(two_dir)
else:
	pass


if os.path.isdir(one_dir):
	pass
else:
	os.mkdir(one_dir)
if os.path.isdir(two_dir):
	pass
else:
	os.mkdir(two_dir)

xml_lst = glob.glob(os.getcwd() + "/*.xml")
for i in tqdm.tqdm(range(len(xml_lst))):
	et = ET.parse(xml_lst[i])
	element = et.getroot()
	element_objs = element.findall('object')
	if len(element_objs) == 1:
		shutil.copyfile(xml_lst[i] , one_dir + "/" + os.path.basename(xml_lst[i]))
		shutil.copyfile(xml_lst[i][:-3] + "png" , one_dir + "/" + os.path.basename(xml_lst[i])[:-3] + "png")
	elif len(element_objs) == 2:
		shutil.copyfile(xml_lst[i] , two_dir + "/" + os.path.basename(xml_lst[i]))
                shutil.copyfile(xml_lst[i][:-3] + "png" , two_dir + "/" + os.path.basename(xml_lst[i])[:-3] + "png")

print('finished!')




