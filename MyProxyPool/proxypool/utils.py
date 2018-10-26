#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import requests
import asyncio
import aiohttp
from fake_useragent import UserAgent, FakeUserAgentError
from requests.exceptions import ConnectionError

def get_page(url, options={}):
    """
    抓取代理
    :param url:
    :param options:
    :return:
    """
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent': ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }
    headers = dict(base_headers, **options)
    print('正在抓取',url)
    try:
        response = requests.get(url, headers=headers)
        print('抓取成功', url, response.status_code)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('抓取失败', url)
        return None

class Downloader(object):
    """
    一个异步下载器，可以对代理源异步抓取，但是容易被BAN
    """

    def __init__(self, urls):
        self.urls = urls
        self._htmls = []

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                self._htmls.append(await response.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def htmls(self):
        self.download()
        return self._htmls