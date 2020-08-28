#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import glob
import shutil
import argparse
from tqdm import tqdm
import xml.etree.cElementTree as ET


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--num')
	args = parser.parse_args()
	num = int(args.num)
	print('num:' , num)
	
	
	sku_dicts = {}
	sku_lst = ['5', '6', '9', '10', '11', '20', '24', '26', '30', '37', '40','41', '42', '44', '46', '61', '63', '64', '65',
            '66', '67', '74', '75', '77', '78', '85', '88', '90', '91', '104', '105']
	
	xml_lsts = glob.glob(os.getcwd() + "/Annotations/*.xml")
	suffix = None
	if os.path.exists(os.getcwd() + "/JPEGImages/" + os.path.basename(xml_lsts[0])[:-3] + "jpg"):
		suffix = "jpg"
	elif os.path.exists(os.getcwd() + "/JPEGImages/" + os.path.basename(xml_lsts[0])[:-3] + "png"):
		suffix = "png"
	
	new_dir = os.path.join(os.getcwd() , str(len(sku_lst)) + "sku")
	if os.path.exists(new_dir):
		shutil.rmtree(new_dir)
	else:
		os.mkdir(new_dir)
		
	if os.path.isdir(new_dir):
		pass
	else:
		os.mkdir(new_dir)
		
	
	num_images = len(xml_lsts)
	for i in tqdm(range(num_images)):
		et = ET.parse(xml_lsts[i])
		element = et.getroot()
		try:
			user_name = element.find('usr').text
			if user_name == "auto":
				continue
		except:
			pass
		element_objs = element.findall('object')
		
		tmp = []
		for element_obj in element_objs:
			class_name = element_obj.find('name').text
			if class_name not in sku_lst:
				break
			tmp.append(class_name)
		
		if len(tmp) != len(element_objs):
			continue	
		for element_obj in element_objs:
			class_name = element_obj.find('name').text
			if sku_dicts.has_key(class_name):
				sku_dicts[class_name] += 1
			else:
				sku_dicts[class_name] = 1
		flag = [True for t in range(len(tmp))]
		for index , j in enumerate(tmp):
			# print(sku_dicts[j])
			if sku_dicts[j] > num:
				# print('fuck:' , sku_dicts[j])
				flag[index] = False
				break
		if False not in flag:
			# print(xml_lsts[i])
			shutil.copyfile(xml_lsts[i], new_dir + "/" + os.path.basename(xml_lsts[i]))
			shutil.copyfile(os.getcwd() + "/JPEGImages/" + os.path.basename(xml_lsts[0])[:-3] + suffix , new_dir + "/" + os.path.basename(xml_lsts[i])[:-3] + suffix)
		
		
		# print(xml_lsts[i])
	print(sku_dicts)
