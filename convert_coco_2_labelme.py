#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :convert_coco_2_labelme.py
@brief       :将coco数据转为labelme格式的json
@time        :2020/10/15 13:44:03
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import json
import cv2
import numpy as np
import os
from glob import glob
from pycocotools.coco import COCO
import argparse
import shutil
from imutils.paths import list_images
from tqdm import tqdm


classes = ['cat', 'dog', 'person', 'bottle', 'chair', 'potted plant',
           'sports ball', 'cup', 'chair', 'toilet', 'mouse', 'cell phone', 'remote',
           'book']

classes_dict = {}


def reference_labelme_json(ref_json_path):
    data = json.load(open(ref_json_path))
    return data


def catid2name(coco):
    classes = dict()
    for cat in coco.dataset['categories']:
        classes[cat['id']] = cat['name']
    return classes


def labelme_shapes(data, data_ref):
    global classes_dict
    shapes = []
    for d in data:
        shape = {}
        label_name = d['category_id']
        if label_name == "potted plant":
            label_name = "potted_plant"
        elif label_name == "sports ball":
            label_name = "ball"
        elif label_name == "cell phone":
            label_name = "cellphone"
        
        shape['label'] = classes_dict[label_name]
        if len(d['segmentation']) == 0:
            continue
        
        try:
            x = d['segmentation'][0][::2]
            y = d['segmentation'][0][1::2]
            shape['points'] = []

            for j in range(len(x)):
                shape['points'].append([x[j], y[j]])
            shape['shape_type'] = data_ref['shapes'][0]['shape_type']
            shape['flags'] = data_ref['shapes'][0]['flags']
            shape['ground_id'] = None
            shapes.append(shape)
            
            break
        except BaseException as e:
            continue

    return shapes


def read_coco(json_file, save_dir , image_lst):
    global classes_dict
    coco = COCO(json_file)
    classes_dict = catid2name(coco)
    base_dir = os.path.dirname(image_lst[0])
    
    for cat in tqdm(classes):
        clsIds = coco.getCatIds(catNms=[cat])
        if len(clsIds) == 0:
            continue
            
        # catIds = coco.getCatIds(catNms=[cat])
        imgIds = coco.getImgIds(catIds=clsIds)
        
        if cat == "potted plant":
            cat = "potted_plant"
        elif cat == "sports ball":
            cat = "ball"
        elif cat == "cell phone":
            cat = "cellphone"
            
        cat_dir = os.path.join(save_dir, cat)
        if os.path.exists(cat_dir):
            shutil.rmtree(cat_dir)
            os.mkdir(cat_dir)
        else:
            os.mkdir(cat_dir)    
                
        for imgId in imgIds:
            img = coco.loadImgs(imgId)[0]
            filename = img['file_name']
            height = img['height']
            width = img['width']

            print("filename: " , filename)
            annIds = coco.getAnnIds(
                imgIds=img['id'], catIds=clsIds, iscrowd=None)

            anns = coco.loadAnns(annIds)
            if len(anns) == 0:
                continue

            data_labelme = {}
            shape_info = labelme_shapes(anns, data_ref)
            if len(shape_info) == 0:
                continue
            
            save_json_name = os.path.join(
                cat_dir , cat + "_" + filename.replace("jpg", "json"))
            src_image_name = os.path.join(base_dir , filename)
            save_image_name = save_json_name.replace(".json" , ".jpg")
            
            data_labelme['shapes'] = shape_info
            data_labelme['version'] = data_ref['version']
            data_labelme['flags'] = data_ref['flags']
            data_labelme['imagePath'] = os.path.basename(save_image_name)
            data_labelme['imageData'] = None
            data_labelme['imageHeight'] = height
            data_labelme['imageWidth'] = width
           
            if os.path.exists(src_image_name):
                shutil.copyfile(src_image_name , save_image_name)
            else:
                continue
            with open(save_json_name, 'w') as fp:
                json.dump(data_labelme, fp, indent=2, ensure_ascii=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d' , '--directory' , help='coco json directory' , default='instances_train2017.json')
    parser.add_argument('-s' , '--save' , help='save directory' , default = "labelme_json")
    parser.add_argument('-i' , '--image' , help='image directory' , default='/home/ubuntu/data/Data/CoCo/train2017')
    parser.add_argument('-r' , '--reference' , help='reference label json' , required=True)
    args = vars(parser.parse_args())
    
    # 参考的json
    data_ref = reference_labelme_json(args['reference'])
    if os.path.exists(args['save']):
        shutil.rmtree(args['save'])
        os.mkdir(args['save'])
    else:
        os.mkdir(args['save'])
    
    image_lst = []
    if os.path.exists(args['image']):
        image_lst = list(list_images(args['image']))

    read_coco(args['directory'] , args['save'] , image_lst)
