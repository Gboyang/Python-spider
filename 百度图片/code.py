#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import random
import os, re
from multiprocessing.dummy import Pool
'''这里只爬取30张图片'''


class Main:
    def __init__(self, arg_url):
        self.url = f'https://image.baidu.com/search/index?tn=baiduimage&word={arg_url}'
        self.dir = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'images')
        self.headers = {
            # 本次请求可以接受的内容
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            # 可以接受的语言类型
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 告诉服务器从哪里来（从哪个网站过来的）
            'Referer': 'http://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%CD%BC%C6%AC&fr=ala&ala=1&alatpl=others&pos=0',
            # 判断程序和浏览器的重要参数
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }

    def re_objURL(self, html):
        # objURL":"http://hbimg.huabanimg.com/06291209b02235823792e214e664a5bd3e070e001eab2-jLxePs_fw658
        obj_url = re.findall('"objURL":"(.*?)"', html, re.DOTALL)
        return obj_url

    def download(self, url):
        bytes_content = requests.get(url=url, headers=self.headers).content
        name = os.path.join(self.dir, str(random.randint(1, 99999)) + '.jpg')
        with open(name, 'wb') as f1:
            f1.write(bytes_content)
            f1.close()
        print('%s下载成功' % name)

    def dir_images(self):
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        else:
            print('请先删除%s再次执行' % self.dir)

    def run(self):
        response_text = requests.get(url=self.url, headers=self.headers).text
        url_list = self.re_objURL(response_text)
        self.dir_images()
        pool = Pool(10)
        pool.map(self.download, url_list)


if __name__ == '__main__':
    user_info = input('请输入你要下载的图片：').strip()
    obj = Main(user_info)
    obj.run()
