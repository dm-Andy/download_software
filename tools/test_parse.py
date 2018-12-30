import requests
from lxml import etree
import argparse

def main():
    
    parse = argparse.ArgumentParser(description='测试xpath和css解析是否正确(js动态生成不能解析到)，注意格式：--xpath "xxx" ，外面用双引号，里面换成单引号')

    parse.add_argument('-url', help='下载页面链接')
    parse.add_argument('--xpath', help='下载按钮的xpath')
    parse.add_argument('--css', help='下载按钮的css')

    params = parse.parse_args()

    ua = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }

    if params.url is None:
        print('url是必须的，具体python test.py -h查看doc')
    else:
        html = requests.get(params.url, headers=ua).content

        data = etree.HTML(html)

        if params.xpath:
            temp = data.xpath(params.xpath)
            if len(temp) <=0:
                print('未解析到任何元素')
            else:
                for x in temp:
                    # 如果要解析的是元素
                    if type(x) == etree._Element:
                        print(etree.tostring(x, encoding='utf-8', method='html', pretty_print=True))
                    else:
                        # 解析的是元素的值或者其他
                        print(x)

        if params.css:
            temp = data.cssselect(params.css)
            if len(temp) <=0:
                print('未解析到任何元素')
            else:
                for x in temp:
                    if type(x) == etree._Element:
                        print(etree.tostring(x, encoding='utf-8', method='html', pretty_print=True))
                    else:
                        print(x)


if __name__ == "__main__":
    main()