# coding:utf-8
import glob
import os
import argparse
import shutil
from imutils.paths import list_images

if __name__ == "__main__":
    xml_lsts = glob.glob(os.getcwd() + "/*.xml")
    jpg_lsts = list(list_images(os.getcwd()))
    suffix = jpg_lsts[0].split(".")[1]

    for xml in xml_lsts:
        jpg_name = xml[:-4] + "." + suffix
        if os.path.exists(jpg_name):
            continue
        else:
            print("delete the xml:%s" % (xml))
            os.remove(xml)
    scene_dir = "background"
    if os.path.exists(scene_dir):
        shutil.rmtree(scene_dir)
        os.mkdir(scene_dir)
    else:
        os.mkdir(scene_dir)

    for jpg in jpg_lsts:
        xml_name = jpg.replace(suffix, "xml")
        if os.path.exists(xml_name):
            continue
        else:
            # os.remove(jpg)
            shutil.move(jpg, os.path.join(scene_dir, os.path.basename(jpg)))
