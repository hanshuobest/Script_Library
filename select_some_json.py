#coding:utf-8
import os
import glob
import shutil

if __name__ == '__main__':
		present_classes = ['16', '26', '33', '39', '67', '82', '86', '94', '122', '124', '126', '127', '128', '129', '133', '135', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157', '158', '159']
		data_dir = os.path.join(os.getcwd() , "all_sku")
		new_dir = os.getcwd()

		json_lst = glob.glob(data_dir + "/*.json")
		suffix = None

		img_lst = glob.glob(data_dir + "/*.jpg") + glob.glob(data_dir + "/*.jpg")

		for json in json_lst:
			class_id = os.path.basename(json).split('-')[0]
			if class_id in present_classes:
				shutil.copyfile(json , os.path.join(new_dir , os.path.basename(json)))
	    		if os.path.exists(json[:-5] + ".jpg"):
		  		    suffix = "jpg"
	    		else:
	          		suffix = "png"
            		img_name = json[:-4] + suffix
            		shutil.copyfile(img_name , os.path.join(new_dir , os.path.basename(img_name)))


