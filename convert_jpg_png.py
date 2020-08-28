#coding:utf-8
import cv2
import glob
import os 
import tqdm
jpg_lst = glob.glob(os.getcwd() + "/*.jpg")
print(len(jpg_lst)) 
for i in tqdm.tqdm(range(len(jpg_lst))):
	img = cv2.imread(jpg_lst[i])
	if type(img) == type(None):
		print('read pic failture!')
		break
	cv2.imwrite(jpg_lst[i][:-3] + "png" , img)
	os.remove(jpg_lst[i])

print('finished!')
