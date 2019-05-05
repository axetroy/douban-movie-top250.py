# -*- coding: utf-8 -*-
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import requests
from fake_useragent import UserAgent

ua = UserAgent(use_cache_server=False)


class IpPoolProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, ip=''):
        self.ip = ip

    def process_request(self, request, spider):
        # 通过调用接口获取代理的 IP
        # https://github.com/jhao104/proxy_pool

        proxy = requests.get('http://localhost:5010/get').text

        print("当前使用IP是：" + proxy)

        request.meta["proxy"] = "http://" + proxy

class AgentPoolProxyMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        request.headers['User-Agent'] = ua.random
