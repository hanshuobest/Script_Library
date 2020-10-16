#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :convert_coco_2_voc.py
@brief       :將coco数据格式转为voc
@time        :2020/08/28 01:08:16
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


from pycocotools.coco import COCO
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import os
import cv2
import shutil
from lxml import etree, objectify
from tqdm import tqdm
import random
from PIL import Image
import json
import argparse
from pascal_voc_io import PascalVocWriter, XML_EXT


classes = ['cat', 'dog', 'person', 'bottle', 'chair', 'potted plant',
           'sports ball', 'cup', 'chair', 'toilet', 'mouse', 'cell phone', 'remote',
           'book']


def catid2name(coco):
    classes = dict()
    for cat in coco.dataset['categories']:
        classes[cat['id']] = cat['name']
        # print(str(cat['id'])+":"+cat['name'])
    return classes


def convert_coco2_voc(json_file, save_dir):
    coco = COCO(json_file)
    classes_dict = catid2name(coco)

    for cat in classes:
        catIds = coco.getCatIds(catNms=[cat])
        if len(catIds) == 0:
            continue
        
        imgIds = coco.getImgIds(catIds=catIds)
        for imgId in tqdm(imgIds):
            img = coco.loadImgs(imgId)[0]
            filename = img['file_name']
            height = img['height']
            width = img['width']

            annIds = coco.getAnnIds(
                imgIds=img['id'], catIds=catIds, iscrowd=None)
            anns = coco.loadAnns(annIds)
            if len(anns) == 0:
                continue
            
            writer = PascalVocWriter(
            filename, filename, (height, width, 3), localImgPath=filename)
            writer.verified = True
            objs = []
            for ann in anns:
                name = classes_dict[ann['category_id']]
                if name in classes:
                    if 'bbox' in ann:
                        bbox = ann['bbox']
                        xmin = (int)(bbox[0])
                        ymin = (int)(bbox[1])
                        xmax = (int)(bbox[2]+bbox[0])
                        ymax = (int)(bbox[3]+bbox[1])
                        obj = [name, 1.0, xmin, ymin, xmax, ymax]
                        objs.append(obj)

                        writer.addBndBox(xmin, ymin, xmax, ymax, name, 0)
            writer.save(os.path.join(save_dir, filename.replace("jpg", "xml")))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', help='json file',
                        default='instances_train2017.json')
    parser.add_argument('-x', '--xml', help='save xml dir', default='xml')
    args = vars(parser.parse_args())
    if os.path.exists(args['xml']):
        shutil.rmtree(args['xml'])
        os.mkdir(args['xml'])
    else:
        os.mkdir(args['xml'])

    convert_coco2_voc(args['json'], args['xml'])
