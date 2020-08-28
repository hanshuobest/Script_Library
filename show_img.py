#coding:utf-8
import cv2
import argparse


if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--name' , required = True)
	args = parser.parse_args()
	
	img = cv2.imread(args.name)
	cv2.imshow('image' , img)
	cv2.waitKey(0)
