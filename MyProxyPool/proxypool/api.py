#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

from flask import Flask, g
from .db import RedisClient


__all__ = ['app']

app = Flask(__name__)

def get_conn():
    """
    Open a new redis connection if there is none yet for the current application context
    """
    if not hasattr(g, 'redis_client'):
        g.redis_client = RedisClient()
    return g.redis_client

@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System 2.0</h2>'

@app.route('/random')
def get_proxy_byRandom():
    """
    获取随机的代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    """
    获取代理池总量
    :return: 代理池总量
    """
    conn = get_conn()
    return str(conn.count())

@app.route('/list')
def get_list():
    """
    Get a list
    :return: 所有代理
    """
    conn = get_conn()
    return str(conn.all())

@app.route('/flush')
def get_counts():
    """
    获取代理池总量
    :return: 代理池总量
    """
    conn = get_conn()
    return conn.flush()

if __name__=='__main__':
    app.run()