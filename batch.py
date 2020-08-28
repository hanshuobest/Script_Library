#coding:utf-8

import os
import glob
import shutil

if __name__ == '__main__':
	batch_num = 500
	batch_index = 0
	root_dir = "/home/han/ABdarknet/darknet/detect_result"
	jpg_lsts = glob.glob(root_dir + "/*.jpg")
	for i_index , img in enumerate(jpg_lsts):
		print(i_index)
		#img = xml.replace("xml" , "jpg")
		batch_index = i_index/batch_num
		if os.path.exists(os.path.join(root_dir , str(batch_index))):
			pass
		else:
			os.mkdir(os.path.join(root_dir , str(batch_index)))
		#shutil.move(xml, os.path.join(root_dir, str(batch_index), os.path.basename(xml)))
		shutil.move(img, os.path.join(root_dir, str(batch_index), os.path.basename(img)))

	
		
		

		
		
		

