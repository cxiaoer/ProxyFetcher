# coding:utf-8
import socket
from proxy_item_dao import get_need_test_proxy, update_proxy_status
from configs import logger_config

logger = logger_config.get_logger(__name__)  # 日志配置


# 检测ip
def test():
    while True:
        need_test_proxy_list = get_need_test_proxy(num=100)
        if len(need_test_proxy_list) > 0:
            for proxy in need_test_proxy_list:
                if ping(host=proxy['ip'], port=proxy['port']):
                    pass


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
