#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :remove_multiple.py
@brief       :图像相似性去重
@time        :2020/10/15 10:45:14
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :将脚本放到图片文件夹下执行
'''


# coding:utf-8
from functools import reduce
import numpy as np
import cv2
import sys
from imutils.paths import list_images
import shutil
from tqdm import tqdm
import os


"""
基于缩略图哈希值比较的图像相似性检索
"""


def getHash(img, N=8):
    """
    @src: 文件名/灰度图/BGR
    @N: 缩略图(thumbnail)的大小
    """
    # (1) 图像转化为灰度图
    if img.ndim == 3 and img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # (2) 使用双线性差值缩小图像
    img = cv2.resize(img, (N, N), 0, 0, cv2.INTER_CUBIC)
    # (3) 以均值为阈值进行二值化
    thresh, threshed = cv2.threshold(img, thresh=int(
        np.mean(img)), maxval=255, type=cv2.THRESH_BINARY)
    # (4) 将二值图像转化为二进制位序列
    lst = threshed.ravel().tolist()
    # (5) 为序列求值(注意此处的lambda函数写法)
    xhash = reduce(lambda res, x: (res << 1) | (x > 0 and 1 or 0), lst, 0)
    return xhash


def countOne(x):
    """统计十进制数的二进制位中1的个数（不计符号位）
    assert countOne(0b1101001) == 4
    """
    x = int(x)
    cnt = 0
    while x:
        cnt += 1
        x &= x-1
    return cnt


def hammingDist(x1, x2):
    """计算两个值的汉明距离，即求异或值的二进制位中1的个数
    assert hammingDist(0b001,0b110) == 3
    assert hammingDist(0b111,0b110) == 1
    """
    return countOne(x1 ^ x2)


if __name__ == "__main__":
    current_dir = os.getcwd()
    image_lst = list(list_images(current_dir))

    for i in tqdm(range(len(image_lst))):
        if image_lst[i] == -1:
            continue
        img1 = cv2.imread(image_lst[i])
        if type(img1) == type(None):
            continue
        xhash1 = getHash(img1)
        for j in tqdm(range(i + 1 , len(image_lst))):
            if image_lst[j] == -1:
                continue
            img2 = cv2.imread(image_lst[j])
            if type(img2) == type(None):
                continue
            xhash2 = getHash(img2)

            dist = hammingDist(xhash1 , xhash2)
            if dist <= 0.2:
                os.remove(image_lst[j])
                print("pic one: " , os.path.basename(image_lst[i]))
                print("pic two: " , os.path.basename(image_lst[j]))
                print("---------------------------------------")

                image_lst[j] = -1



