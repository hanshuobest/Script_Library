#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :test_depth.py
@brief       :测试depth和rgb是否对齐
@time        :2020/12/09 09:57:48
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import cv2
import numpy as np

depth_name = "depth_0.png"
color_name = "rgb_0.png"
    
color = cv2.imread(color_name)
depth = cv2.imread(depth_name , -1)

def get_pixel(event , x , y , flags , param):
    if param == "color":
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"color click: {x} ,  {y}")
    elif param == 'depth':
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f"depth click: {x} ,  {y}")
            
            cur_depth = depth[y][x]
            print("cur_depth: " , cur_depth)
         

def main():
    global color , depth
    
    tmp_depth = depth * 255
    
    cv2.namedWindow("depth")
    cv2.namedWindow("color")
    cv2.setMouseCallback('color' , get_pixel , param="color")
    cv2.setMouseCallback('depth' , get_pixel , param="depth")
    while True:
        cv2.imshow("depth" , tmp_depth)
        cv2.imshow("color" , color)
        if cv2.waitKey(20) & 0xFF == 27:
            break
        
    cv2.destroyAllWindows()
    
     
if __name__ == '__main__':
    main()
    
