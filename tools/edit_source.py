import json
import argparse
import os
from operator import itemgetter
from itertools import groupby
import sys
from const import DATA_PATH


def main():

    parse = argparse.ArgumentParser(description='编辑下载软件的数据源')

    parse.add_argument('dest', help='要修改的name')
    parse.add_argument('-name', help='软件名称')
    parse.add_argument('-desc', help='软件介绍')
    parse.add_argument('-category', help='软件类别')
    parse.add_argument('-downloadUrl', help='软件的下载地址，可以直接设置此值，但是不保证软件是最新版。设置此选项将直接下载不在解析xpath以及css')
    parse.add_argument('-url', help='下载页面链接')
    parse.add_argument('-download', help='可选：true or false 是要下载还是仅仅维护一个软件来源信息，默认是不下载')
    parse.add_argument('--xpath', help='下载按钮的xpath（与css二选一即可）')
    parse.add_argument('--css', help='下载按钮的css（与xpath二选一即可）')

    params = parse.parse_args()

    try:
        if not os.path.exists(DATA_PATH):
            print('data.json 不存在，请先添加数据源')
            sys.exit(1)
        else:
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                local_data = json.loads(f.read())
                
                temp = [x for x in local_data if x['name'].upper() == params.dest.upper()]

                if len(temp) > 1:
                    print('key：%s 重复' % params.dest)
                elif not temp:
                    print('key：%s 不存在' % params.dest)
                else:
                    new_line = temp[0]
                    if params.name:
                        new_line['name'] = params.name
                    if params.desc:
                        new_line['desc'] = params.desc
                    if params.category:
                        new_line['category'] = params.category
                    if params.downloadUrl:
                        new_line['downloadUrl'] = params.downloadUrl
                    if params.url:
                        new_line['url'] = params.url
                    if params.xpath:
                        new_line['xpath'] = params.xpath
                    if params.css:
                        new_line['css'] = params.css
                    if params.download:
                        new_line['download'] = False if params.download.lower() == 'false' else True
                        
                    with open(DATA_PATH, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(local_data, indent=4, separators=(',', ':')))
        
    except Exception as ex:
        print('发生异常：%s' % ex)


if __name__ == "__main__":
    main()

