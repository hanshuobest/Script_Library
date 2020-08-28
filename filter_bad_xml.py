#coding:utf-8
# 过滤掉损坏掉的xml和与之对应的png


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import glob
import shutil
import xml.etree.cElementTree as ET
import cv2
import imghdr

if __name__ == '__main__':
    xml_lsts = glob.glob(os.getcwd() + "/*.xml")
    for i in xml_lsts:
        try:
            et = ET.parse(i)
        except:
	        os.remove(i)
	        os.remove(i[:-3] + "png")
    png_lsts = glob.glob(os.getcwd() + "/*.png")
    for i in png_lsts:
	if imghdr.what(i):
		continue
	else:
		os.remove(i)
		os.remove(i[:-3] + "xml")
		print('delete the bad png and xml:' , os.path.basename(i))

	    
		
		
