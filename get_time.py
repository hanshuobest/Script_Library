#coding:utf-8
# 通过文件时间筛选文件到指定位置
# useage
# python get_time.py --to dst
import os
import datetime
import time
import argparse

# '''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
	timeStruct = time.localtime(timestamp)
	return time.strftime('%Y-%m-%d',timeStruct)


def get_FileCreateTime(filePath):
	filePath = unicode(filePath,'utf8')
	t = os.path.getctime(filePath)
	# return TimeStampToTime(t)
	return t
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--to')
	args = parser.parse_args()
	
	from_dir = os.getcwd()
	to_dir = args.to
	
	dir_lsts = [os.path.join(from_dir , i) for i in os.listdir(from_dir) if os.path.isdir(i)]
	for dl in dir_lsts:
		g_time = get_FileCreateTime(dl)
		if g_time == "2018-09-05":
			shell_script = "mv " + dl + " " + to_dir
			os.system(shell_script)
			print(shell_script)
			


		
		

