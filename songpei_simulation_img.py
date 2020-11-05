#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :songpei_simulation_img.py
@brief       :处理松沛仿真的数据
@time        :2020/10/28 16:36:45
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import os
from glob import glob
from imutils.paths import list_images
import shutil
from tqdm import tqdm
import argparse
import cv2

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l' , '--label' , help='input label' , required=True , type=str)
    args = parser.parse_args()
    
    current_dir = os.getcwd()
    image_lst = list(list_images(current_dir))
    
    img_lst = [name for name in image_lst if os.path.basename(name).startswith('img')]
    id_lst = [name for name in image_lst if os.path.basename(name).startswith('id')]
    
    for name in tqdm(img_lst):
        base_name = os.path.basename(name)[:-4]
        if os.path.exists(base_name):
            shutil.rmtree(base_name)
            os.mkdir(base_name)
        else:
            os.mkdir(base_name)
        
        
        id_name = name.replace("img" , "id")
        
        if not os.path.exists(id_name.replace(".jpg" , ".png")):
            print(id_name)
            continue
        print(name)
        img = cv2.imread(name)
        #shutil.copyfile(name,  os.path.join(base_name ,  + "img.jpg"))
        cv2.imwrite(os.path.join(base_name , "img.png") , img)
        label_name = os.path.join(base_name , "label.png")
        shutil.copyfile(id_name.replace(".jpg" , ".png") , label_name)
        
        os.remove(name)
        os.remove(id_name.replace(".jpg" , ".png"))
        
        with open(os.path.join(base_name , "label_names.txt") , "w") as f:
            f.write("_background_\n")
            f.write(args.label)
        
        
    
    
    

if __name__ == '__main__':
    main()
    




