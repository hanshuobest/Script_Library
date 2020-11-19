# -*- coding:utf-8 -*-
# author:hanshuo
# 将文件夹下所有的xml和png都移动到当前目录下

import sys
import os
import glob
import shutil


if __name__ == "__main__":
    for fpath, dirs, fs in os.walk(os.getcwd()):
        for f in fs:
            tmp = os.path.join(fpath, f)
            if not os.path.isfile(tmp):
                continue
            if (
                os.path.basename(tmp)[-3:] == "txt"
                or os.path.basename(tmp)[-3:] == "png"
                or os.path.basename(tmp)[-3:] == "jpg"
                or os.path.basename(tmp)[-4:] == "json"
                or os.path.basename(tmp)[-3:] == "xml"
            ):
                if tmp == os.path.join(os.getcwd(), os.path.basename(tmp)):
                    continue
                else:
                    shutil.copyfile(tmp, os.getcwd() + "/" + os.path.basename(tmp))
                os.remove(tmp)
