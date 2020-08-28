
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF , renderPM
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
import imutils
from imutils.paths import list_images
import os
import pandas as pd

def count_match(image):
	height , width = image.shape[:2]
	real_img_height = int(height/5) - 3
	
	count_result = []
	for i in range(real_img_height):
		count_result.append(cv2.countNonZero(image[i * 5, :]) /2)
		# print('index:{} --->{}'.format(i , cv2.countNonZero(image[i * 5, :]) /2))
	return count_result



if __name__ == '__main__':
	svg_dir = "/home/han/Company_project/3D-platform/data_collection_dir/svg"
	svg_img_lsts = list(list_images(svg_dir))
	print(svg_img_lsts)
	
	xmax = 0
	statistic_results = []
	for i in svg_img_lsts:
		img = cv2.imread(i)
		_ , binary = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
		count_result = count_match(binary)
		if xmax < len(count_result):
			xmax = len(count_result)
		
		statistic_results.append(count_result)
		
	plt.figure('statistic distribution')

	mean_val = []
	ax1 = plt.subplot(3, 1, 1)
	ax1.set_title("distribution curve")
	ax2 = plt.subplot(3, 1, 2)
	ax2.set_title('per shop mean value')
	ax3 = plt.subplot(3, 1, 3)
	ax3.set_title('all shop mean value')
	plt.sca(ax1)

	l = []
	labels = []
	colors = ['b' , 'g' , 'r' , 'c' , 'm']
	for i , result in enumerate(statistic_results):
		x = np.arange(len(result))
		l_tmp = plt.plot(x , np.array(result , dtype=np.int32) , colors[i] , lw = 2)
		l.append(l_tmp)
		labels.append(os.path.basename(svg_img_lsts[i])[:-4])

		mean_val.append(np.mean(np.array(result , dtype=np.int32)))
	
	plt.legend(l , labels = labels , loc = 'best')
	w = pd.Series(mean_val , index=labels)
	plt.sca(ax2)
	plt.bar(labels , mean_val)

	labels = ['total_mean']
	total_mean = np.mean(mean_val)
	w_mean = pd.Series(total_mean , index=labels)
	plt.sca(ax3)
	plt.bar(labels , total_mean)

	plt.show()

	
	
	
	
	
	
	

	









