#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
    
    @version: 1.0
    @author: phping
    @contact: liuyongfei198805@gmail.com
    @time: 17/03/21 下午13:35
"""

import scrapy
from scrapy import Selector
from scrapy import Request


class NgaSpider(scrapy.Spider):
    name = "NgaSpider"
    host = "http://bbs.ngacn.cc/"
    # 这个例子中只指定了一个页面作为爬取的起始url
    # 当然从数据库或者文件或者什么其他地方读取起始url也是可以的
    start_urls = [
        "http://bbs.ngacn.cc/thread.php?fid=406",
    ]

    # 爬虫的入口，可以在此进行一些初始化工作，比如从某个文件或者数据库读入起始url
    def start_requests(self):
        for url in self.start_urls:
            # 此处将起始url加入scrapy的待爬取队列，并指定解析函数
            # scrapy会自行调度，并访问该url然后把内容拿回来
            yield Request(url=url, callback=self.parse_page)

    # 版面解析函数，解析一个版面上的帖子的标题和地址
    def parse_page(self, response):
        selector = Selector(response)
        content_list = selector.xpath("//*[@class='topic']")
        for content in content_list:
            topic = content.xpath('string(.)').extract_first()
            print topic
            url = self.host + content.xpath('@href').extract_first()
            print url
            # 此处，将解析出的帖子地址加入待爬取队列，并指定解析函数
            yield Request(url=url, callback=self.parse_topic)
            # 可以在此处解析翻页信息，从而实现爬取版区的多个页面

    # 帖子的解析函数，解析一个帖子的每一楼的内容
    def parse_topic(self, response):
        selector = Selector(response)
        content_list = selector.xpath("//*[@class='postcontent ubbcode']")
        for content in content_list:
            content = content.xpath('string(.)').extract_first()
            print content
            # 可以在此处解析翻页信息，从而实现爬取帖子的多个页面