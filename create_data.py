#coding:utf-8
# 制作数据集

import os
import random
# import tensorflow as tf
import argparse
# from tensorflow.contrib import slim
import glob
def createDataset(xml_path , save_path):
    trainval_percent = 1.0
    train_percent = 1.0
    # total_xml = os.listdir(xmlfilepath)
    total_xml = glob.glob(xmlfilepath + '/*.xml')
    num = len(total_xml)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    print("train and val size", tv)
    print("train suze", tr)

    ftrainval = open(os.path.join(saveBasepath, 'ImageSets/Main/trainval.txt'), 'w')
    ftest = open(os.path.join(saveBasepath, 'ImageSets/Main/test.txt'), 'w')
    ftrain = open(os.path.join(saveBasepath, 'ImageSets/Main/train.txt'), 'w')
    fval = open(os.path.join(saveBasepath, 'ImageSets/Main/val.txt'), 'w')

    for i in list:
        name = total_xml[i][:-4] + '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--year')
	args = parser.parse_args()
	
	xmlfilepath = os.path.join(os.getcwd()[:-7] , 'VOC' + args.year + '/Annotations')
	saveBasepath = os.path.join(os.getcwd()[:-7] , 'VOC' + args.year)
	print('xmlfilepath:%s'  %(xmlfilepath))
	print('saveBasepath:%s' %(saveBasepath))
createDataset(xmlfilepath , saveBasepath)
