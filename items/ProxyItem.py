# coding:utf-8


class ProxyItem(object):
    """抓取任务的抽象"""

    def __init__(self, **kwargs):
        super(ProxyItem, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return '&'.join([key + '=' + value for (key, value) in
                         self.__dict__.items()])
