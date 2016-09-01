# coding:utf-8
""" 代理的db操作

批量查询; 更新状态
"""

import MySQLdb

from SimpleConnectionPool import SimpleConnectionPool
from configs import db_config
from configs.logger_config import get_logger
from items.ProxyItem import ProxyItem

logger = get_logger(__name__)  # 日志配置
# 数据库连接池
connection_pool = SimpleConnectionPool(host=db_config.db_host,
                                       db=db_config.db,
                                       username=db_config.db_username,
                                       password=db_config.db_password,
                                       max_connection_size=db_config.max_connection_size)


def batch_insert_proxy(ip_list):
    """批量插入ip 列表, 直接ignore掉duplication记录

    :param ip_list: :class:`ProxyItem` object list
    :return
    """

    insert_sql = 'insert ignore into T_IP_Proxies (Ip, Port, ProxyType, Location)  ' \
                 'values (%s, %s, %s, %s) '
    ip_info_list = [(ip.ip, ip.port, ip.proxy_type, ip.ip_location)
                    for ip in ip_list]
    connection = connection_pool.get_connection(timeout=5)  # 获取连接,超时5秒钟
    try:
        cursor = connection.cursor()
        cursor.executemany(insert_sql, ip_info_list)
        connection.commit()
    finally:
        connection_pool.free_connection(connection=connection)


def get_need_test_proxy(num):
    """读取检测任务

    :param num: 每次读取多少数量的代理信息
    :return :return: :class:`ProxyItem` object list
    """

    need_test_proxy_list = []
    # 每次取100个检测任务
    select_sql = 'select Ip as ip, Port as port, SuccessedTestTimes as success_test_times,' \
                 'FailedTestTimes as fail_test_times,' \
                 'ProxyType as proxy_type, LastModifyTime as last_modify_time ' \
                 'from T_IP_Proxies ' \
                 'where NextTestTime < now() and Status = 0 ' \
                 'order by NextTestTime asc ' \
                 'limit %s'
    connection = connection_pool.get_connection(timeout=5)  # 获取连接,超时5秒钟
    try:
        cursor = connection.cursor()
        cursor.execute(select_sql, (num,))
        columns = cursor.description
        result = [{columns[index][0]: column for index, column in enumerate(value)}
                  for value in cursor.fetchall()]
        for item in result:
            update_sql = 'update T_IP_Proxies set Status = 2, ' \
                         'LastModifyTime = now() ' \
                         'where Ip = %s and Port = %s and LastModifyTime = %s'
            cursor.execute(update_sql, (item['ip'], item['port'],
                                        str(item['last_modify_time'])))
            connection.commit()
            # 乐观锁
            if cursor.rowcount > 0:
                need_test_proxy_list.append(ProxyItem(ip=item['ip'],
                                                      port=item['port'],
                                                      proxy_type=item['proxy_type'],
                                                      fail_test_times=item['fail_test_times']))
    except MySQLdb.Error as error:
        logger.exception('[读取检测任务] 抛异常', error)
    finally:
        connection_pool.free_connection(connection=connection)
    return need_test_proxy_list


def get_need_reset_proxy(num, timeout):
    """获取需要重置的代理列表

    :param num: 每次读取多少数量的需要重置的代理信息
    :param timeout: 任务超时时间; 一旦超时,重置任务
    :return: :class:`ProxyItem` object list
    """

    need_reset_proxy_list = []
    select_sql = 'select Ip as ip, Port as port, SuccessedTestTimes as success_test_times,' \
                 'FailedTestTimes as fail_test_times,' \
                 'ProxyType as proxy_type, LastModifyTime as last_modify_time ' \
                 'from T_IP_Proxies ' \
                 'where NextTestTime < now() + %s and Status = 2 ' \
                 'order by LastModifyTime asc ' \
                 'limit %s'
    connection = connection_pool.get_connection(timeout=5)  # 获取连接,超时5秒钟
    try:
        cursor = connection.cursor()
        cursor.execute(select_sql, (timeout, num))
        columns = cursor.description
        need_reset_proxy_list = [{columns[index][0]: column for index, column in enumerate(value)}
                                 for value in cursor.fetchall()]
    except MySQLdb.Error as error:
        logger.exception('[重置代理] 抛异常', error)
    finally:
        connection_pool.free_connection(connection=connection)
    return need_reset_proxy_list


def update_proxy_status(ip_info_list):
    """检测完更新每个ip状态；包括状态以及下次检测时间，成功或失败次数

    :param ip_info_list: :class:`ProxyItem` object list
    :return
    """

    connection = connection_pool.get_connection(timeout=5)  # 获取连接,超时5秒钟
    try:
        cursor = connection.cursor()
        for ip_info in ip_info_list:
            update_sql = "update T_IP_Proxies set "
            if not isinstance(ip_info, ProxyItem):
                raise Exception
            if ip_info.status is not None:
                update_sql += "Status = {0}, ".format(ip_info.status)
            if ip_info.next_test_time is not None:
                update_sql += "NextTestTime = '{0}', ".format(ip_info.
                                                              next_test_time)
            if ip_info.success_test_times is not None:
                update_sql += "SuccessedTestTimes={0},".format(ip_info.
                                                               success_test_times)
            if ip_info.fail_test_times is not None:
                update_sql += "FailedTestTimes ={0}, ".format(ip_info.
                                                              fail_test_times)
            update_sql += "LastModifyTime = NOW() where Ip='{0}' " \
                          'and Port = {1}'.format(ip_info.ip,
                                                  ip_info.port)
            print update_sql
            cursor.execute(update_sql)
            connection.commit()
    except MySQLdb.Error as error:
        print error
        logger.exception('[更新任务状态] 抛异常')
    finally:
        connection_pool.free_connection(connection=connection)
