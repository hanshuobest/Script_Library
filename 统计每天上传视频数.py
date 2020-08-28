# 统计每天上传视数

import shelve
import os
import matplotlib.pyplot as plt

s = shelve.open('./records')
data_lst = []
for k , v in s.items():
    # if v['date'][:10] > '2019-10-01':
        data_lst.append(v['date'][:10])

date_dict = {}
for d in data_lst:
    if d in date_dict:
        date_dict[d] += 1
    else:
        date_dict[d] = 1

date_dict = dict(sorted(date_dict.items() , key= lambda  item: item[0] , reverse = False))
print(date_dict)

x = []
y = []
index = 0
for k , v in date_dict.items():
    x.append(index)
    y.append(v)
    index += 1

plt.plot(x , y)
plt.show()

print('平均每天：' , len(data_lst)/len(x))

s.close()


