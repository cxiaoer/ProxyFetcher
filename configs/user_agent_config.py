# coding:utf-8
"""
user-agent 解析和读取
"""

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

# opera
user_agent_list.append('Opera/9.80 (X11; Linux i686; Ubuntu/14.10) '
                       'Presto/2.12.388 Version/12.16')  # 12.16
user_agent_list.append('Opera/9.80 (Windows NT 6.0) '
                       'Presto/2.12.388 Version/12.14')  # 12.14
user_agent_list.append('Mozilla/5.0 (Windows NT 6.0; rv:2.0) '
                       'Gecko/20100101 Firefox/4.0 Opera 12.14')  # 12.14
user_agent_list.append('Mozilla/5.0 (compatible; MSIE 9.0; '
                       'Windows NT 6.0) Opera 12.14')  # 12.14


user_agent_list.append('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) '
                       'Gecko/20100101 Firefox/34.0')
user_agent_list.append('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; '
                       'rv:1.9.1.6) '
                       'Gecko/20091201 Firefox/3.5.6')
user_agent_list.append('Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 '
                       '(KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11')
user_agent_list.append('Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; '
                       'Trident/6.0)')
user_agent_list.append('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) '
                       'Gecko/20100101 Firefox/40.0')
user_agent_list.append('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 '
                       'Chrome/44.0.2403.89 Safari/537.36')


def get_user_agent():
    """
    随机获取一个user_agent
    :return:
    """
    # length = len(user_agent_list)
    # random_index = random.randint(0, length - 1)
    return random.choice(user_agent_list)


if __name__ == '__main__':
    for i in range(100):
        print(get_user_agent())
