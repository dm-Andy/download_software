# -*- coding: utf-8 -*-
from scrapy.conf import settings
import json

class ParseUrlSpiderPipeline(object):
    def process_item(self, item, spider):
        data_source = spider.settings['DATA_PATH']
        with open(data_source, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        line = [x for x in data if x['name'] == item['name']][0]

        # 更新最终下载地址为解析后的url
        line['latest_url'] = item['url']

        with open(data_source, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, indent=4, separators=(',', ':')))

        return item
