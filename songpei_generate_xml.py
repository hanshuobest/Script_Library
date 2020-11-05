#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :songpei_generate_xml.py
@brief       :利用松沛渲染的模型生成xml
@time        :2020/11/03 15:26:40
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import cv2
import glob
from tqdm import tqdm
from tqdm.cli import main
import os
from imutils.paths import list_images
import argparse
import numpy as np
from pascal_voc_io import PascalVocWriter, XML_EXT


def write_xml(image_file_name, img_folder_name, img_size, bndbox, label):
    imagePath = os.path.join(img_folder_name, image_file_name)
    writer = PascalVocWriter(img_folder_name, image_file_name, (
        img_size[0], img_size[1], 3), localImgPath=imagePath, usrname="auto")
    writer.verified = True
    writer.addBndBox(bndbox[0], bndbox[1], bndbox[2], bndbox[3], label, 0)
    writer.save(targetFile=imagePath[:-4] + XML_EXT)


def get_annotation_from_mask(mask):
    '''Given a mask, this returns the bounding box annotations
    Args:
        mask(NumPy Array): Array with the mask
    Returns:
        tuple: Bounding box annotation (xmin, xmax, ymin, ymax)
    '''
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    if len(np.where(rows)[0]) > 0:
        ymin, ymax = np.where(rows)[0][[0, -1]]
        xmin, xmax = np.where(cols)[0][[0, -1]]
        return xmin, xmax, ymin, ymax
    else:
        return -1, -1, -1, -1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--label', help='input label',
                        required=True, type=str)
    args = parser.parse_args()

    current_dir = os.getcwd()
    image_lst = list(list_images(current_dir))

    img_lst = [name for name in image_lst if os.path.basename(
        name).startswith('img')]
    id_lst = [name for name in image_lst if os.path.basename(
        name).startswith('id')]

    for name in tqdm(img_lst):
        mask_name = name.replace("img" , "id").replace(".jpg" , ".png")
        print(mask_name)
        mask_img = cv2.imread(mask_name, 0)
        _, mask_img = cv2.threshold(mask_img, 10, 255, cv2.THRESH_BINARY)
        xmin, xmax, ymin, ymax = get_annotation_from_mask(mask_img)
        
        image_file_name = os.path.basename(name)
        img_folder_name = os.path.dirname(name)
        img_size = mask_img.shape
        bndbox = (xmin, ymin, xmax , ymax)
        label = args.label
        
        write_xml(image_file_name , img_folder_name , img_size , bndbox , label)


if __name__ == '__main__':
    main()
