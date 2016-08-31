# coding:utf-8
import socket
from proxy_item_dao import get_need_test_proxy, update_proxy_status
from configs import logger_config
import copy
import time
from check_proxy import ping, check_visit_website

logger = logger_config.get_logger(__name__)  # 日志配置


# 检测ip
def test():
    while True:
        need_test_proxy_list = get_need_test_proxy(num=100)
        if len(need_test_proxy_list) > 0:
            for proxy in need_test_proxy_list:
                tmp = copy.copy(proxy)
                setattr(tmp, 'status', 0)  # 先标记为需要检测
                is_success = False
                if ping(host=tmp.ip, port=tmp.port, timeout=3):
                    is_success = True
                setattr(tmp, 'next_test_time', time.strftime(
                    '%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 10)))
                if tmp.fail_test_times >= 100:  # 失败次数大于100直接置为无效代理
                    setattr(tmp, 'status', 1)
                update_proxy_status(is_success=is_success, ip_info_list=[tmp])
        else:
            logger.info('[代理检测] 暂时没有要检测的ip')
            time.sleep(2)


if __name__ == '__main__':
    test()
