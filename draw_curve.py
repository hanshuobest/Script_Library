# encoding: utf-8
# brief     :绘制cost time 和 iou之间的关系曲线
# author    :韩硕
# date      :2019-8-22


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


if __name__ == '__main__':
	cost_time = [85 , 201 , 307 , 431 , 545 , 623 , 1043]
	iou = [0.7403 , 0.8551 , 0.8876 , 0.9077 , 0.9104 , 0.920 , 0.929]

	plt.figure("cost time & iou")
	plt.xlabel(r'cost time' , fontsize = 20 , color = 'red')
	plt.ylabel(r'iou' , fontsize = 20 , color = 'red')
	plt.plot(np.array(cost_time , dtype=np.int32) , np.array(iou , np.float32) , 'g' , lw = 2)
	plt.show()

	
	
	
	
	
	
	

	









