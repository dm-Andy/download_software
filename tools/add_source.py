import json
import argparse
import os
from const import DATA_PATH


def main():
    parse = argparse.ArgumentParser(description='添加下载软件的数据源')

    parse.add_argument('name', help='软件名称')
    parse.add_argument('category', help='软件类别')
    parse.add_argument('-desc', help='软件介绍')
    parse.add_argument('-downloadUrl', help='软件的下载地址，可以直接设置此值，但是不保证软件是最新版。设置此选项将直接下载不在解析xpath以及css')
    parse.add_argument('-url', help='下载页面链接')
    parse.add_argument('--xpath', help='下载按钮的xpath（与css二选一即可）')
    parse.add_argument('--css', help='下载按钮的css（与xpath二选一即可）')
    parse.add_argument('-d', dest='download', default=False, action='store_true', help='是要下载还是仅仅维护一个软件来源信息，默认是不下载')

    params = parse.parse_args()

    try:
        data ={
            'name': params.name,
            'desc': params.desc,
            'category': params.category,
            'downloadUrl': params.downloadUrl,
            'url': params.url,
            'xpath': params.xpath,
            'css': params.css,
            'download': params.download
        }
        if not os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                f.write(json.dumps([data]))
        else:
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                local_data = json.loads(f.read())
                local_data.append(data)
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                f.write(json.dumps(local_data, indent=4, separators=(',', ':')))
        
    except Exception as ex:
        print('发生异常：%s' % ex)


if __name__ == "__main__":
    main()

