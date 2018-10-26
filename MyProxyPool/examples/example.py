import os
import sys
import requests
from bs4 import BeautifulSoup
from MyProxyPool.proxypool.setting import *

dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir)


def get_proxy():
    r = requests.get('http://{0}:{1}/random'.format(API_HOST, API_PORT))
    proxy = BeautifulSoup(r.text, "lxml").get_text()
    return proxy


def crawl(url, proxy):
    proxies = {'http': proxy}
    r = requests.get(url, proxies=proxies)
    return r.text


def main():
    proxy = get_proxy()
    html = crawl('http://docs.jinkan.org/docs/flask/', proxy)
    print(html)

if __name__ == '__main__':
    main()

