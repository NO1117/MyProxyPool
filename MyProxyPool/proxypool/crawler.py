#!/usr/bin/env/ python 
# -*- coding:utf-8 -*-
# Author:Mr.Xu

import re
from .utils import get_page
from pyquery import PyQuery as pq

class ProxyMetaclass(type):
    """
    元类，在FreeProxyGetter类中加入__CrawlFunc__和__CrawlFuncCount__连个参数，分别表示爬虫函数和爬虫函数的数量
    """
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class FreeProxyCrawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print("Getting: {0} from {1}".format(proxy, callback))
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self):
        """
        获取66ip
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, 4)]
        for url in urls:
            print("Crawling: ",url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc(".containerbox table tr:gt(0)").items()
                for tr in trs:
                    ip = tr.find('td:nth_child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        """
        获取Goubanjia
        :return: 代理
        """
        start_url = 'http://www.goubanjia.com'
        print("Crawling: ", start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc("td.ip']").items()
            for td in tds:
                ip = td.find('p').remove()
                yield td.text().replace(' ', '')

    def crawl_ip3366(self):
        """
        获取ip3366
        :return: 代理
        """
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            print("Crawling: ", start_url)
            html = get_page(start_url)
            ip_address = re.compile("<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>") # \s*匹配空格,起到换行的作业
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_kuaidaili(self):
        """
        获取kuaidaili,国内高匿代理
        :return: 代理
        """
        for page in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(page)
            print("Crawling: ", start_url)
            html = get_page(start_url)
            if html:
                ip_address = re.compile("<td data-title='IP'>(.*?)</td>")
                re_ip_address = ip_address.findall(html)
                port = re.compile("<td data-title='PORT'>(.*?)</td>")
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    result = address + ':' + port
                    yield result.replace(' ', '')

    def crawl_xicidaili(self):
        """
        获取xicidaili
        :return: 代理
        """
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
            'Host': 'www.xicidaili.com',
            'Referer': 'http://www.xicidaili.com/nn/3',
            'Upgrade-Insecure-Requests': '1',
        }
        for page in range(1, 4):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(page)
            print("Crawling: ", start_url)
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    ip_address = re.compile("<td>(\d+\.\d+\.\d+\.\d+)</td>")
                    re_ip_address = ip_address.findall(tr)
                    port = re.compile("<td>(\d+)</td>")
                    re_port = port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        result = address + ':' + port
                        yield result.replace(' ', '')

    def crawl_iphai(self):
        """
        获取iphai
        :return: 代理
        """
        start_url = 'http://www.iphai.com/'
        print("Crawling: ",start_url)
        html = get_page(start_url)
        if html:
            find_trs = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_trs.findall(html)
            for tr in range(1, len(trs)):
                ip_address = re.compile("<td>\s(\d+\.\d+\.\d+\.\d+)\s</td>", re.S)
                re_ip_address = ip_address.findall(trs[tr])
                port = re.compile("<td>\s(\d+)\s</td>", re.S)
                re_port = port.findall(trs[tr])
                for address, port in zip(re_ip_address, re_port):
                    result = address + ':' + port
                    yield result.replace(' ', '')

    def crawl_89ip(self):
        """
        获取89ip
        :return: 代理
        """
        for page in range(1, 4):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(page)
            print("Crawling: ", start_url)
            html = get_page(start_url)
            ip_address = re.compile("<tr>\s*<td>\s(\d+\.\d+\.\d+\.\d+)\s</td>") # \s*匹配空格,起到换行的作业
            re_ip_address = ip_address.findall(html)
            port = re.compile("<td>\s(\d+)\s</td>")
            re_port = port.findall(html)
            for address, port in zip(re_ip_address, re_port):
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_data5u(self):
        """
        获取data5u
        :return: 代理
        """
        start_url = 'http://www.data5u.com/free/gngn/index.shtml'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
            'Host': 'www.data5u.com',
            'Referer': 'http://www.data5u.com/free/index.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        }
        print("Crawling: ",start_url)
        html = get_page(start_url, options=headers)
        if html:
            ip_address = re.compile("<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\'port.*?>(\d+)</li>", re.S)
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')