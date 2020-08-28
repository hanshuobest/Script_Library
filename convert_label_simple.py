#coding:utf-8

import os
import glob
import sys

if __name__ == '__main__':
    json_lsts = glob.glob(os.getcwd() + "/*.json")
    for i in json_lsts:
        str_commod = "/home/han/.local/bin/labelme_json_to_dataset" + " " + os.path.basename(i)
        os.system(str_commod)

    print('finished!')
