#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os


class KuWo:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), 'mp3')
        self.url = 'http://www.kuwo.cn/api/www/bang/bang/musicList'
        self.url_args = {'bangId': 93, 'pn': 1, 'rn': 30}
        self.mp3_url_info = 'http://www.kuwo.cn/url'
        self.mp3_url_args = {'type': 'convert_url3', 'br': '128kmp3'}
        self.headers = {
            'Cookie': "Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1584010620; _ga=GA1.2.496568827.1584010620; _gid=GA1.2.1323051400.1584010620; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1584010629; kw_token=WCLSYUP6S",
            'csrf': 'WCLSYUP6S',
            'Referer': "http://www.kuwo.cn/rankList",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        }

    def mp3_info(self, rid):
        self.mp3_url_args['rid'] = rid
        dic = requests.get(url=self.mp3_url_info, headers=self.headers, params=self.mp3_url_args).json()
        return dic['url']

    def r_mp3(self, mp3_url):
        data = requests.get(url=mp3_url, headers=self.headers).content
        return data

    def save_mp3(self, name, data):
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        s = str(name) + '.mp3'
        name = os.path.join(self.path, s)
        with open(name, 'wb') as f1:
            f1.write(data)
        print('%s 下载成功' % name)

    def main(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.url_args).json()
        if 'musicList' in r['data']:
            for dic in r['data']['musicList']:
                name = dic['name']
                rid = dic['rid']
                mp3_url = self.mp3_info(rid)
                if not mp3_url:
                    continue
                data = self.r_mp3(mp3_url)
                self.save_mp3(name, data)
            self.url_args['pn'] += 1
            self.main()
        else:
            return None


if __name__ == '__main__':
    K = KuWo()
    K.main()
