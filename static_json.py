#coding:utf-8

import os
import glob

json_lsts = glob.glob(os.getcwd() + "/*.json")
img = glob.glob(os.getcwd() + "/*.jpg") + glob.glob(os.getcwd() + "/*.png")
# assert len(json_lsts) == len(img)

print('json_lsts:' , len(json_lsts))
print('img:' , len(img))



suffix = os.path.basename(img[0])[-3:]
print(suffix)
class_statics = {}
for i in img:
	json_name = i[:-3] + "json"
	if not os.path.exists(json_name):
		os.remove(i)
		continue
	class_id = os.path.basename(i).split('-')[0]
	if class_statics.has_key(class_id):
		class_statics[class_id] += 1
	else:
		class_statics[class_id] = 1
		
print('-------------------------------------------------------------------')
print('before sort the number of detect good:')
cls_dict = sorted(class_statics.items() , key = lambda item:int(item[0]))
print(cls_dict)
print('-------------------------------------------------------------------')

cls_dict = dict(cls_dict)
cls_dict = sorted(cls_dict.items() , key=lambda item:item[1] , reverse=True)
print(cls_dict)
print('the number of detect goods:' , len(cls_dict))
print('-------------------------------------------------------------------')


