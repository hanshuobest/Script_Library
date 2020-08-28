'''
数据增强
'''


#coding:utf-8
import os
import Augmentor
import glob


# 一个小例子
def random_sample():
    p = Augmentor.Pipeline("/Users/han/Desktop/Test")
    p.random_distortion(probability=1 , grid_width=4 , grid_height=4 , magnitude=8)
    p.rotate(probability=1 , max_left_rotation=10 , max_right_rotation=10)
    p.sample(10)

if __name__ == '__main__':
    # data_path = ""
    # p = Augmentor.Pipeline(data_path)
    # # 旋转
    # p.rotate(probability=0.7 , max_left_rotation= 10 , max_right_rotation= 10)
    #
    # # 透视形变 , magnitude 形变程度
    # p.skew_tilt(probability=1 , magnitude=1)
    # # 向四个角形变
    # p.skew_corner(probability=1 , magnitude=1)
    # # 如果进行所有方向的随机变化使用skew()
    # # 弹性扭曲
    # p.random_distortion(probability=1 , grid_height=5 , grid_width=16 , magnitude=8)
    # # 错切变换
    # p.shear(probability=1 , max_shear_left=0 , max_shear_right=20)
    # # 截取
    # # p.crop_by_size(probability=1 , width=100 , height=100 , centre=True)
    # # 镜像变换
    # p.flip_left_right(probability=1)
    # p.flip_random(1)
    # p.flip_top_bottom(probability=1)
    #
    # # 随机去除 rectangle_area变化范围为0.1 - 1
    # p.random_erasing(probability=1 , rectangle_area=0.5)

    random_sample()



