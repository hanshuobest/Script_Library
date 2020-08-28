#coding:utf-8
# coder:hanshuo
# 2018-5-23

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import glob
import argparse
import shutil


# from:
# to  :/home/han/darknet/scripts/VOCdevkit/Test
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--fromdir")
    parser.add_argument("--todir")
    args = parser.parse_args()
    
    from_dir = args.fromdir
    to_dir = args.todir
    
    # print('from_dir:' , from_dir)
    # print('to_dir:' , to_dir)
    
    lst_dir = os.listdir(from_dir)
    print(lst_dir)
    jpg_dirs = []
    xml_dirs = []
    for i in lst_dir:
        if i.endswith('xml'):
             xml_dirs.append(i)
        else:
             jpg_dirs.append(i)
    
    print('xml_dirs:' , xml_dirs)
    print('jpg_dirs:' , jpg_dirs)
    
    for xml_dir in xml_dirs:
	print(xml_dir)
        dirs = os.listdir(from_dir + "/" + xml_dir)
        for d in dirs:
            lsts = glob.glob(from_dir + "/" + xml_dir + "/" + d + "/*.xml")
            for i in lsts:
                shutil.copyfile(i , to_dir  +  "/" + os.path.basename(i))
	
    for jpg_dir in jpg_dirs:
        dirs = os.listdir(from_dir + "/" + jpg_dir)
        for d in dirs:
            lsts = glob.glob(from_dir + "/" + jpg_dir + "/" + d + "/*.png")
            for i in lsts:
                shutil.copyfile(i, to_dir + "/" + os.path.basename(i))
		
    print('finished!')
 

