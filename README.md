# download_software

1. 维护软件数据源，解析并下载
2. 分为两个部分:
    * tools：配置数据源，以及下载
    * spider：根据数据源配置解析最终的下载地址

> **环境依赖**

1. python3
2. scrapy_splash，其依赖于docker，所以这两个必须有

> **说明**

1. 修改`tools/const.py`里面的配置信息
2. 修改spider的settings
3. 先用tools里面的工具配置数据源信息
4. 利用爬虫解析软件的最终下载地址
5. 用tools里面的`download_software.py`进行下载
6. 在下载之前一定要更新`latest_url`，有的网站下载链接的目录是变化的
7. 添加数据源的时候，指定`-d`就是下载，默认不下载

