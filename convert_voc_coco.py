
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :convert_voc_coco.py
@brief       :将voc格式的标注文件转为coco格式
@time        :2020/04/11 23:46:15
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :python3 convert_voc_coco.py -i xxx
'''

import os
import glob
import json
import shutil
import numpy as np
import xml.etree.ElementTree as ET
import argparse
from statistic_xml import statistic
 
START_BOUNDING_BOX_ID = 1
 
 
def get(root, name):
    return root.findall(name)
 
def get_and_check(root, name, length):
    vars = root.findall(name)
    if len(vars) == 0:
        raise NotImplementedError('Can not find %s in %s.'%(name, root.tag))
    if length > 0 and len(vars) != length:
        raise NotImplementedError('The size of %s is supposed to be %d, but is %d.'%(name, length, len(vars)))
    if length == 1:
        vars = vars[0]
    return vars
 
 
def convert(xml_list, json_file):
    json_dict = {"images": [], "type": "instances", "annotations": [], "categories": []}
    categories = pre_define_categories.copy()
    bnd_id = START_BOUNDING_BOX_ID
    all_categories = {}
    for index, line in enumerate(xml_list):
        # print("Processing %s"%(line))
        xml_f = line
        tree = ET.parse(xml_f)
        root = tree.getroot()
        
        filename = os.path.basename(xml_f)[:-4] + ".jpg"
        image_id = 1 + index
        size = get_and_check(root, 'size', 1)
        width = int(get_and_check(size, 'width', 1).text)
        height = int(get_and_check(size, 'height', 1).text)
        image = {'file_name': filename, 'height': height, 'width': width, 'id':image_id}
        json_dict['images'].append(image)

        for obj in get(root, 'object'):
            category = get_and_check(obj, 'name', 1).text
            if category in all_categories:
                all_categories[category] += 1
            else:
                all_categories[category] = 1
            if category not in categories:
                if only_care_pre_define_categories:
                    continue
                new_id = len(categories) + 1
                print("[warning] category '{}' not in 'pre_define_categories'({}), create new id: {} automatically".format(category, pre_define_categories, new_id))
                categories[category] = new_id
            category_id = categories[category]
            bndbox = get_and_check(obj, 'bndbox', 1)
            xmin = int(float(get_and_check(bndbox, 'xmin', 1).text))
            ymin = int(float(get_and_check(bndbox, 'ymin', 1).text))
            xmax = int(float(get_and_check(bndbox, 'xmax', 1).text))
            ymax = int(float(get_and_check(bndbox, 'ymax', 1).text))
            assert(xmax > xmin), "xmax <= xmin, {}".format(line)
            assert(ymax > ymin), "ymax <= ymin, {}".format(line)
            o_width = abs(xmax - xmin)
            o_height = abs(ymax - ymin)
            ann = {'area': o_width*o_height, 'iscrowd': 0, 'image_id':
                   image_id, 'bbox':[xmin, ymin, o_width, o_height],
                   'category_id': category_id, 'id': bnd_id, 'ignore': 0,
                   'segmentation': []}
            json_dict['annotations'].append(ann)
            bnd_id = bnd_id + 1
 
    for cate, cid in categories.items():
        cat = {'supercategory': 'none', 'id': cid, 'name': cate}
        json_dict['categories'].append(cat)
    json_fp = open(json_file, 'w')
    json_str = json.dumps(json_dict , indent=2 , ensure_ascii=False)
    json_fp.write(json_str)
    json_fp.close()
    print("------------create {} done--------------".format(json_file))
    print("find {} categories: {} -->>> your pre_define_categories {}: {}".format(len(all_categories), all_categories.keys(), len(pre_define_categories), pre_define_categories.keys()))
    print("category: id --> {}".format(categories))
    print(categories.keys())
    print(categories.values())
 
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' , '--xml' , help='xml和image所在的目录')
    parser.add_argument('-o' , '--output', help='output directory' , default="output")
    parser.add_argument('-r' , '--rate' , help='train dataset rate' , default=1.0)
    
    args = vars(parser.parse_args())

    xml_dir = args['xml']
    clses = statistic(xml_dir)
    classes = [str(c) for c in range(clses)]
    pre_define_categories = {}
    for i, cls in enumerate(classes):
        pre_define_categories[cls] = i + 1
    only_care_pre_define_categories = True
    
    if os.path.exists(args['output']):
        shutil.rmtree(args['output'])
    
    if os.path.isdir(args['output']):
        pass
    else:
        os.mkdir(args['output'])
 
    train_ratio = args['rate']
    save_json_train = 'instances_train.json'
    save_json_val = 'instances_val.json'
    
    xml_list = glob.glob(xml_dir + "/*.xml")
    xml_list = np.sort(xml_list)
    np.random.seed(100)
    np.random.shuffle(xml_list)
 
    train_num = int(len(xml_list)*train_ratio)
    xml_list_train = xml_list[:train_num]
    xml_list_val = xml_list[train_num:]
    
    annotation_path = os.path.join(args['output'] , "annotations")
    train_path = os.path.join(args['output'] , "images/train")
    val_path = os.path.join(args['output'] , "images/val")

    if os.path.exists(annotation_path):
        shutil.rmtree(annotation_path)
    os.makedirs(annotation_path)

    if os.path.exists(train_path):
        shutil.rmtree(train_path)
    os.makedirs(train_path)
    if os.path.exists(val_path):
        shutil.rmtree(val_path)
    os.makedirs(val_path)

    convert(xml_list_train, os.path.sep.join([annotation_path , save_json_train]))
    convert(xml_list_val, os.path.sep.join([annotation_path , save_json_val]))
 
    f1 = open(os.path.sep.join([annotation_path , "train.txt"]), "w")
    for xml in xml_list_train:
        img = xml[:-4] + ".jpg"
        f1.write(os.path.basename(xml)[:-4] + "\n")
        shutil.copyfile(img, os.path.join(train_path , os.path.basename(img)))
 
    f2 = open(os.path.sep.join([annotation_path , "val.txt"]), "w")
    for xml in xml_list_val:
        img = xml[:-4] + ".jpg"
        f2.write(os.path.basename(xml)[:-4] + "\n") 
        shutil.copyfile(img, os.path.join(val_path , os.path.basename(img)))
    f1.close()
    f2.close()
    print("-------------------------------")
    print("train number:", len(xml_list_train))
    print("val number:", len(xml_list_val))