# coding:utf-8

import hashlib
from threading import RLock

url_md5_set = set()  # url的md5集合
__lock = RLock()  # 将查询和添加set封装成原子操作的锁


# url的md5的32位16进制表示
def __url_md5(url):
    md5 = hashlib.md5()
    md5.update(str.strip(url))
    result = md5.hexdigest()
    return result


# set 去重
def set_duplicate_remover(url):
    url_md5 = __url_md5(url=url)
    with __lock:
        if url_md5 in url_md5_set:
            is_url_crawled = True
        else:
            is_url_crawled = False
            url_md5_set.add(url_md5)
    return is_url_crawled


# redis 去重
def redis_duplicate_remover(url):
    pass
