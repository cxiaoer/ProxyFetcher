# coding:utf-8

import random

user_agent_list = []
user_agent_list.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                       'AppleWebKit/601.7.7 (KHTML, like Gecko) '
                       'Version/9.1.2 Safari/601.7.7')
user_agent_list.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/51.0.2704.106 Safari/537.36')
user_agent_list.append('Mozilla/5.0 (Windows NT 6.3; Win64, x64; '
                       'Trident/7.0; rv:11.0) like Gecko')
user_agent_list.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/44.0.2403.157 Safari/537.36')
user_agent_list.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; '
                       'rv:40.0) Gecko/20100101 Firefox/40.0')
user_agent_list.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64; '
                       'rv:40.0) Gecko/20100101 Firefox/40.0')
user_agent_list.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136')


# 随机获取一个user_agent
def get_user_agent():
    length = len(user_agent_list)
    random_index = random.randint(0, length - 1)
    return user_agent_list.index(random_index)
