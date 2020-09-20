#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

'''梨视频爬取'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
}


def download(url):
    response_text = requests.get(url=url, headers=headers).text
    # var contId="1649482",liveStatusUrl="liveStatus.jsp",liveSta="",playSta="1",autoPlay=!1,isLiving=!1,isVrVideo=!1,hdflvUrl="",sdflvUrl="",hdUrl="",sdUrl="",ldUrl="",srcUrl="https://video.pearvideo.com/mp4/adshort/20200207/cont-1649482-14880359_adpkg-ad_hd.mp4",vdoUrl=srcUrl,skinRes="//www.pearvideo.com/domain/skin",videoCDN="//video.pearvideo.com";
    # 我们需要的srcUrl="https://video.pearvideo.com/mp4/adshort/20200207/cont-1649482-14880359_adpkg-ad_hd.mp4"
    vedio_url = re.findall('srcUrl="(.*?)"', response_text, re.S)[0]
    vedio_data = requests.get(url=vedio_url, headers=headers).content
    vedio_path = vedio_url.split('/')[-1]
    with open(vedio_path, 'wb') as f1:
        f1.write(vedio_data)
        print(vedio_path + '下载成功！.....')


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
