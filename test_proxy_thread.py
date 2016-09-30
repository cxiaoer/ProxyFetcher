# coding:utf-8
""" 检测代理线程组
"""

import datetime

from check_proxy import check_visit_website
from configs import logger_config
from proxy_item_dao import get_need_test_proxy, update_proxy_status
from utils import *

logger = logger_config.get_logger(__name__)  # 日志配置


@thread_pool(thread_num=10)
def test():
    """
    检测ip
    :return:
    """

    while True:
        need_test_proxy_list = get_need_test_proxy(num=100)
        if len(need_test_proxy_list) == 0:
            logger.info('[代理检测] 暂时没有要检测的ip')
            time.sleep(2)
            continue
        update_list = []
        for proxy in need_test_proxy_list:
            # tmp = copy.deepcopy(proxy)
            proxy['last_modify_time'] = datetime.datetime.now()
            proxy['status'] = 0  # 先标记为需要检测
            proxy['next_test_time'] = datetime.datetime.now() + \
                datetime.timedelta(minutes=1)  # 一分钟后检测
            # if ping(host=tmp.ip, port=tmp.port, timeout=3):
            if check_visit_website(proxy, website='douban.com'):
                proxy['success_test_times'] += 1  # 成功次数加一
                proxy['failed_test_times'] = None
            else:
                if proxy['failed_test_times'] >= 100:  # 失败次数大于100直接置为无效代理
                    setattr(proxy, 'status', 1)
                proxy['failed_test_times'] += 1
                proxy['success_test_times'] = None
            update_list.append(proxy)
            update_proxy_status(update_list)


if __name__ == '__main__':
    test()
