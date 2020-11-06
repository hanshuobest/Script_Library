# coding:utf-8
import xml.etree.cElementTree as ET
from tqdm import tqdm
import argparse
import shutil
import glob
import os
import sys


def select_sku(img_dir, xml_dir, label_name, select_number):
    xml_lsts = glob.glob(xml_dir + "/*.xml")
    img_lsts = glob.glob(img_dir + "/*.jpg")

    save_dir = label_name + "-sku"
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    else:
        os.makedirs(save_dir)

    num_images = len(xml_lsts)
    count = 0
    for i in tqdm(range(num_images)):
        et = ET.parse(xml_lsts[i])
        element = et.getroot()
        try:
            user_name = element.find('usr').text
            if user_name == "auto":
                continue
        except:
            pass
        element_objs = element.findall('object')
        tmp = []
        for element_obj in element_objs:
            class_name = element_obj.find('name').text.strip()
            tmp.append(class_name)

        d = [False for cls in tmp if cls != label_name]
        if d:
            continue

        for element_obj in element_objs:
            class_name = element_obj.find('name').text.strip()
            if class_name == label_name:
                count += 1

        new_image_name = os.path.join(save_dir, os.path.basename(
            xml_lsts[i].replace(".xml", ".jpg")))
        new_xml_name = os.path.join(save_dir, os.path.basename(xml_lsts[i]))
        shutil.copyfile(xml_lsts[i], new_xml_name)
        shutil.copyfile(xml_lsts[i].replace(".xml", ".jpg"), new_image_name)

        if count > select_number:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number')
    parser.add_argument('-l', '--label')

    args = parser.parse_args()
    num = int(args.num)
    print('num:', num)
    
    current_dir = os.getcwd()
    xml_path , img_path = current_dir, current_dir
    select_sku(img_path , xml_path , args.label , 1000)
    

    # sku_dicts = {}
    # sku_lst = ['5', '6', '9', '10', '11', '20', '24', '26', '30', '37', '40', '41', '42', '44', '46', '61', '63', '64', '65',
    #            '66', '67', '74', '75', '77', '78', '85', '88', '90', '91', '104', '105']

    # xml_lsts = glob.glob(os.getcwd() + "/Annotations/*.xml")
    # suffix = None
    # if os.path.exists(os.getcwd() + "/JPEGImages/" + os.path.basename(xml_lsts[0])[:-3] + "jpg"):
    #     suffix = "jpg"
    # elif os.path.exists(os.getcwd() + "/JPEGImages/" + os.path.basename(xml_lsts[0])[:-3] + "png"):
    #     suffix = "png"

    # new_dir = os.path.join(os.getcwd(), str(len(sku_lst)) + "sku")
    # if os.path.exists(new_dir):
    #     shutil.rmtree(new_dir)
    # else:
    #     os.mkdir(new_dir)

    # if os.path.isdir(new_dir):
    #     pass
    # else:
    #     os.mkdir(new_dir)

    # num_images = len(xml_lsts)
    # for i in tqdm(range(num_images)):
    #     et = ET.parse(xml_lsts[i])
    #     element = et.getroot()
    #     try:
    #         user_name = element.find('usr').text
    #         if user_name == "auto":
    #             continue
    #     except:
    #         pass
    #     element_objs = element.findall('object')

    #     tmp = []
    #     for element_obj in element_objs:
    #         class_name = element_obj.find('name').text
    #         if class_name not in sku_lst:
    #             break
    #         tmp.append(class_name)

    #     if len(tmp) != len(element_objs):
    #         continue
    #     for element_obj in element_objs:
    #         class_name = element_obj.find('name').text
    #         if sku_dicts.has_key(class_name):
    #             sku_dicts[class_name] += 1
    #         else:
    #             sku_dicts[class_name] = 1
    #     flag = [True for t in range(len(tmp))]
    #     for index, j in enumerate(tmp):
    #         # print(sku_dicts[j])
    #         if sku_dicts[j] > num:
    #             # print('fuck:' , sku_dicts[j])
    #             flag[index] = False
    #             break
    #     if False not in flag:
    #         # print(xml_lsts[i])
    #         shutil.copyfile(xml_lsts[i], new_dir +
    #                         "/" + os.path.basename(xml_lsts[i]))
    #         shutil.copyfile(os.getcwd() + "/JPEGImages/" + os.path.basename(xml_lsts[0])[
    #                         :-3] + suffix, new_dir + "/" + os.path.basename(xml_lsts[i])[:-3] + suffix)

    #     # print(xml_lsts[i])
    # print(sku_dicts)
