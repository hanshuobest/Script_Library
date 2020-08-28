
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
import argparse, xlwt


# 99 classes
# classes = ['5', '6', '9', '10', '11', '16', '20', '22', '24', '26', '30', '33', '35', '37', '39', '40', '41', '42', '44', '46', '61', '63', '64', '65', '66', '67', '72', '73', '74', '75', '77', '78', '82', '83', '84', '85', '86', '88', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '104', '105', '106', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159']

# present_classes = [5,6,9,16,22,26,30,33,39,40,46,61,67,73,74,75,82,84,85,86,90,94,96,97,104,105,106,115,116,117,118,120,121,122,124,126,127,128,129,133,135,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159]
# present_classes = [str(x) for x in present_classes]

# 35 classes
# classes = [5 ,  6 ,  9 , 16 ,  30 ,  37 ,  40 ,  42 ,  44 ,  46 ,  61 ,  65 ,  66 ,  67 ,  74 ,  75 ,  77 ,  78 ,  85 ,  88 ,  90 ,  91 ,  94 ,  104 ,  105 ,  122 ,  127 ,  139 ,  140 ,  141 ,  142 ,  143 ,  144 ,  145 ,  146]

#classes = [5, 30, 39, 40, 41, 42, 67, 95, 96, 97, 105, 119, 121, 123, 133]
#classes = [str(i) for i in classes]
classes = [str(i) for i in range(2 , 82)]
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
	# net = dn.load_net("cfg/yolov3-tiny.cfg", "/home/han/darknet/yolov3_final.weights", 0)
	# meta = dn.load_meta("cfg/voc.data")

	net = dn.load_net(args.cfg, args.model, 0)
	meta = dn.load_meta("cfg/voc.data")
	for i in range(meta.classes):
		print(meta.names[i])

	test_path = "/home/han/Desktop/test_20190319"
	confidence = 0.8
	iou_threshold = 0.45
	save_groundTruth =False #False
	
	list1 = glob.glob(test_path + "/*.jpg")
	list2 = glob.glob(test_path + "/*.png")
	# auto choice image format
	if len(list1) == 0 and len(list2) != 0:
		suffix = ".png"
	elif len(list1) != 0 and len(list2) == 0:
		suffix = ".jpg"
	elif len(list1) == 0 and len(list2) == 0:
		print("There are no images in folder: %s" % test_path)
		os._exit(0)
	else:
		print("Don't put JPG and PNG in a folder at the same time...")
		os._exit(0)
	book = xlwt.Workbook(encoding='utf-8',style_compression=0)
	sheet = book.add_sheet('mysheet',cell_overwrite_ok=True)
	result_name = 'sku_result_' + str(confidence)
	f = open(result_name+'.txt', 'w')
	conf = 'confidence: ' + str(confidence)
	sheet.write(0, 0, 'confidence:')
	sheet.write(0, 1, confidence)
	f.write(conf + '\n')
	f.write('classes' + '\t' +'    '+ 'precision' + '\t' +'    '+ 'recall')
	f.write('\n')
	rc, ac= [], []
	sheet.write(1, 0, 'classes')
	sheet.write(1, 1, 'precision')
	sheet.write(1, 2, 'recall')
	result_path = "data/result_" + str(confidence)
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
	
	xml_lsts = glob.glob(test_path + "/*.xml")
	num_imgs = len(xml_lsts)
	assert num_imgs !=  0
	
	detect_all_boxes = {}
	gt_all_boxes = {}
	back_all_boxes = {}
	error_matrix = np.zeros(shape=(len(classes) , len(classes)) , dtype=np.float32)

	for i in range(len(classes)):
		detect_all_boxes[classes[i]] = []
		gt_all_boxes[classes[i]] = []
	
	
	
	for i in tqdm(range(num_imgs)):
		img_name = test_path + "/" + os.path.basename(xml_lsts[i])[:-4] + suffix
		print('img_name:' , img_name)
		if not os.path.exists(img_name):
			print('%s not exist!' % (img_name))
			continue
		
		img = cv2.imread(img_name)
		if type(img) == type(None):
			continue
		
		# ground truth
		reuslts = readAnnotations(xml_lsts[i])
		for result in reuslts:
			try:
				cls = result[0]
				if cls in classes:
					gt_all_boxes[cls].append(
						(os.path.basename(xml_lsts[i])[:-4], result[1], result[2], result[3], result[4]))
					cv2.rectangle(img, (result[1], result[2]), (result[3], result[4]), (255, 0, 0), 2)
					cv2.putText(img, str(result[0]), (
						int(result[1] + (result[3] - result[1]) / 3), int(result[2] + (result[4] - result[2]) / 2)),
					            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
			except:
				print('result:', result)
		
		# detect result
		detect_results = dn.detect(net , meta , img_name , confidence , 0.5 , 0.45)

		if len(detect_results) == 0:
			print('%s:%s' % ("The image do not detect any sku"  , os.path.basename(img_name)))
			shutil.copyfile(xml_lsts[i] , no_detect_dir + "/" + os.path.basename(xml_lsts[i]))
			shutil.copyfile(img_name , no_detect_dir + "/" + os.path.basename(img_name))
			# continue
		
		for detect_result in detect_results:
			draw_rect(img , detect_result)
			cls = detect_result[0]
			if cls not in classes:
				continue
			conf = detect_result[1]
			box = detect_result[2]
			
			back_flag = False
			iou_tmp = np.zeros(len(reuslts))
			cls_tmp = None
			i_flag = 0
			for result in reuslts:
				iou = calcIOU((box[0] + box[2]) * 0.5, (box[1] + box[3]) * 0.5, box[2] - box[0], box[3] - box[1], (result[1] + result[3]) * 0.5, (result[2] + result[4]) * 0.5, result[3] - result[1],
				              result[4] - result[2])
				if iou == 0:
					iou_tmp[i_flag] = 1
				elif iou > 0.5:
					if cls != result[0]:
						print('iou:' , iou)
						print('%s -> %s' % (result[0] , cls))
						error_matrix[classes.index(result[0])][classes.index(cls)] += 1
						
				i_flag += 1
			
			if np.sum(iou_tmp) == len(reuslts):
				back_flag = True
				
				
			
			if not back_flag:
				detect_all_boxes[cls].append((os.path.basename(img_name)[:-4] , box[0] , box[1] , box[2] , box[3]))
				cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
				cv2.putText(img, str(int(cls)), (int(box[0] + (box[2] - box[0]) * 0.5 - 10), int(box[1] + (box[3] - box[1]) * 0.5)),
				            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
			else:
				if back_all_boxes.has_key(cls):
					back_all_boxes[cls] += 1
				else:
					back_all_boxes[cls] = 1
				
				# print('background image:' , img_name)
		
		cv2.imwrite(result_path + "/" + os.path.basename(img_name)[:-4] + suffix , img)
	
	back_all_boxes = sorted(back_all_boxes.items() , key= lambda item:item[1] , reverse=True)
	
	
	print('%s：' % ('背景误识别率'))
	print(back_all_boxes)
	
	index = np.where(error_matrix > 5)
	print(index)
	print('----------------------------------------')
	for i in range(len(index[0])):
		print('the class of %s is recognized as %s | total num: %d  | percent:%f' % (classes[index[0][i]] , classes[index[1][i]] , error_matrix[index[0][i]][index[1][i]] , float(error_matrix[index[0][i]][index[1][i]])/(len(gt_all_boxes[classes[index[0][i]]]))))
	print('----------------------------------------')

	sum_pos = 0
	sum_nd = 0
	sum_tp = 0
	sum_fp = 0
	line_num = 2
	for i in tqdm(range(0 , len(classes))):
		print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
		print('detect ', classes[i])
		
		if not os.path.isdir(result_path + "/" + classes[i]):
			os.mkdir(os.path.join(result_path , classes[i]))
		
		save_dir_class_pos = os.path.join(result_path , classes[i] , "pos")
		save_dir_class_neg = os.path.join(result_path , classes[i] , "neg")
		save_dir_class_groundTruth = os.path.join(result_path , classes[i] , "groundTruth")

		if os.path.exists(save_dir_class_pos):
			shutil.rmtree(save_dir_class_pos)
		os.mkdir(save_dir_class_pos)
		
		if os.path.exists(save_dir_class_neg):
			shutil.rmtree(save_dir_class_neg)
		os.mkdir(save_dir_class_neg)

		if os.path.exists(save_dir_class_groundTruth):
			shutil.rmtree(save_dir_class_groundTruth)
		os.mkdir(save_dir_class_groundTruth)
		
		
		# 该类商品在label中出现的次数
		npos = len(gt_all_boxes[classes[i]])
		# 该类商品检测出现的次数
		nd = len(detect_all_boxes[classes[i]])
		print('npos:', npos)
		print('nd:', nd)
		
		sum_pos += npos
		sum_nd += nd
		
		BB_name = [[j for j in x] for x in detect_all_boxes[str(classes[i])]]
		BBGT_name = [[j for j in x] for x in gt_all_boxes[str(classes[i])]]
			
		tp = np.zeros(nd)
		fp = np.zeros(nd)
		npos_flag = np.zeros(npos)
		for d in range(nd):
			bb = BB_name[d]
			max_iou = -np.inf
			b_flag = None
			for p in range(npos):
				# if save_groundTruth:
				# 	shutil.copyfile(result_path + "/" + bb[0] + suffix , save_dir_class_groundTruth + "/" + bb[0] +  suffix)
				
				b_flag = (bb[0] == BBGT_name[p][0])
				# 同一张图像
				if b_flag:
					iou = calcIOU((bb[1] + bb[3]) * 0.5, (bb[2] + bb[4]) * 0.5, bb[3] - bb[1], bb[4] - bb[2], (BBGT_name[p][1] + BBGT_name[p][3]) * 0.5, (BBGT_name[p][2] + BBGT_name[p][4]) * 0.5,
                                                              BBGT_name[p][3] - BBGT_name[p][1], BBGT_name[p][4] - BBGT_name[p][2])
					
					if iou > iou_threshold:
						tp[d] = 1
						npos_flag[p] = 1
						shutil.copyfile(result_path + "/" + bb[0] + suffix , save_dir_class_pos + "/" + bb[0] +  suffix)
						break
			if not b_flag:
				fp[d] = 1
				shutil.copyfile(result_path + "/" + bb[0] + suffix , save_dir_class_neg + "/" + bb[0] + suffix)
				
		print('tp:' , np.sum(tp))
		print('fp:' , np.sum(fp))
		
		for d in range(npos):
			bb = BBGT_name[d]
			if save_groundTruth:
				shutil.copyfile(result_path + "/" + bb[0] + suffix , save_dir_class_groundTruth + "/" + bb[0] + suffix)
			
		sum_tp += np.sum(tp)
		sum_nd += np.sum(fp)
		
		if npos != 0 and nd != 0:
			float_rec = float(np.sum(tp)) / npos
			float_acc = float(np.sum(tp)) / nd
			if float_rec > 1.0:
				float_rec = 1.000000
			if float_acc > 1.0:
				float_acc = 1.000000
			print('the precision of %s is :%f' % (classes[i], float_acc))
			print('the recall of %s is :%f ' % (classes[i], float_rec))
			acc = '%.4f' % (float_acc)
			rec = '%.4f' % (float_rec)
			f.write(classes[i] +'    '+ '\t' + acc +'    '+ '\t' + rec)
			f.write('\n')
			if classes[i] in present_classes:
				sheet.write(line_num, 0, classes[i])
				sheet.write(line_num, 1, acc)
				sheet.write(line_num, 2, rec)
				line_num += 1
			rc.append(float_rec)
			ac.append(float_acc)
		elif npos != 0 and nd == 0:
			print('the recall of %s is : %f' % (classes[i], 0))
		print('---------------------------------------------')
		
		
		
	print('sum_tp:', sum_tp)
	print('sum_pos:', sum_pos)
	print('sum_nd:', sum_nd)
	print('confidence:', confidence)
	print('the Mean precision is :', float(sum_tp) / sum_nd)
	print('the Mean recall is :', float(sum_tp) / sum_pos)
	mean_acc = '%.4f' %(float(sum_tp) / sum_nd)
	mean_rec = '%.4f' %(float(sum_tp) / sum_pos)
	#mean_acc = '%.4f' %(np.mean(ac)) #(float(sum_tp) / sum_nd)
	#mean_rec = '%.4f' %(np.mean(rc)) #(float(sum_tp) / sum_pos)
	f.write('Mean' + '\t' +'    '+ mean_acc + '\t' + mean_rec)
	f.close()
	sheet.write(line_num, 0, 'Mean')
	sheet.write(line_num, 1, mean_acc)
	sheet.write(line_num, 2, mean_rec)
	book.save(result_name + '.xls')
