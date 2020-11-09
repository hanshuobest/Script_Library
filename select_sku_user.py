#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :select_sku_user.py
@brief       :根据用户名挑选xmL
@time        :2020/11/09 13:32:10
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


from tqdm import tqdm
import argparse
import shutil
import glob
import os
import xml.etree.cElementTree as ET


def filter_xml(xml_path, usr_name):
    try:
        et = ET.parse(xml_path)
        element = et.getroot()

        dir_path = os.path.dirname(xml_path)
        newdir = os.path.join(dir_path, usr_name)
        print(xml_path)
        user_name = element.find('usr').text
        if user_name == usr_name:
            shutil.copyfile(xml_path, newdir + "/" +
                            os.path.basename(xml_path))
            shutil.copyfile(xml_path[:-3] + "jpg", newdir +
                            "/" + os.path.basename(xml_path)[:-3] + "jpg")
    except BaseException as e:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    args = parser.parse_args()
    user = args.name

    newdir = os.path.join(os.getcwd(), user)
    if os.path.exists(newdir):
        shutil.rmtree(newdir)  # !/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :select_sku_user.py
@brief       :根据用户名挑选xmL
@time        :2020/11/09 13:32:10
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


def filter_xml(xml_path, usr_name):
    try:
        et = ET.parse(xml_path)
        element = et.getroot()

        dir_path = os.path.dirname(xml_path)
        newdir = os.path.join(dir_path, usr_name)
        print(xml_path)
        user_name = element.find('usr').text
        if user_name == usr_name:
            shutil.copyfile(xml_path, newdir + "/" +
                            os.path.basename(xml_path))
            shutil.copyfile(xml_path[:-3] + "jpg", newdir +
                            "/" + os.path.basename(xml_path)[:-3] + "jpg")
            os.remove(xml_path)
            os.remove(xml_path.replace(".xml" , ".jpg"))
    except BaseException as e:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    args = parser.parse_args()
    user = args.name

    newdir = os.path.join(os.getcwd(), user)
    if os.path.exists(newdir):
        shutil.rmtree(newdir)
    else:
        os.mkdir(newdir)
        pass

    if os.path.isdir(newdir):
        pass
    else:
        os.makedirs(newdir)

    xml_dir = os.getcwd()
    lsts = glob.glob(xml_dir + "/*.xml")
    for i in tqdm(range(len(lsts))):
        filter_xml(lsts[i], user)

