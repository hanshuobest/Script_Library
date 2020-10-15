#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :remove_multiple.py
@brief       :图像相似性去重
@time        :2020/10/15 10:45:14
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''


# coding:utf-8
from functools import reduce
import numpy as np
import cv2
import sys



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
    # 读取图像
    img1 = cv2.imread("testImg/1_1.png")
    img2 = cv2.imread("testImg/3_1.png")
    # 计算哈希
    xhash1 = getHash(img1)
    xhash2 = getHash(img2)
    # 进行汉明距离度量
    dist = hammingDist(xhash1, xhash2)

    print("xhash1: {}\nxhash2: {}\ndist: {}".format(xhash1, xhash2, dist))
