#coding:utf-8

import os
import glob
import json
import shutil


if __name__ == '__main__':
    processed_dir = "processed_dir"
    un_processed_dir = "un_processed_dir"
    if os.path.exists(processed_dir):
        shutil.rmtree(processed_dir)
    else:
        os.mkdir(processed_dir)

    if os.path.isdir(processed_dir):
        pass
    else:
        os.mkdir(processed_dir)

    if os.path.exists(un_processed_dir):
        shutil.rmtree(un_processed_dir)
    else:
        os.mkdir(un_processed_dir)

    if os.path.isdir(un_processed_dir):
        pass
    else:
        os.mkdir(un_processed_dir)

    img_lsts = glob.glob(os.path.join(os.getcwd() , "*.png"))
    for i in img_lsts:
        json_name = i.replace("png" , "json")
        if os.path.exists(json_name):
            with open(json_name , 'rb') as f:
                json_info = json.load(f)
                if len(json_info['shapes']) == 0:
                    os.remove(json_name)
                    shutil.move(i, os.path.join(un_processed_dir, os.path.basename(i)))
                else:
                    shutil.move(i , os.path.join(processed_dir , os.path.basename(i)))
                    shutil.move(json_name , os.path.join(processed_dir ,os.path.basename(json_name)))
        else:
             shutil.move(i , os.path.join(un_processed_dir , os.path.basename(i)))
   
    
    




