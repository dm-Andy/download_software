import requests
import os
import json
from const import *
import sys
from queue import Queue
from threading import Thread


def main():
    # 检查数据源文件是否存在
    check()

    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        #把数据放到队列
        queue_link = Queue()
        [queue_link.put(x) for x in data if x.get('download') == True]
        
        # 记录下载内容
        log = {'success':[], 'pass':[], 'not_pass':[]}

        th_list = []
        # 开启线程
        for x in range(THREAD_COUNT):
            th = DownloadThread(queue_link, log)
            th.start()
            th_list.append(th)
        
        for x in th_list:
            x.join()

        print('=' * 30)
        print('done...')
        success_ = [x.lower() for x in log['success']].sort()
        pass_ = [x.lower() for x in log['pass']].sort()
        not_pass_ = [x.lower() for x in log['not_pass']].sort()

        print('【下载成功】：%s' % success_)
        print('【文件大小认证通过】：%s' % pass_)
        print('【文件大小认证未通过】：%s' % not_pass_)

    except Exception as ex:
        print('发生异常：%s' % ex)
        sys.exit(2)


class DownloadThread(Thread):
    def __init__(self, queue_link, log):
        self.queue_link = queue_link
        self.log = log
        super(DownloadThread, self).__init__()
    
    def run(self):
        while not self.queue_link.empty():
            item = self.queue_link.get(block=False)
            self.pre_download(item)

    def pre_download(self, item):
        name = item['name']
        category = item['category']
        downloadUrl = item['downloadUrl']
        latest_url = item.get('latest_url')

        # 获取最终的下载地址 
        if downloadUrl:
            link = downloadUrl
        if latest_url:
            link = latest_url
           
        size, link = self.get_file_size(link)

        if size < DOWNLOAD_MAX_SIZE:
            self.log['pass'].append(name)
            self.download(link, category, size)
        else:
            self.log['not_pass'].append(name)
        
    def get_file_size(self, url):
        res = requests.head(url, headers=UA)
        location = res.headers.get('location')

        # 避免重定向死循环，只get两次
        if location:
            print('---------------location 1  %s' % location)
            url = location # 如果有302，获取最终下载链接
            res = requests.head(location, headers=UA)
            location = res.headers.get('location')
            if location:
                print('---------------location 2  %s' % location)
                url = location # 如果有302，获取最终下载链接
                res = requests.head(location, headers=UA)
            
        size = res.headers.get('Content-Length')
        if size:
            return (int(size) / 1024 /1024, url)
        else:
            # 到这里有两种情况：1. 返回的并不是下载链接，而是网页 2. 像亚马逊那种，发送head请求服务器返回是错误的，而且链接尾部也不是文件名
            return (0, url)

    def download(self, link, category, size):
        if not os.path.exists(FILES_STORE):
            os.mkdir(FILES_STORE)

        full_path = os.path.join(FILES_STORE, category)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
        try:
            res = requests.get(link, headers=UA)

            if size <= 0:
                temp = res.headers.get('Content-Disposition')
                if temp:
                    file_name = temp.split('=')[-1]
                else:
                    print('【解析错误，服务器返回可能是网页】 %s' % link)
                    return False
            else:
                file_name = os.path.split(link)[1]

            full_name = '%s/%s' % (full_path, file_name)

            with open(full_name, 'wb') as f:
                f.write(res.content)

            self.log['success'].append(file_name)
            print('【%s】下载完成' % file_name)

        except Exception as ex:
            print('下载错误：%s' % ex)

def check():
    if not os.path.exists(DATA_PATH):
        print('data.json 不存在，请先添加数据源')
        sys.exit(1)


if __name__ == "__main__":
    main()
