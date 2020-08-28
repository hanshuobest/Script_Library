# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 将连续的图片另存为视频

import cv2
import glob
import os
from tqdm import tqdm


fps = 25

for i in range(6):
	video_dir = str(i) + ".avi"
	img_dir = os.path.join(os.getcwd() , str(i))
	img_lsts = glob.glob(img_dir + "/*.jpg")

	name_lst = []
	for j in img_lsts:
		split_num = int(os.path.basename(j)[:-4].split('_')[1])
		name_lst.append(split_num)
	
	name_lst.sort()
	print(name_lst)

	img_0 = cv2.imread(img_lsts[0])
	h , w , _ = img_0.shape
	img_size = (w , h)
	print(img_size)



	fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
	videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)

	for k in tqdm(range(len(name_lst))):
	
		img = cv2.imread(os.path.join(img_dir ,str(i) + "_" + str(name_lst[k]) + ".jpg"))
		if type(img) == type(None):
			print('read image failture!')
			break

		videoWriter.write(img)

	videoWriter.release()
	print('finished!')
