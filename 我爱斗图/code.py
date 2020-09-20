#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
import time
from bs4 import BeautifulSoup

'''爬取我爱斗图的图片'''


class DouTu:
    def __init__(self):
        self.url = 'https://www.52doutu.cn/search/%E7%86%8A%E7%8C%AB%E5%A4%B4'
        self.ajx = 'https://www.52doutu.cn/api/'
        self.data = {'types': 'search',
                     'action': 'searchpic',
                     'wd': '熊猫头',
                     'limit': 60,
                     }
        self.dir = os.path.join(os.getcwd(), 'images')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', }

    '''处理原页面的数据'''

    def htm_page(self):
        page_1 = requests.get(url=self.url, headers=self.headers).text
        bs = BeautifulSoup(page_1, 'lxml')
        div_list = bs.select(".img-blocks > .img-block-item > a")
        for i in div_list:
            content_url = i['href']
            self.download(content_url)

    '''处理ajax数据'''

    def ajx_response(self):
        response = requests.post(url=self.ajx, data=self.data).json()
        for url in response['rows']:
            self.download(url['url'])

    '''处理图片名'''

    def tp_name(self, cont_url):
        if not cont_url.endswith(".jpg"):
            name = cont_url.split('/')[-1] + '.jpg'
            joint_path = os.path.join(self.dir, name)
            return joint_path
        else:
            name = cont_url.split('/')[-1]
            joint_path = os.path.join(self.dir, name)
            return joint_path

    '''下载图片'''

    def download(self, cont_url):
        name = self.tp_name(cont_url)
        by_content = requests.get(url=cont_url, headers=self.headers).content
        with open(name, 'wb') as f1:
            f1.write(by_content)
            print('【%s】图片下载成功' % name)
            time.sleep(3)

    def main(self):
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        self.htm_page()
        count = 1
        while True:
            self.data['offset'] = count
            count += 1
            self.ajx_response()


if __name__ == '__main__':
    d = DouTu()
    d.main()
