#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import time
from multiprocessing import Process
from .api import app
from .getter import Getter
from .tester import ValidityTester
from .setting import *
from .db import RedisClient

class Scheduler(object):

    def check_pool(lower_threshold=POOL_LEN_CHECK_CYCLE, upper_threshold=POOL_UPPER_THRESHOLD, cycle=POOL_LEN_CHECK_CYCLE):
        """
        if the number of proxies less then lower_threshold, add proxy
        :param lower_threshold:
        :param upper_threshold:
        :param cycle:
        :return:
        """
        conn = RedisClient()
        adder = Getter()
        while True:
            if conn.count() < lower_threshold:
                adder.adder()
            time.sleep(cycle)

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle:
        :return:
        """
        tester = ValidityTester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :param cycle:
        :return:
        """
        getter = Getter()
        while True:
            print('开始爬去代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        :return:
        """
        app.run(API_HOST, API_PORT)

    def run(self):
        print("代理池开始运行")

        if CHECK_ENABLED:
            check_process = Process(target=Scheduler.check_pool)
            check_process.start()

        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()