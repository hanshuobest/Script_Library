#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :create_clock.py
@brief       :为每个音频创建一个文件夹
@time        :2020/11/30 16:18:04
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import os
from shutil import rmtree
import json
from glob import glob
import shutil


def write_json(json_info, save_path):
    with open(save_path, 'w') as fp:
        json.dump(json_info, fp, indent=2, ensure_ascii=False)


def main():
    mp3_lst = glob(os.getcwd() + "/*.mp3")
    for i, m in enumerate(mp3_lst):
        save_dir = "sample_clock_" + str(i)
        if os.path.exists(save_dir):
            rmtree(save_dir)
            os.mkdir(save_dir)
        else:
            os.mkdir(save_dir)

        shutil.copyfile(m, os.path.join(save_dir, "audio.mp3"))
        info = {"00:00": "negative"}
        json_name = os.path.join(save_dir , "labels.json")
        write_json(info , json_name)


if __name__ == '__main__':
    main()
