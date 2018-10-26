#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = 'myredisserver'

# Redis key
REDIS_KEY = 'myproxies'

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

# 代理池数量界限
POOL_LOWER_THRESHOLD = 20
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 60

# 获取周期
GETTER_CYCLE = 20

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True
CHECK_ENABLED = True

VALID_STATUS_CODES = [200, 302]

# 测试URL，建议爬取某个网站就测试相应站点
TEST_URL = 'http://www.baidu.com'

# API 配置
API_HOST = '127.0.0.1'
API_PORT = 5000

# 最大批量测试量
BATCH_TEST_SIZE = 100

# 代理超时限制
PROXY_TIMEOUT = 15

# 检查周期
VALID_CHECK_CYCLE = 60
POOL_LEN_CHECK_CYCLE = 20