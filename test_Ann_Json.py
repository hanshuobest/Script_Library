#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :test_Ann_Json.py
@brief       :针对金哥的标注数据进行处理
@time        :2020/10/19 13:22:45
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


import glob
import os
import argparse
import json


class JsonProcess(object):
    def __init__(self) -> None:
        pass

    def read_json(self, json_path):
        info = None
        with open(json_path, 'r') as f:
            info = json.load(f)
        return info

    def write_json(self, json_info, save_path):
        with open(save_path, 'w') as fp:
            json.dump(json_info, fp, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    json_lsts = glob.glob(os.getcwd() + "/*.json")
    jpg_lsts = glob.glob(os.getcwd() + "/*.jpg")
    
    jprocess = JsonProcess()

    for j in json_lsts:
        jpg_name = j[:-5] + ".jpg"
        if os.path.exists(jpg_name):
            pass
        else:
            print('delete the json:%s' % (j))
            os.remove(j)
            
        info = jprocess.read_json(j)
        if len(info['shapes']) > 1:
            print(j)
            first_info = info['shapes'][0]
            info['shapes'] = []
            info['shapes'].append(first_info)
            
            jprocess.write_json(info , j)
    for jpg in jpg_lsts:
        json_name = jpg[:-4] + ".json"
        if os.path.exists(json_name):
            continue
        else:
            print(jpg)
            os.remove(jpg)
