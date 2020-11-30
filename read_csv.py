#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@filename    :read_csv.py
@brief       :读取csv文件
@time        :2020/11/30 14:47:05
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
"""

import pandas as pd
import csv
import numpy as np


def main():
    csv_file = "/home/han/data/Data/ESC-50-master/ESC-50-master/meta/esc50.csv"
    csv_data = pd.read_csv(csv_file, usecols=["filename", "category"])

    save_names = []
    fs = open("clock.txt", "w")
    # f_cry = open("clock.txt", "w")

    csv_data = np.array(csv_data).tolist()
    for filename, cls in csv_data:
        if "clock" in cls:
            print(cls)
            save_names.append(filename)
            fs.write(filename)
            fs.write("\n")

        # if "cry" in cls:
        #     f_cry.write(filename)
        #     f_cry.write("\n")

    fs.close()
    # f_cry.close()


if __name__ == "__main__":
    main()
