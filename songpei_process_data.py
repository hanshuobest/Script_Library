#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename    :songpei_process_data.py
@brief       :处理松沛数据生成xml
@time        :2020/11/12 11:23:40
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :python3 songpei_process_data.py -i /home/han/Downloads/water
"""


import os
from glob import glob
from pascal_voc_io import PascalVocWriter, XML_EXT, write_xml
import argparse
import cv2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input dir")
    args = parser.parse_args()

    current_dir = args.input

    # img_lst = glob(current_dir + "/*.jpg")
    txt_lst = glob(current_dir + "/*.txt")

    for txt_f in txt_lst:
        with open(txt_f, "r") as f:
            all_line = f.readlines()

            if len(all_line) == 0:
                continue

            image_file_name = txt_f.replace(".txt", ".jpg")
            img_folder_name = os.path.dirname(txt_f)
            img = cv2.imread(image_file_name)
            img_size = img.shape

            bndboxs = []
            labels = []

            for line in all_line:
                per_line = line.split(" ")
                per_line[-1] = per_line[-1].strip()
                per_line = list(map(float, per_line))

                label = None
                if per_line[0] == 0.0:
                    label = "hair"
                else:
                    label = "cluster_hair"
                    
                labels.append(label)

                cx = per_line[1] * img_size[1]
                cy = per_line[2] * img_size[0]
                w = per_line[3] * img_size[1]
                h = per_line[4] * img_size[0]

                bndbox = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
                bndbox = list(map(int, bndbox))
                
                bndboxs.append(bndbox)

            
            write_xml(
                image_file_name=os.path.basename(image_file_name),
                img_folder_name=img_folder_name,
                img_size=img.shape,
                bndboxs=bndboxs,
                labels=labels,
            )


if __name__ == "__main__":
    main()
