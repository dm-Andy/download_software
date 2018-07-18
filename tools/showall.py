import json
import os
from operator import itemgetter
from itertools import groupby
from argparse import ArgumentParser
import sys
from const import DATA_PATH


def main():

    parse = ArgumentParser(description=__doc__)
    
    parse.add_argument('-c', dest='category', help='显示全部类别', default=False, action='store_true')

    parse.add_argument('-n', dest='name', help='显示指定类别下的软件')
    parse.add_argument('-d', dest='download', help='显示要下载的', default=False, action='store_true')
    parse.add_argument('-nd', dest='not_download', help='显示不要下载的', default=False, action='store_true')
    parse.add_argument('-a', dest='all', help='显示全部字段', default=False, action='store_true')
    params = parse.parse_args()

    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            # 根据类别进行排序
            data.sort(key=itemgetter('category'))
        
        # 显示全部类别
        if params.category: # type: boolean
            show_category(data)
        
        # 显示要下载的
        if params.download:
            show_download(data, params.name, params.all, True)

        # 显示不要下载的
        if params.not_download:
            show_download(data, params.name, params.all, False)

        # 显示指定类别下的软件，注意顺序，放在show_download后面，否则参数有-n的时候再加上参数-d -d过滤不起作用
        if params.name:
            show_info_with_category(params.name, params.all, data)
        
        # 显示全部
        for category,items in groupby(data,key=itemgetter('category')):
            show_info(category, params.all, items)
            
    except Exception as ex:
        print('发生异常：%s' % ex)

def show_category(data):
    lines = set([x['category'] for x in data])
    [print(x) for x in lines]
    sys.exit(0)
    
def show_info_with_category(name, all, data):
    for category,items in groupby(data,key=itemgetter('category')):
        if category == name:
            show_info(name, all, items)
            sys.exit(0)
    sys.exit(0)

def show_download(data, name, all, isdownload):
    data.sort(key=itemgetter('download'))
    for download,items in groupby(data,key=itemgetter('download')):
        if download == isdownload:
            download_items = list(items)
            download_items.sort(key=itemgetter('category'))
            for category,items_part in groupby(download_items,key=itemgetter('category')):
                # 查看某类别下要下载的
                if name:
                    if category == name:
                        show_info(category, all, items_part)
                        sys.exit(0)
                else:
                    show_info(category, all, items_part)
    sys.exit(0)
            
def show_info(category, all, items):
    print('    ' + category)
    if all:
        for x in items:
            print('-' * 50)
            print('name：%s' % x.get('name'))
            print('desc：%s' % x.get('desc'))
            print('category：%s' % x.get('category'))
            print('downloadUrl：%s' % x.get('downloadUrl'))
            print('url：%s' % x.get('url'))
            print('latest_url：%s' % x.get('latest_url'))
            print('xpath：%s' % x.get('xpath'))
            print('css：%s' % x.get('css'))
            print('download：%s' % x.get('download'))
    else:
        [print('%s: %s - %s' % (x.get('name'), x.get('desc'), x.get('url'))) for x in items]
    print()
    print()

if __name__ == "__main__":
    main()