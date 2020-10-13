#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@filename    :crawling.py
@brief       :指定类别爬虫
@time        :2020/10/12 11:15:48
@author      :hscoder
@versions    :1.0
@email       :hscoder@163.com
@usage       :
'''

import argparse
import os
import pdb
import re
import sys
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time
import traceback
from tqdm import tqdm

timeout = 5
socket.setdefaulttimeout(timeout)

# classes = ['dog' , 'cat' , 'person' , 'weight scale' , 'ball' , 'shoes' , 'clothes' 
#            , 'book' , 'bottle' , 'pen' , 'socks' , 'paper' , 'cellphone' , 'furniture base'
#            , 'weight scale' , 'power strip' , 'Pet feces' , 'glasses' , 'sofa' , 'chair' 
#            , 'table' , 'remote controller' , 'jewelry' , 'Trash can' , 'potted plant']

classes = ['dog']


class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    __per_page = 30

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 获取后缀名
    @staticmethod
    def get_suffix(name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 保存图片
    def save_image(self, rsp_data, word , image_count = 1000):
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir('./' + word)) + 1
        for image_info in rsp_data['data']:
            try:
                if 'replaceUrl' not in image_info or len(image_info['replaceUrl']) < 1:
                    continue
                obj_url = image_info['replaceUrl'][0]['ObjUrl']
                thumb_url = image_info['thumbURL']
                url = 'https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=%s&thumburl=%s' % (
                    urllib.parse.quote(obj_url), urllib.parse.quote(thumb_url))
                print('url: %s' % obj_url)

                suffix = self.get_suffix(obj_url)
                # 指定UA和referrer，减少403
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'),
                ]
                urllib.request.install_opener(opener)
                # 保存图片
                filepath = './%s/%s' % (word,
                                        str(self.__counter) + str(suffix))
                urllib.request.urlretrieve(url, filepath)
                if os.path.getsize(filepath) < 5:
                    print("下载到了空文件，跳过!")
                    # 删除文件
                    os.unlink(filepath)
                    continue
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                print("下载+1,已有" + str(self.__counter) + "张图")
                self.__counter += 1
                
            finally:
                if self.__counter > image_count:
                    break  
        
        print("self.__counter： " , self.__counter)  
        return self.__counter

    # 开始获取
    def get_images(self, word , image_count = 1000):
        search = urllib.parse.quote(word)
        tmp_count = 0
        pn = self.__start_amount
        while pn < self.__amount:
            url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word=%s&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=%s&rn=%d&gsm=1e&1594447993172=' % (
                search, search, str(pn), self.__per_page)
            
            # 设置header防403
            try:
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                rsp = page.read()
                
                 # 解析json
                rsp = rsp.decode()
                rsp = rsp.replace(r"\'" , r"\\'")
                rsp_data = json.loads(rsp , strict = False)
                tmp_count = self.save_image(rsp_data, word , image_count)
                print("tmp_count: " , tmp_count)
                print("image_count: " , image_count)
                if tmp_count > image_count:
                    print("tmp_count > image_count")
                    page.close()
                    break
                
                # 读取下一页
                print("下载下一页")
                pn += 60
                
            except BaseException as e:
                print('download image occur---{}'.format(e))
                print(traceback.format_exc())
                print('url: {}'.format(url))
                continue
                
        print("下载任务结束")
   

    def start(self, total_page=1, start_page=1, per_page=30 , count=1000):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param total_page: 需要抓取数据页数 总抓取图片数量为 页数 x per_page
        :param start_page:起始页码
        :param per_page: 每页数量
        :return:
        """
        self.__per_page = per_page
        self.__start_amount = (start_page - 1) * self.__per_page
        self.__amount = total_page * self.__per_page + self.__start_amount

        for word in tqdm(classes):
           self.get_images(word , count)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-tp", "--total_page", type=int,
                        help="需要抓取的总页数" , default=10000)
    parser.add_argument("-sp", "--start_page", type=int,
                        help="起始页数" , default=1)
    parser.add_argument("-pp", "--per_page", type=int, help="每页大小",
                        choices=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], default=30, nargs='?')
    parser.add_argument("-d", "--delay", type=float,
                        help="抓取延时（间隔）", default=0.05)
    parser.add_argument("-c" , "--count" , type=int,
                        help="每个类别图片数量" , default=1000)
    args = parser.parse_args()

    crawler = Crawler(args.delay)
    crawler.start(args.total_page, args.start_page, args.per_page , args.count)
