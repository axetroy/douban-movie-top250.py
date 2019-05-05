# -*- coding: utf-8 -*-

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 123,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'douban.middlewares.AgentPoolProxyMiddleware': 124,
    'douban.middlewares.IpPoolProxyMiddleware': 125
}

DOWNLOAD_DELAY = 0.25
