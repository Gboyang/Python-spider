#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor


class KuWo:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), 'mp3')
        self.pool = ThreadPoolExecutor(5)
        self.url = 'http://www.kuwo.cn/api/www/bang/bang/musicList'
        self.url_args = {'bangId': 93, 'pn': 1, 'rn': 30}
        self.info = []
        self.mp3_url_info = 'http://www.kuwo.cn/url'
        self.mp3_url_args = {'type': 'convert_url3', 'br': '128kmp3'}
        self.headers = {
            'Cookie': "_ga=GA1.2.857137131.1584089513; _gid=GA1.2.547561671.1584089513; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1584089512,1584091539,1584153293,1584153999; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1584153999; kw_token=ZS4LBI3VMD",
            'csrf': 'ZS4LBI3VMD',
            'Referer': "http://www.kuwo.cn/rankList",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        }

    def public(self, url, args):
        '''公共'''
        json_data = requests.get(url=url, headers=self.headers, params=args).json()
        return json_data

    def music_list(self):
        '''获取酷我排行榜所有歌曲'''
        response = self.public(self.url, self.url_args)
        if 'musicList' in response['data']:
            for dic in response['data']['musicList']:
                name = dic['name']
                rid = dic['rid']
                self.info.append({'name': name, 'rid': rid})
            self.url_args['pn'] += 1
            self.music_list()
        else:
            return None

    def path_dir(self, name):
        '''路径文件处理'''
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        fi_name = str(name) + '.mp3'
        return os.path.join(self.path, fi_name)

    def download(self, url, path):
        '''下载'''
        mp3 = requests.get(url=url, headers=self.headers).content
        with open(path, 'wb') as f1:
            f1.write(mp3)
        print('%s 下载成功' % path)

    def main(self):
        '''人口'''
        self.music_list()
        for dic in self.info:
            name = dic['name']
            self.mp3_url_args['rid'] = dic['rid']
            path = self.path_dir(name)
            data = self.public(self.mp3_url_info, self.mp3_url_args)
            if data['code'] == 200:
                self.pool.submit(self.download, data['url'], path=path)
                # 怕爬取速度太快被封
                time.sleep(2)


if __name__ == '__main__':
    K = KuWo()
    K.main()
