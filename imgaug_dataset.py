#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :imgaug_dataset.py
@brief       :数据增强生成bndbox
@time        :2020/11/24 21:13:00
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import xml.etree.ElementTree as ET
import pickle
import os
from os import getcwd
import numpy as np
from PIL import Image
import cv2
from glob import glob
import imgaug as ia
from imgaug import augmenters as iaa
from pascal_voc_io import write_xml, PascalVocWriter, XML_EXT
import argparse
import shutil
from tqdm import tqdm
ia.seed(1)


def read_xml_annotation(root, image_id):
    in_file = open(os.path.join(root, image_id))
    tree = ET.parse(in_file)
    root = tree.getroot()

    bndbox = root.find('object').find('bndbox')

    xmin = int(bndbox.find('xmin').text)
    xmax = int(bndbox.find('xmax').text)
    ymin = int(bndbox.find('ymin').text)
    ymax = int(bndbox.find('ymax').text)

    return (xmin, ymin, xmax, ymax)


def readAnnotations(xml_path):
    import xml.etree.cElementTree as ET

    et = ET.parse(xml_path)
    element = et.getroot()
    element_objs = element.findall('object')

    results = []
    for element_obj in element_objs:
        result = []
        class_name = element_obj.find('name').text.strip()
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


def change_xml_annotation(root, image_id, new_target):

    new_xmin = new_target[0]
    new_ymin = new_target[1]
    new_xmax = new_target[2]
    new_ymax = new_target[3]

    import pdb
    pdb.set_trace()
    in_file = open(os.path.join(root, str(image_id)+'.xml'))  # 这里root分别由两个意思
    tree = ET.parse(in_file)
    xmlroot = tree.getroot()
    object = xmlroot.find('object')
    bndbox = object.find('bndbox')
    xmin = bndbox.find('xmin')
    xmin.text = str(new_xmin)
    ymin = bndbox.find('ymin')
    ymin.text = str(new_ymin)
    xmax = bndbox.find('xmax')
    xmax.text = str(new_xmax)
    ymax = bndbox.find('ymax')
    ymax.text = str(new_ymax)
    tree.write(os.path.join(root, str(image_id)+"_aug"+'.xml'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--times", help="multiply times", default=1)
    args = parser.parse_args()

    current_dir = os.getcwd()
    aug_dir = "aug"
    if os.path.exists(aug_dir):
        shutil.rmtree(aug_dir)
        os.mkdir(aug_dir)
    else:
        os.mkdir(aug_dir)

    xml_lst = glob(current_dir + "/*.xml")
    img_lst = glob(current_dir + "/*.jpg")
    
    for img_name in tqdm(img_lst):
        img = Image.open(img_name)
        img = np.array(img)

        results = readAnnotations(img_name.replace("jpg", "xml"))
        bndboxes = []
        for bndbox in results:
            bndboxes.append(ia.BoundingBox(
                x1=bndbox[1], y1=bndbox[2], x2=bndbox[3], y2=bndbox[4]))

        bbs = ia.BoundingBoxesOnImage(bndboxes, shape=img.shape)

        for i in range(int(args.times)):
            seq = iaa.Sequential([
                iaa.Flipud(0.5),
                iaa.Multiply((1.2, 1.5)),
                iaa.Affine(
                    translate_px={"x": 10, "y": 10},
                    scale=(0.8, 0.95),
                    rotate=(-10, 10)
                )
            ])

            # 保持坐标和图像同步改变，而不是随机
            seq_det = seq.to_deterministic()
            image_aug = seq_det.augment_images([img])[0]
            bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]

            after_bnds = bbs_aug.bounding_boxes

            # # image_before = bbs.draw_on_image(img, thickness=2)
            image_after = bbs_aug.draw_on_image(image_aug, thickness=2)
            save_img_name = "aug_" + str(i) + os.path.basename(img_name)
            save_img_name = os.path.join(aug_dir, save_img_name)

            Image.fromarray(image_aug).save(save_img_name)

            bboxes = []
            labels = []
            for r, _ in enumerate(results):
                box = []
                box.append(int(bbs_aug.bounding_boxes[r].x1))
                box.append(int(bbs_aug.bounding_boxes[r].y1))
                box.append(int(bbs_aug.bounding_boxes[r].x2))
                box.append(int(bbs_aug.bounding_boxes[r].y2))
                bboxes.append(box)
                labels.append(results[r][0])

            write_xml(os.path.basename(save_img_name), os.path.dirname(
                save_img_name), img_size=img.shape[:2], bndboxs=bboxes, labels=labels)
