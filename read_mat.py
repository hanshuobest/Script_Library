#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename    :read_mat.py
@brief       :读取mat文件
@time        :2020/11/10 13:14:52
@author      :hanshuo
@versions    :1.0
@email       :hscoder@163.com
@usage       :
"""

import scipy.io
import cv2
import argparse
import glob
from pascal_voc_io import PascalVocWriter, write_xml
from tqdm import tqdm
import os


classes = [
    "trash_bin",
    "telephone",
    "shoe",
    "pen",
    "pencil",
    "cellphone",
    "can",
    "bottle",
]


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--annatation", help="annation dir")
    parser.add_argument("-i", "--image", help="image dir")
    args = parser.parse_args()
    return args


def main():
    args = parser_args()
    img_lst = glob.glob(args.image + "/*.JPEG")
    mat_lst = glob.glob(args.annatation + "/*.mat")

    image_dir = os.path.dirname(img_lst[0])
    for mat in tqdm(mat_lst):
        try:
            data = scipy.io.loadmat(mat)
            info = data["record"][0][0].tolist()

            image_name = info[0].tolist()[0]
            print(image_name)

            info = info[1][0].tolist()[0]
            cls_name = info[0].tolist()[0]
            if cls_name not in classes:
                continue

            bndbox = info[1].tolist()[0]
            bndbox = list(map(int, bndbox))
            print(bndbox)

            image_file_name = mat.replace(".mat", ".JPEG").replace(
                "Annotations", "Images"
            )
            print(image_file_name)
            image_size = cv2.imread(image_file_name).shape

            img_foler_name = image_dir

            write_xml(
                image_file_name=os.path.basename(image_file_name),
                img_folder_name=img_foler_name,
                img_size=image_size,
                bndbox=bndbox,
                label=cls_name,
            )

        except BaseException as e:
            continue


if __name__ == "__main__":
    main()
