# coding:utf-8

import time
from tqdm import tqdm
import argparse
import shutil
import glob
import os
import xml.etree.cElementTree as ET
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filter", help="select or filter", default=True)
    args = parser.parse_args()

    classes = ["wire", "hair", "pen"]
    for i in classes:
        new_dir = str(i) + "-sku"
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        else:
            os.mkdir(new_dir)
        if os.path.isdir(new_dir):
            pass
        else:
            os.mkdir(new_dir)
    xml_dir = os.getcwd()
    lsts = glob.glob(xml_dir + "/*.xml")

    start_time = time.time()
    for i in lsts:
        et = ET.parse(i)
        element = et.getroot()
        element_objs = element.findall("object")

        suffix = None
        if os.path.exists(i[:-3] + "jpg"):
            suffix = "jpg"
        elif os.path.exists(i[:-3] + "png"):
            suffix = "png"
        for element_obj in element_objs:
            class_name = element_obj.find("name").text.strip()
            if class_name in classes:
                new_dir = os.path.join(os.getcwd(), str(class_name) + "-sku")
                shutil.copyfile(i, new_dir + "/" + os.path.basename(i))
                shutil.copyfile(
                    i[:-3] + suffix, new_dir + "/" + os.path.basename(i)[:-3] + suffix
                )
                
                if args.filter:
                    os.remove(i)
                    os.remove(i.replace("xml" , "jpg"))
            else:
                break
    cost_time = time.time() - start_time
    print("cost time:", cost_time)
