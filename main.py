# coding:utf-8
"""代理服务程序的主入口
"""

from fetch_proxy_thread import fetch, init
from test_proxy_thread import test

if __name__ == '__main__':
    init()  # 初始化任务
    fetch()  # 开始抓取代理
    test()  # 检测代理
