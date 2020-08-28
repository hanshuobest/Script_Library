
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))

import darknet as dn
import pdb
import cv2
import glob
from tqdm import tqdm
import shutil
import numpy as np
import argparse
import time

classes = [2 , 3 , 4]
classes = [str(i) for i in classes]
present_classes = classes


def draw_rect(img, rst):
	if len(rst) > 0:
		cls , conf , x0 , y0 , x1 , y1 = rst[0] , rst[1] , rst[2][0] , rst[2][1] , rst[2][2] , rst[2][3]
		cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), 2)
		cv2.putText(img, str(int(cls)), (int(x0 + (x1 - x0) * 0.5 - 10 ), int(y0 + (y1 - y0) / 2)), cv2.FONT_HERSHEY_SIMPLEX,
		            0.6, (0, 0, 255), 2)
		cv2.putText(img , str(conf) , (x0 , y0 + 20) , cv2.FONT_HERSHEY_SIMPLEX , 0.5 , (0 , 255 , 0) , 1)


def calcIOU(x1, y1, w1, h1, x2, y2, w2, h2):
	'''
	
	:param x1:center_x
	:param y1:center_y
	:param w1:
	:param h1:
	:param x2:
	:param y2:
	:param w2:
	:param h2:
	:return:
	'''
	IOU = 0
	if ((abs(x1 - x2) < ((w1 + w2) / 2.0)) and (abs(y1 - y2) < ((h1 + h2) / 2.0))):
		left = max((x1 - (w1 / 2.0)), (x2 - (w2 / 2.0)))
		upper = max((y1 - (h1 / 2.0)), (y2 - (h2 / 2.0)))
		
		right = min((x1 + (w1 / 2.0)), (x2 + (w2 / 2.0)))
		bottom = min((y1 + (h1 / 2.0)), (y2 + (h2 / 2.0)))
		inter_w = abs(left - right)
		inter_h = abs(upper - bottom)
		inter_square = inter_w * inter_h
		union_square = (w1 * h1) + (w2 * h2) - inter_square
		IOU = inter_square / union_square * 1.0
	
	return IOU

def maxIou(x1, y1, w1, h1, x2, y2, w2, h2):
		# print('x1:' , x1)
		# print('y1:' , y1)
		# print('w1:' , w1)
		# print('h1:' , h1)
		# print('----------------')
		# print('x2:' , x2)
		# print('y2:' , y2)
		# print('w2:' , w2)
		# print('h2:' , h2)
		
		IOU = 0
		if ((abs(x1 - x2) < ((w1 + w2) / 2.0)) and (abs(y1 - y2) < ((h1 + h2) / 2.0))):
			left = max((x1 - (w1 / 2.0)), (x2 - (w2 / 2.0)))
			upper = max((y1 - (h1 / 2.0)), (y2 - (h2 / 2.0)))
			right = min((x1 + (w1 / 2.0)), (x2 + (w2 / 2.0)))
			bottom = min((y1 + (h1 / 2.0)), (y2 + (h2 / 2.0)))
			inter_w = abs(left - right)
			inter_h = abs(upper - bottom)
			inter_square = inter_w * inter_h
			area1 = w1 * h1
			area2 = w2 * h2
			iou1 = float(inter_square)/area1
			iou2 = float(inter_square)/area2
			# print("iou1:" , iou1)
			# print("iou2:" , iou2)
			if iou1 > iou2:
				return iou1
			else:
				return iou2
		return IOU



def readAnnotations(xml_path):
	import xml.etree.cElementTree as ET
	
	et = ET.parse(xml_path)
	element = et.getroot()
	element_objs = element.findall('object')
	
	results = []
	for element_obj in element_objs:
		result = []
		class_name = element_obj.find('name').text
		obj_bbox = element_obj.find('bndbox')
		x1 = int(round(float(obj_bbox.find('xmin').text)))
		y1 = int(round(float(obj_bbox.find('ymin').text)))
		x2 = int(round(float(obj_bbox.find('xmax').text)))
		y2 = int(round(float(obj_bbox.find('ymax').text)))
		
		result.append(class_name)
		result.append(x1)
		result.append(y1)
		result.append(x2)
		result.append(y2)
		
		results.append(result)
	return results


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--cfg" , required=True)
	parser.add_argument("--model" , required=True)
	args = parser.parse_args()	
	
	dn.set_gpu(0)

	net = dn.load_net(args.cfg, args.model, 0)
	meta = dn.load_meta("cfg/voc.data")
	for i in range(meta.classes):
		print(meta.names[i])
		
	test_path = "/home/han/darknet/test_data"
	result_path = "data/result"
	if os.path.exists(result_path):
		shutil.rmtree(result_path)
	else:
		os.mkdir(result_path)

	
	if not os.path.isdir(result_path):
		os.mkdir(result_path)
	no_detect_dir = os.path.join(result_path , "no_detect")
	if os.path.exists(no_detect_dir):
		shutil.rmtree(no_detect_dir)
	else:
		os.mkdir(no_detect_dir)
	
	jpg_lsts = glob.glob(test_path + "/*.jpg")
	num_imgs = len(jpg_lsts)
	assert num_imgs !=  0
	
	detect_all_boxes = {}
	gt_all_boxes = {}
	

	for i in range(len(classes)):
		detect_all_boxes[classes[i]] = []
		# gt_all_boxes[classes[i]] = []
	
	
	
	for i in tqdm(range(num_imgs)):
		img_name = jpg_lsts[i]
		print('img_name:' , img_name)
		if not os.path.exists(img_name):
			print('%s not exist!' % (img_name))
			continue
		
		img = cv2.imread(img_name)
		
		# detect result
		start_time = time.time()
		detect_results = dn.detect(net , meta , img_name , 0.5 , 0.5 , 0.35)


		if len(detect_results) == 0:
			print('%s:%s' % ("The image do not detect any sku"  , os.path.basename(img_name)))
			shutil.copyfile(img_name , no_detect_dir + "/" + os.path.basename(img_name))
			continue
		
		for detect_result in detect_results:
			draw_rect(img , detect_result)
		
		
		cv2.imwrite(result_path + "/" + os.path.basename(img_name)[:-4] + ".jpg" , img)
	

