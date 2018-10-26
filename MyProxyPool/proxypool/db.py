#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import redis
import re
from random import choice
from .error import PoolEmptyError
from .setting import *

class RedisClient(object):

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis 密码
        """
        if password:
            self._db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        else:
            self._db = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def flush(self):
        """
        flush db
        :return:
        """
        self._db.flushall()

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理,设置分数为初始分数10
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not re.match(r'\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print("代理:{}不符合规范，丢弃".format(proxy))
            return
        if not self._db.zscore(REDIS_KEY, proxy):
            return self._db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
        随机获取代理，首先尝试获取最高分代理，如果最高分不存在，则按排名获取，否则报出异常
        :return: 随机代理
        """
        result = self._db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self._db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，分数小于最小值，则代理删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self._db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print("代理:{0},当前分数{1}，减1".format(proxy, score))
            return self._db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print("代理：{0}，当前分数{1}，删除".format(proxy, score))
            return self._db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在代理
        :param proxy: 代理
        :return: 是否存在
        """
        return self._db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print("代理:{0}可用，分数设置为{1}".format(proxy, MAX_SCORE))
        return self._db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
        获取代理总的数量
        :return: 数量
        """
        return self._db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self._db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self._db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__=='__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)

