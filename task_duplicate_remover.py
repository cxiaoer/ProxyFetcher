# coding:utf-8
"""
常用的去重操作
1: hashset 去重
2: redis去重
"""

import hashlib
from threading import RLock

url_md5_set = set()  # url的md5集合
__lock = RLock()  # 将查询和添加set封装成原子操作的锁


# url的md5的32位16进制表示
def __url_md5(url):
    md5 = hashlib.md5()
    trim_url = str.strip(url)
    md5.update(trim_url.encode())
    result = md5.hexdigest()
    return result


def hashset_duplicate_remover(url):
    """
    hashset 去重

    :param url: 要访问的url;  比如http://www.baidu.com
    :return:
    """

    url_md5 = __url_md5(url=url)
    with __lock:
        if url_md5 in url_md5_set:
            is_url_crawled = True
        else:
            is_url_crawled = False
            url_md5_set.add(url_md5)
    return is_url_crawled


def redis_duplicate_remover(url):
    """
    redis 去重

    :param url: 要访问的url;  比如http://www.baidu.com
    :return:
    """

    pass


if __name__ == '__main__':
    print(__url_md5("hello,world"))
    print(__url_md5("hello,world"))
    print(__url_md5("hello"))
