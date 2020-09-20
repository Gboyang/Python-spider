#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
import time
'''爬取LOL所有英雄的皮肤'''


class LOL:
    def __init__(self):
        # 如果需要修改图片存放位置只需该下面即可
        self.dir = os.getcwd()
        self.url = []
        self.hero = 'https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

    '''获取英雄url'''
    def hero_list(self):
        response = requests.get(url=self.hero, headers=self.headers).json()
        for hero in response['hero']:
            hero_id = hero['heroId']
            self.url.append(f'https://game.gtimg.cn/images/lol/act/img/js/hero/{hero_id}.js')

    '''下载'''
    def download(self, url, path):
        b_content = requests.get(url=url, headers=self.headers).content
        with open(path, 'wb') as f1:
            f1.write(b_content)
        print('%s下载成功' % path)
        time.sleep(1)

    '''创建目录'''
    def dir_image(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    '''请求json数据'''
    def hero_page(self):
        self.hero_list()
        for url in self.url:
            response = requests.get(url=url, headers=self.headers).json()
            self.json_date(response)

    '''处理json数据'''
    def json_date(self, response):
        for i in response['skins']:
            if i['mainImg']:
                url = i['mainImg']
                name = i.get('heroName')
                dir1 = os.path.join(self.dir, name)
                self.dir_image(dir1)
                filename = url.split('/')[-1]
                path_name = os.path.join(dir1, filename)
                self.download(url=url, path=path_name)
            else:
                continue


if __name__ == '__main__':
    l = LOL()
    l.hero_page()
