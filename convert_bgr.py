#coding:utf-8

import cv2
import numpy as np
import glob
import math
import os

if __name__ == '__main__':
    dir_path = os.getcwd()

    img_lsts = glob.glob(dir_path + "/*.jpg")
    
    resize_height = 416
    resize_width = 416
    print(img_lsts)
    for i in img_lsts:
        img = cv2.imdecode(np.fromfile(i , dtype=np.uint8) , -1)
        img = cv2.resize(img , (resize_height , resize_width))
        img = img.astype('uint8')
        b , g , r = cv2.split(img)
        height = img.shape[0]
        width = img.shape[1]
        channels = img.shape[2]

        file_path = i[:-4] + str("-") + str(resize_height) + "x" + str(resize_width) + ".bgr"
        fileSave = open(file_path , "wb")
        for step in range(0 , height):
            for step2 in range(0 , width):
                fileSave.write(b[step , step2])

        for step in range(0, height):
            for step2 in range(0, width):
                fileSave.write(g[step, step2])
        for step in range(0, height):
            for step2 in range(0, width):
                fileSave.write(r[step, step2])

        fileSave.close()
        print('finished!')








