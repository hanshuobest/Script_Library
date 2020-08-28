#coding:utf-8
from __future__ import print_function
import os
import xlrd

def read_xlsx(xlsx_path):
    workbook = xlrd.open_workbook(xlsx_path)
    booksheet = workbook.sheet_by_name('Sheet1')

    p_sku = []
    p_chinese = []
    # p_sku.append('__background__')
    # p_chinese.append('back')
    for row in range(0 , booksheet.nrows):
        row_data = []
        for col in range(2):
            cel = booksheet.cell(row , col)
            val = int(cel.value)
            if (col + 1) % 2:
                p_sku.append(val)
            else:
                p_chinese.append(val)

    return p_sku , p_chinese

if __name__== '__main__':
	p_sku , p_chinese = read_xlsx('Untitled 1.xlsx')
	f = open("pascal_label_map.pbtxt" , "w")
	k = 1	
	for i ,j in zip(p_sku,p_chinese):
		s = 'item {\n' + '\tid:' + str(k) + '\n' +  '\tname:'  + str("'") + str(j) + str("'") + '}\n'
		# print(s)
		# print('"%s", ' %j ,   end='')
		print(j)
		k += 1
	  	f.write(s)
	f.close()

	
	


