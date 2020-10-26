#coding:utf-8
# 将数据分成训练集和测试集单独保存
import os
import random
import glob
import numpy as np
import shutil

if __name__ == '__main__':
        xml_lsts = glob.glob(os.getcwd() + "/*.xml")
        total_num = len(xml_lsts)
        train_percent = 0.8
        test_percent = 0.2

        num_lst = range(total_num)
        np.random.shuffle(num_lst)

        train_num = int(train_percent * total_num)
        test_num = int(test_percent * total_num)
        
        train = random.sample(num_lst , train_num)
        
        train_dir = "Train"
        test_dir   = "Test"

        if os.path.exists(train_dir):
	        shutil.rmtree(train_dir)
        else:
	        os.mkdir(train_dir)
	        pass
        
        if os.path.exists(test_dir):
	        shutil.rmtree(test_dir)
        else:
	        os.mkdir(test_dir)
	        pass
        
        
        if os.path.isdir(train_dir):
            pass
        else:
            os.mkdir(train_dir)
	    
        if os.path.isdir(test_dir):
             pass
        else:
            os.mkdir(test_dir)
        
	        
        
        for i in num_lst:
            if i in train:
                shutil.copyfile(xml_lsts[i], os.getcwd() + "/" + train_dir + "/" + os.path.basename(xml_lsts[i]))
                shutil.copyfile(xml_lsts[i][:-3] + "jpg", os.getcwd() + "/" + train_dir + "/" + os.path.basename(xml_lsts[i])[:-3] + "jpg")
            else:
	            shutil.copyfile(xml_lsts[i], os.getcwd() + "/" + test_dir + "/" + os.path.basename(xml_lsts[i]))
	            shutil.copyfile(xml_lsts[i][:-3] + "jpg",
	                            os.getcwd() + "/" + test_dir + "/" + os.path.basename(xml_lsts[i])[:-3] + "jpg")
	            
	    
                
	        
             
			
						
