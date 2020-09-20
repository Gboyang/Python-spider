#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup


class MeiZi:
    def __init__(self):
        self.url = 'http://jandan.net/ooxx'
        self.path = os.path.join(os.getcwd(), 'img')
        self.count = 1
        self.pool = ThreadPoolExecutor(20)
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }

    def img_dir(self):
        '''存放目录处理'''
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def download(self, url, path):
        '''下载'''
        by_data = requests.get(url=url, headers=self.headers).content
        with open(path, 'wb') as f1:
            f1.write(by_data)
        print('%s 成功' % path)

    def a_link(self, a_list):
        '''处理图片url'''
        for li in a_list:
            url = 'http:' + str(li['href'])
            path = os.path.join(self.path, "%s.jpg" % self.count)
            self.pool.submit(self.download, url, path)
            self.count += 1

    def run(self):
        self.img_dir()
        response = requests.get(url=self.url, headers=self.headers).text
        soup = BeautifulSoup(response, 'lxml')
        page = soup.find('a', class_="previous-comment-page")
        a_list = soup.select(".commentlist > li > div > div > div > p > a")
        self.a_link(a_list)
        if page:
            url = 'http:' + str(page.attrs['href'])
            self.url = url
            self.run()
        else:
            return None


if __name__ == '__main__':
    M = MeiZi()
    M.run()