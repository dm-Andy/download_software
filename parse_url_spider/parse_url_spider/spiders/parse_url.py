# -*- coding: utf-8 -*-
import scrapy
import json
import sys
from scrapy import Request
from scrapy.conf import settings
from parse_url_spider.items import ParseUrlItem
from scrapy_splash import SplashRequest
from urllib import parse
import requests


class ParseUrlSpider(scrapy.Spider):
    name = 'parse_url'
    allowed_domains = []

    try:
        data_path = settings['DATA_PATH']
        with open(data_path ,'r', encoding='utf-8') as f:
            data = json.loads(f.read())
    except:
        print('数据源data.json不存在')
        sys.exit(1)

    start_urls = []
    
    def start_requests(self):
        for item in self.data:
            # 没有下载地址的，进行解析，排除不下载的
            if not item['downloadUrl'] and item.get('download'):
                # 有些下载链接都是js生成的，需要等待js渲染完成之后再获取
                yield SplashRequest(item['url'], callback=self.parse, meta={'name':item['name']}, args={'wait': 5})
    
    def parse(self, response):
        name = response.meta['name']
        item = ParseUrlItem()

        line = [x for x in self.data if x['name'] == name][0]
        xpath = line['xpath']
        css = line['css']
        
        if xpath:
            link = response.xpath(xpath).extract_first()
        if css:
            link = response.css(css).extract_first()
        
        # 判断链接是否包含HTTP
        if link.find('http') == -1:
            # 有的是直接url+href，有的需要解析域名然后在+href
            # /cmderdev/cmder/releases/download/v1.3.6/cmder.7z
            if link.find('/') == 0:
                node = parse.urlparse(line['url'])
                link = '%s://%s%s' % (node.scheme, node.netloc, link)
            else:
                link = line['url'] + link

        print('【%s】%s' % (name, link))
        item['name'] = name
        item['url'] = link

        yield item