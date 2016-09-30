# coding:utf-8
""" 代理的db操作

批量查询; 更新状态
"""

from configs.logger_config import get_logger
from items.ProxyItem import ProxyItem, session_factory
from session_manager import transactional_session, temp_session
import datetime

logger = get_logger(__name__)  # 日志配置


def batch_insert_proxy(ip_list):
    """批量插入ip 列表, 直接ignore掉duplication记录

    :param ip_list: :class:`ProxyItem` object list
    :return
    """
    if ip_list is None or len(ip_list) == 0:
        return
    for item in list(map(transferDicToItem, ip_list)):
        ip = item.ip
        port = item.port
        try:
            with transactional_session(session_factory=session_factory) \
                    as session:
                session.add(item)
        except Exception as e:
            msg = '插入代理:{}, 端口:{}失败'.format(ip, str(port))
            print(msg)
            print(e)


def get_need_test_proxy(num):
    """读取检测任务

    :param num: 每次读取多少数量的代理信息
    :return :return: :class:`ProxyItem` object list
    """
    items = []
    with transactional_session(session_factory=session_factory) as session:
        items = session.query(ProxyItem).filter(
            ProxyItem.next_test_time <= datetime.datetime.now(),
            ProxyItem.status == 0). \
            order_by(ProxyItem.next_test_time.asc()). \
            limit(num).all()
        # 判断每个代理任务是否已经被其他进程取走了
        for item in items:
            result = session.query(ProxyItem).filter(
                ProxyItem.ip == item.ip,
                ProxyItem.port == item.port,
                ProxyItem.status == item.status,
                ProxyItem.last_modify_time == item.last_modify_time). \
                update({'status': 2,
                        'last_modify_time': datetime.datetime.now()})
            if result > 0:  # 更新成功木有其他进程读取了这个任务
                items.append(item)
    return list(map(transferItemToDic, items))


def get_need_reset_proxy(num, timeout):
    """获取需要重置的代理列表

    :param num: 每次读取多少数量的需要重置的代理信息
    :param timeout: 任务超时时间; 一旦超时,重置任务
    :return: :class:`ProxyItem` object list
    """
    with temp_session(session_factory=session_factory) as session:
        items = session.query(ProxyItem).filter(
            ProxyItem.next_test_time <= datetime.datetime.now() -
            datetime.timedelta(hours=1),
            ProxyItem.status == 2). \
            order_by(ProxyItem.next_test_time.asc()). \
            limit(num).all()
        return list(map(transferItemToDic, items))


def update_proxy_status(ip_info_list):
    """检测完更新每个ip状态；包括状态以及下次检测时间，成功或失败次数

    :param ip_info_list: :class:`ProxyItem` object list
    :return
    """

    if len(ip_info_list) == 0:
        return
    for item in list(map(transferDicToItem, ip_info_list)):
        ip = item.ip
        port = item.port
        try:
            with transactional_session(session_factory=session_factory) \
                    as session:
                session.query(ProxyItem).filter(
                    ProxyItem.ip == ip,
                    ProxyItem.port == port). \
                    update({column: getattr(item, column)
                            for column in list(filter(lambda tmp: False
                                                      if tmp.startswith('_') or
                                                      getattr(
                                                          item, tmp) is None
                                                      else True,
                                                      ProxyItem.__dict__.keys()
                                                      ))
                            })
        except Exception as e:
            msg = '更新代理:{}, 端口:{}状态出错'.format(ip, str(port))
            print(msg)
            print(e)
            # logger.exception(msg, e)


def transferDicToItem(dic):
    """  字典转化成对象
    :param dic 代理信息对象字典
    """
    item = ProxyItem()
    # print(type(dic['location']))
    for key in dic.keys():
        setattr(item, key, dic[key])
    return item


def transferItemToDic(item):
    """  对象转化成字典
    :param item 代理信息对象字典
    """
    return {column: getattr(item, column)
            for column in list(filter(lambda tmp: False
                                      if tmp.startswith('_') or
                                      getattr(
                                          item, tmp) is None
                                      else True,
                                      ProxyItem.__dict__.keys()
                                      ))}


if __name__ == '__main__':
    # print(ProxyItem.__dict__.keys())
    # print(type(ProxyItem.__table__)
    res = get_need_reset_proxy(1, 1)
    print(type(res))
    for item in res:
        # logger.info('代理:%s', item.ip)
        tmp = {}
        tmp['ip'] = item['ip']
        tmp['port'] = item['port']
        tmp['next_test_time'] = datetime.datetime.now()
        # item[next_test_time] = datetime.datetime.now()
        tmp['status'] = 0
        update_proxy_status([{'ip': item['ip'],
                              'port': item['port'],
                              'next_test_time': datetime.datetime.now(),
                              'status': 0}, ])
    # item_1 = ProxyItem(ip='test1', port=9000)
    # item_2 = ProxyItem(ip='test2', port=9001)
    # item_3 = ProxyItem(ip='test2', port=9001)
    # batch_insert_proxy([item_1, item_2, item_3])
