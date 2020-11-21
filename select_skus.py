# coding:utf-8

import sys
import xml.etree.cElementTree as ET
import os
import glob
import shutil
import argparse
from tqdm import tqdm
import time


def filter_xml(xml_path, class_id, newdir):
    et = ET.parse(xml_path)
    element = et.getroot()
    element_objs = element.findall("object")

    suffix = None
    if os.path.exists(xml_path[:-3] + "jpg"):
        suffix = "jpg"
    elif os.path.exists(xml_path[:-3] + "png"):
        suffix = "png"

    jpg_dir = os.path.dirname(xml_path)

    for element_obj in element_objs:
        class_name = element_obj.find("name").text
        if class_name == class_id:
            shutil.copyfile(xml_path, newdir + "/" + os.path.basename(xml_path))
            shutil.copyfile(
                xml_path[:-3] + suffix,
                newdir + "/" + os.path.basename(xml_path)[:-3] + suffix,
            )


if __name__ == "__main__":
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
            else:
                break
