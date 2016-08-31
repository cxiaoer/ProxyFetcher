# coding:utf-8

import hashlib


# url的md5的32位16进制表示
def __url_md5(url):
    md5 = hashlib.md5()
    md5.update(str.strip(url))
    result = md5.hexdigest()
    return result


# set 去重
def set_duplicate_remover(url):
    pass


# redis 去重
def redis_duplicate_remover(url):
    pass
