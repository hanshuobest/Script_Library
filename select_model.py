#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename    :select_model.py
@brief       :挑选出用的哪些模型
@time        :2020/11/23 16:01:43
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
"""


import os
import shutil
from glob import glob


def main():
    current_dir = os.getcwd()
    img_lst = glob(current_dir + "/*.jpg")
    save_file = "all_model.txt"
    with open(save_file, "w") as f:
        for img in img_lst:
            if "img" not in img:
                continue
            
            split_str = os.path.basename(img).split("_")
            index = split_str.index("img")
            
            split_str = split_str[index:]
            split_str = "_".join(split_str)
            
            # print(split_str)
            f.write(split_str)
            f.write("\n")


if __name__ == "__main__":
    main()
