#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import random
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool

'''线程池版'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}


def seveData(data):
    vedio_name = str(random.randint(1, 99999)) + '.mp4'
    with open(vedio_name, 'wb') as f1:
        f1.write(data)
        print(vedio_name + '下载成功')


def download(url):
    vedio_urls = []
    response_text = requests.get(url=url, headers=headers).text
    # 我们需要的srcUrl="https://video.pearvideo.com/mp4/adshort/20200207/cont-1649482-14880359_adpkg-ad_hd.mp4"
    vedio_url = re.findall('srcUrl="(.*?)"', response_text, re.S)[0]
    # 获取视频的url追加到列表
    vedio_urls.append(vedio_url)
    # 使用线程池对vedio_urls列表中的url进行视频数据的下载
    pool = Pool(20)
    # 返回视频的二进制数据
    data_list = pool.map(lambda link: requests.get(url=link, headers=headers).content, vedio_urls)
    pool.map(seveData, data_list)


if __name__ == '__main__':
    url = 'https://www.pearvideo.com/popular'
    response = requests.get(url=url, headers=headers)
    page_text = response.text
    # 解析
    bs = BeautifulSoup(page_text, 'lxml')
    li_list = bs.select('.popular-list > li')
    for li in li_list:
        data_url = 'https://www.pearvideo.com/' + li.a['href']
        download(data_url)
