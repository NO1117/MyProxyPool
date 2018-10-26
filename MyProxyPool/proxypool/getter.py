#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import sys
from .db import RedisClient
from .crawler import FreeProxyCrawler
from .tester import ValidityTester
from .error import ResourceDepletionError
from .setting import *

class Getter():

    def __init__(self):
        self._redis = RedisClient()
        self._tester = ValidityTester()
        self._crawler = FreeProxyCrawler()

    def is_over_threshold(self):
        """
        判断是都达到了代理池限制
        judge if count is overflow
        :return:
        """
        if self._redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def adder(self):
        print("PoolAdder is working")
        proxy_count = 0
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                proxies = self._crawler.get_proxies(callback)
                # test crawled proxies
                self._tester.run()
                proxy_count += len(proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
                for proxy in proxies:
                    self._redis.add(proxy)
            if proxy_count == 0:
                raise ResourceDepletionError

    def run(self):
        print("获取器开始执行")
        if not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self._crawler.get_proxies(callback)
                sys.stdout.flush()
                for proxy in proxies:
                    self._redis.add(proxy)