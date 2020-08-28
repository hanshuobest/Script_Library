#coding:utf-8

import os
import glob
import json


def read_json(json_name):
    with open(json_name , 'r') as fp:
        json_info = json.load(fp)
        return json_info
def write_json(json_info , json_name):
    with open(json_name , 'w') as fp:
        json.dump(json_info , fp)



if __name__ == '__main__':
    json_path = "/Users/han/generate_data/sku"
    json_lst = glob.glob(os.path.join(json_path , "*.json"))
    for json_file in json_lst:
        json_info = read_json(json_file)
        imagePath = json_info['imagePath']
        if 'jpg' in imagePath:
            json_info['imagePath'] = imagePath[:-3] + "png"
            write_json(json_info  , json_file)



