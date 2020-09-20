#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


class Main:
    def __init__(self, arg):
        self.url = f'http://www.tianqi.com/{arg}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

    def date(self):
        tq_page = requests.get(url=self.url, headers=self.headers).text
        bs = BeautifulSoup(tq_page, 'lxml')
        nodes = bs.find_all('dd')
        toby = ""
        for n in nodes:
            temp = n.get_text()
            if temp.find('[切换城市]'):
                temp = temp[:temp.find('[切换城市]')]
            toby += temp
        tianqi = "".join([s for s in toby.splitlines(True) if s.strip()])
        print(tianqi)


if __name__ == '__main__':
    t = Main('beijing')
    t.date()