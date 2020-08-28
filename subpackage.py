#coding:utf-8
'''
save every 100 pictures in a folder
'''

import os
import time
import datetime
import glob
import shutil
def TimeStampToTime(timestamp):
	timeStruct = time.localtime(timestamp)
	return time.strftime('%Y-%m-%d',timeStruct)


def get_FileCreateTime(filePath):
	filePath = unicode(filePath,'utf8')
	t = os.path.getctime(filePath)
	return TimeStampToTime(t)
	# return t


if __name__ == '__main__':
	dir_path = "/media/han/DATA/paimian"
	img_lsts = glob.glob(dir_path + "/*.jpg")
	img_lsts = sorted(img_lsts , key=lambda x : os.path.getmtime(x) , reverse=True)
	
	for i , fname in enumerate(img_lsts):
		if i %100 == 0:
			os.mkdir(os.path.join(dir_path , str(i/100)))
		shutil.move(fname , os.path.join(dir_path , str(i/100) , os.path.basename(fname)))