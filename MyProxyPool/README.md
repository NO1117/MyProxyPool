# ProxyPool

此代理池在获取IP的时候使用了Random方法按照分数高低随机获取代理使用，参照：[https://github.com/Python3WebSpider/ProxyPool](https://github.com/Python3WebSpider/ProxyPool)

## 安装

### 安装Python

至少Python3.5以上

### 安装Redis

安装好之后将Redis服务开启

### 配置代理池

```
cd proxypool
```

进入proxypool目录，修改settings.py文件

PASSWORD为Redis密码，如果为空，则设置为None

#### 安装依赖

```
pip3 install -r requirements.txt
```

#### 打开代理池和API

```
python3 run.py
```

## 获取代理


利用requests获取方法如下

```
import requests

PROXY_POOL_URL = 'http://localhost:5000/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
```

## 各模块功能

* api.py

  > API模块，启动一个Web服务器，使用Flask实现，对外提供代理的获取功能。


* crawler.py

  > 爬虫模块
  * class FreeProxyCrawler
    > 用于抓取代理源网站的代理，用户可复写和补充抓取规则。
  
  
* db.py

  > Redis数据库连接模块

  * class RedisClient

    > 数据库操作类，维持与StrictRedis的连接和对数据库有序聚合的增删改查，


* error.py

  > 异常模块

  * class ResourceDepletionError

    > 资源枯竭异常，如果从所有抓取网站都抓不到可用的代理资源，
    >
    > 则抛出此异常。

  * class PoolEmptyError

    > 代理池空异常，如果代理池长时间为空，则抛出此异常。


* getter.py

  > 添加模块

  * class Getter

    > 代理添加器，用来触发爬虫模块，对代理池内的代理进行补充，代理池代理数达到阈值时停止工作。
    

* importer.py

  > 添加模块（手工）
  
  
* schedule.py

  > 调度器模块

  * class Scheduler

    > 代理池启动类，运行RUN函数时，会创建四个进程，负责API接口开关，检测器开关，添加器开关，代理池内容的增加和更新。

* setting.py

  > 设置模块，包含数据块配置和模块开关，以及其他配置
  

* tester.py

  > 测试模块
   * class Tester

    > 异步检测类，可以对给定(全部)的代理的可用性进行异步检测。
  

* utils.py

  > 工具箱：包含一个请求器和一个异步下载器

## 项目参考

[https://github.com/WiseDoge/ProxyPool](https://github.com/WiseDoge/ProxyPool)
