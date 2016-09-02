# coding:utf-8
"""
重置超时代理任务线程组
"""

import copy
from proxy_item_dao import get_need_reset_proxy, update_proxy_status
import time
from configs.logger_config import get_logger

logger = get_logger(__name__)  # 日志配置


def reset_timeout_proxy(timeout=600):
    """
    将数据库中由于超时或者抛出异常的代理状态由检测中->待检测
    :param timeout:  默认超时时间
    :return:
    """
    while 1:  # while 1比while true更快, 效率更高
        # 默认将超时时间设为10分钟
        need_test_proxy_list = get_need_reset_proxy(100, timeout=timeout)
        if len(need_test_proxy_list):
            logger.info('[代理检测] 暂时没有要检测的ip')
            time.sleep(600)
        update_list = []
        for ip_info in need_test_proxy_list:
            tmp = copy.copy(ip_info)
            tmp.success_test_times = None
            tmp.fail_test_times = None
            setattr(tmp, 'status', 0)
            setattr(tmp, 'next_test_time', time.time())
            update_list.append(tmp)
        update_proxy_status(update_list)
