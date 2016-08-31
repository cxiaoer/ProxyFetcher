# coding:utf-8

import random

user_agent_list = []
user_agent_list.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                       'AppleWebKit/601.7.7 (KHTML, like Gecko) '
                       'Version/9.1.2 Safari/601.7.7')
user_agent_list.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/51.0.2704.106 Safari/537.36')


# 随机获取一个user_agent
def get_user_agent():
    length = len(user_agent_list)
    random_index = random.randint(0, length - 1)
    return user_agent_list.index(random_index)
