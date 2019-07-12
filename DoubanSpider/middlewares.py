# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


import json
import logging
import requests
import random

# 阿布云
import base64
# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"
# 代理隧道验证信息
proxyUser = "H675C8U0H0073G1D"
proxyPass = "C039978C9A5F5F56"
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth


# 代理ip
# class ProxyMiddleware():
#     def __init__(self, proxy_url):
#         self.logger = logging.getLogger(__name__)
#         self.proxy_url = proxy_url
#
#     def get_random_proxy(self):
#         try:
#             response = requests.get(self.proxy_url)
#             if response.status_code == 200:
#                 proxy = response.text
#
#             # response = requests.get(self.proxy_url)
#             # if response.status_code == 200:
#             #     proxy_d = json.loads(response.text)
#             #     ip = proxy_d.get('ip')
#             #     port = proxy_d.get('port')
#             #     proxy = ip + ':' + port
#
#                 return proxy
#         except requests.ConnectionError:
#             return False
#
#     def process_request(self, request, spider):
#         # if request.meta.get('retry_times'):
#         # retry_count = 5
#         # while retry_count > 0:
#         #     try:
#                 proxy = self.get_random_proxy()
#                 if proxy:
#                     uri = 'https://{proxy}'.format(proxy=proxy)
#                     self.logger.debug('使用代理 ' + proxy)
#                     request.meta['proxy'] = uri
#             # except Exception:
#             #     retry_count -= 1
#             #     # 出错5次, 删除代理池中代理
#             # requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
#             # return None
#
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(
    #         proxy_url=settings.get('PROXY_URL')
    #     )


from fake_useragent import UserAgent
#随机UA
class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random
        # print(request.headers['User-Agent'])



