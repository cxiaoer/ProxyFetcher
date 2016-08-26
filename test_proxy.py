# coding:utf-8
import socket
from proxy_item_dao import get_need_test_proxy, update_proxy_status
from configs import logger_config
import copy
import time

logger = logger_config.get_logger(__name__)  # 日志配置


# 检测ip
def test():
    while True:
        need_test_proxy_list = get_need_test_proxy(num=100)
        if len(need_test_proxy_list) > 0:
            for proxy in need_test_proxy_list:
                tmp = copy.copy(proxy)
                is_success = False
                if ping(host=tmp.ip, port=tmp.port):
                    is_success = True
                setattr(tmp, 'next_test_time', time.time() + 10)
                if tmp.fail_test_times >= 100:  # 失败次数大于100直接置为无效代理
                    setattr(tmp, 'status', 1)
                update_proxy_status(is_success=is_success, ip_info_list=[tmp])


# ping 一个ip
def ping(host='127.0.0.1', port=8000, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        logger.info('[检测代理] 代理: %s port: %s 验证通过;', host, port)
        return True
    except Exception, e:
        logger.error('[检测代理] 代理: %s port: %s 无法connect;', host, port)
        return False
