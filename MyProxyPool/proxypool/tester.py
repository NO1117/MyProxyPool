#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import asyncio
import aiohttp
import time
import sys
from .db import RedisClient
from .setting import *
try:
    from aiohttp import ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectorError, ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectorError, ClientError

class ValidityTester(object):
    test_url = TEST_URL

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []
        self._redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        异步测试单个代理
        test on proxy by async, if valid, put them to usable_proxies
        :param proxy:代理
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试代理：',proxy)
                async with session.get(self.test_url, proxy=real_proxy, timeout=PROXY_TIMEOUT, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODES:
                        self._redis.max(proxy)
                        # self._redis.put(proxy)
                        print('代理{}可用'.format(proxy))
                    else:
                        self._redis.decrease(proxy)
                        print(response.status,'请求响应码不合法, IP:', proxy)
            except (ServerDisconnectedError, ClientResponseError, ClientError, ClientConnectorError, asyncio.TimeoutError, AttributeError) as e:
                self._redis.decrease(proxy)
                print('代理请求失败,分数减一', proxy)
                print(e)

    def run(self):
        """
        测试主函数
        aio test all proxies
        :return:
        """
        print('测试器开始运行')
        try:
            count = self._redis.count() #
            print("当前剩余{}个代理",format(count))
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i + BATCH_TEST_SIZE, count)
                print('正在测试第{0}-{1}个代理'.format(start + 1, stop))
                test_proxies = self._redis.batch(start, stop)
                loop = asyncio.get_event_loop()
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print("测试器发生错误", e.args)