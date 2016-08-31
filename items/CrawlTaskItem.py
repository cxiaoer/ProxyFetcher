# coding:utf-8
"""
抓取任务的类表示
"""


class CrawlTaskItem(object):
    """抓取任务的抽象"""

    def __init__(self, site, url):
        super(CrawlTaskItem, self).__init__()
        self.site = site
        self.url = url
