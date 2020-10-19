#coding:utf-8
import glob
import os
import argparse

if __name__=='__main__':
	json_lsts = glob.glob(os.getcwd() + "/*.json")
	jpg_lsts = glob.glob(os.getcwd() + "/*.jpg")

	for json in json_lsts:
        	jpg_name = json[:-5] +  ".jpg"
        	if os.path.exists(jpg_name):
                	continue
        	else:
                	print('delete the json:%s' %(json))
                	os.remove(json)
	for jpg in jpg_lsts:
		json_name = jpg[:-4] + ".json"
		if os.path.exists(json_name):
			continue
		else:
                        print(jpg)
                        os.remove(jpg)
