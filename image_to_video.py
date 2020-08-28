# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 将连续的图片另存为视频

import cv2
import glob
import os
from tqdm import tqdm


img_dir = os.getcwd()
file_id = 0
video_dir = str(0) + ".avi"
fps = 25

img_lsts = glob.glob(img_dir + "/*.jpg")
# print(img_lsts)


name_lst = []
for i in img_lsts:
	split_num = int(os.path.basename(i)[:-4].split('_')[1])
	# print(split_num)
	name_lst.append(split_num)
	
name_lst.sort()
print(name_lst)

img_0 = cv2.imread(img_lsts[0])
h , w , _ = img_0.shape
img_size = (w , h)
print(img_size)



fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)

for i in tqdm(range(len(name_lst))):
	
	img = cv2.imread(os.path.join(img_dir ,str(file_id) + "_" + str(name_lst[i]) + ".jpg"))
	if type(img) == type(None):
		print('read image failture!')
		break

	videoWriter.write(img)

videoWriter.release()
print('finished!')
