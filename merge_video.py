#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :merge_video.py
@brief       :将检测的结果生成视频
@time        :2020/11/05 16:11:59
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import os
import cv2
from glob import glob
from tqdm import tqdm

def main():
    current_dir = os.getcwd()
    image_lst = glob(current_dir + "/*.jpg")
    image_lst = sorted(image_lst , key= lambda item: os.path.basename(item).split('.')[0])
    
    video = cv2.VideoWriter("output_video.mp4" , cv2.VideoWriter_fourcc(*'mp4v') , 15 , (640 , 480))
    
    for name in tqdm(image_lst):
        img = cv2.imread(name)
        video.write(img)
    video.release()

if __name__ == '__main__':
    main()
    
