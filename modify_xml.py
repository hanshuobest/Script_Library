#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import xml.etree.cElementTree as ET
import os
import glob
import argparse

map_label_dict = {1: '7080069', 2: '33010108', 3: '33010109', 4: '33010110', 5: '33010111', 6: '33020040', 7: '33020041', 8: '33040087', 9: '33040088', 10: '33050153', 11: '33060206', 12: '33060207', 13: '33060208', 14: '34070296', 15: '35010266', 16: '35010267', 17: '36030382', 18: '37010231', 19: '37010232', 20: '37010233', 21: '40020209', 22: '66020053', 23: '76010011', 24: '76010012', 25: '76010013', 26: '76010014', 27: '87010001', 28: '87010002', 29: '87010004', 30: '87010005', 31: '87010006', 32: '87010007', 33: '87010008', 34: '87010009', 35: '87010010', 36: '87010011', 37: '87010012', 38: '87010013', 39: '87010014', 40: '87010015', 41: '87010016', 42: '87010017', 43: '87010018', 44: '87010019', 45: '87010020', 46: '87010021', 47: '87010022', 48: '87010023', 49: '87010024', 50: '87010025', 51: '87010026', 52: '87010027', 53: '87010028', 54: '87010029', 55: '87010030', 56: '87010031', 57: '87010032', 58: '87010033', 59: '87010034', 60: '87010035', 61: '87010036', 62: '87010037', 63: '87010038', 64: '87010039', 65: '87010040', 66: '87010041', 67: '87010042', 68: '87010043', 69: '87010044', 70: '87010045', 71: '87010046', 72: '87010047', 73: '87010048', 74: '87010049', 75: '87010050', 76: '87010051', 77: '87010052', 78: '87010053', 79: '87010054', 80: '87010055', 81: '87010056', 82: '87010057', 83: '87010058', 84: '87010059', 85: '87010060', 86: '87010061', 87: '87010062', 88: '87010063', 89: '87010064', 90: '87010065', 91: '87010066', 92: '87010067', 93: '87010068', 94: '87010069', 95: '87010070', 96: '87010071', 97: '87010072', 98: '87010073', 99: '87010074', 100: '87010075', 101: '87010076', 102: '87010077', 103: '87010078', 104: '87010079', 105: '87010080', 106: '87010081', 107: '87010083', 108: '87010084', 109: '87010085', 110: '87010086'}

	
def modify_xml(xml_path , modify_content):
	try:
		et = ET.parse(xml_path)
	except:
		print('xml_path:%s' %(xml_path))
	element = et.getroot()
	path = element.find('path').text
	dir_path = os.path.dirname(path)
	dir_path = dir_path[:-12]
	file_name = os.path.basename(path)
	
	element.find('path').text = os.path.join(modify_content , file_name)
	print(os.path.join(modify_content , file_name))
	element.find('folder').text = modify_content[-18:-11]
	element_objs = element.findall('object')
	for element_obj in element_objs:
		class_name = int(element_obj.find('name').text)
		if class_name in map_label_dict:
			element_obj.find('name').text = map_label_dict[class_name]
	et.write(xml_path)
	
	

if __name__ == '__main__':
	# xml_dir = u'/home/han/桌面/Anno/VOC2018/Annotations'
	# modify_content = u'/home/han/桌面/Anno/VOC2018/JPEGImages'
	parser = argparse.ArgumentParser()
	parser.add_argument('--year')
	args = parser.parse_args()
	
	xml_dir = os.path.join(os.getcwd()[:-7] , 'VOC' + args.year + '/Annotations')
	modify_content = os.path.join(os.getcwd()[:-7] , 'VOC' + args.year + '/JPEGImages')
	print('xml_dir:%s' %(xml_dir))
	print('modify_content:%s' %(modify_content))	
	xml_lsts = glob.glob(xml_dir + '/*.xml')
	for i in xml_lsts:
		modify_xml(i, modify_content)
	
	
