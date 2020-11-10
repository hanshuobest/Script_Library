#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :read_mat.py
@brief       :读取mat文件
@time        :2020/11/10 13:14:52
@author      :hanshuo
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import scipy.io
import cv2

data = scipy.io.loadmat('n00000000_1.mat') # 读取mat文件


info = data['record'][0][0].tolist()
# print(info)
image_name = info[0].tolist()[0]
print(image_name)

info = info[1][0].tolist()[0]
cls_name = info[0].tolist()[0]
print(cls_name)
bndbox = info[1].tolist()[0]
print(bndbox)


img = cv2.imread(image_name)
cv2.rectangle(img, (bndbox[0] , bndbox[1]) , ())

