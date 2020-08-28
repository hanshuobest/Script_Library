#coding:utf-8
# 脚本描述
# 将脚本放到文件下，自动过滤xml和png
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sys, os
import glob
from tqdm import tqdm
import shutil


classes = ['5','6','7','9','10','15','20','24','32','35','37','38','40','41','42','44','46','54','61','62','63','64','65','66','67','70','71','72','74','75','77','78','79','80','82','88','89','90','91','93','104','105','106']

def readAnnotations(xml_path):
	import xml.etree.cElementTree as ET
	print('xml_path:' , xml_path)	
	et = ET.parse(xml_path)
	element = et.getroot()
	element_objs = element.findall('object')
	if len(element_objs) == 0:
		os.remove(xml_path)
		os.remove(os.path.basename(xml_path)[:-4] + ".png")
		print('the xml is null , delete it  auto:' , os.path.basename(xml_path))
	element_width = int(element.find('size').find('width').text)
	element_height = int(element.find('size').find('height').text)
	
	
	results = []
	if element_width ==0 or element_height == 0:
		os.remove(xml_path)
		print('the xml size is 0 , have deleted the xml:' , xml_path)
		return results
	for element_obj in element_objs:
		result = []
		class_name = element_obj.find('name').text
		# print('class_name:' , class_name)
		if class_name == None:
			print('the xml class is None , have delete the xml :' , os.path.basename(xml_path))
			os.remove(xml_path)
		else:
			if str(class_name) in classes:
				continue
				
			else:
				print('the class of the xml is not exsit  , delete the xml:' , os.path.basename(xml_path))
				shutil.copyfile(xml_path , "other/" + os.path.basename(xml_path))
				shutil.copyfile(os.path.basename(xml_path)[:-4] + ".png" , "other/" + os.path.basename(xml_path)[:-4] + ".png")
				os.remove(xml_path)
				os.remove(os.path.basename(xml_path)[:-4] + ".png")
				break


if __name__=='__main__':
	xml_lsts = glob.glob(os.getcwd() +  "/*.xml")
	if not os.path.exists(os.path.join(os.getcwd() , "other")):
		os.mkdir(os.path.join(os.getcwd() , "other"))
	else:
		pass
	
	for i in xml_lsts:
		readAnnotations(i)
	
		
	print('---------------finished---------------')







