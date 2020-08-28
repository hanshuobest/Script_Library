#coding:utf-8
import os
import glob
import sys

png_lst = glob.glob(os.getcwd() + "/*.png")
for i in png_lst:
	new_image_name = os.path.basename(i).split('-')[0] + "-" +  str(int(os.path.basename(i).split('-')[1][:-4]) + 20) + ".png"
	cmd = 'mv ' + i + " " + os.path.join(os.getcwd() , new_image_name)
	print(cmd)
	os.system(cmd)

xml_lst = glob.glob(os.getcwd() + "/*.json")
for i in xml_lst:
	new_xml_name = os.path.basename(i).split('-')[0] + "-" + str(int(os.path.basename(i).split('-')[1][:-5]) + 20) + ".json"
	print('xml:' , new_xml_name)
	cmd = 'mv ' + i + " " + os.path.join(os.getcwd() , new_xml_name)
	os.system(cmd)
 
