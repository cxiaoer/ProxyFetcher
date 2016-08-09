# coding:utf-8

import MySQLdb
from configs import db_config
import time
from configs.logger_config import *
import threading

# 日志配置
logger = get_logger(__name__)
# 连接池, 采用list结构,更好记录每个链接的状态
connection_pool = []
# 连接池锁
__connection_lock = threading.Lock()


# 获取连接
def get_connection():
    current_time = time.time()
    with __connection_lock:
        while True:
            interval = time.time() - current_time
            # 10s内没有获取到连接,直接抛异常
            if interval > 10:
                logger.error('[获取数据库连接] 获取数据库连接超时[10秒]')
                raise Exception
            for (index, connection_dict) in enumerate(connection_pool):
                if connection_dict['status'] == 1:
                    continue
                logger.info('[获取数据库连接] 获取到空闲连接, index=%s', index)
                return (index, connection_dict)
            # 连接全部处于被占用的情况或者木有连接, 可以新建一个连接放置在里面
            if len(connection_pool) <= db_config.max_connection_size:
                logger.warn('[获取数据库连接] 没有空闲连接, 新建一个连接')
                connection_dict = init_db_connection()
                connection_dict['status'] = 1  # 标记为使用中
                connection_pool.append(connection_dict)
                return (connection_pool.index(connection_dict), connection_dict)


# 释放连接
def release_connection(index):
    connection_pool[index]['status'] = 0  # 重新标记为可用
    connection_pool[index]['time'] = time.time()  # 重新记录使用时间


# 初始化一个连接
def init_db_connection():
    connection_dict = {}
    connection = MySQLdb.connect(host=db_config.db_host,
                                 user=db_config.db_username,
                                 passwd=db_config.db_password,
                                 db=db_config.db)
    connection_dict['connection'] = connection
    connection_dict['status'] = 0  # 0 - 此连接可用;1-正在使用中
    connection_dict['time'] = time.time()  # 记录使用时间
    return connection_dict


# 批量插入ip 列表, 直接ignore掉duplication记录
def batch_insert_ip(ip_list):
    insert_sql = 'insert ignore into T_IP_Proxies (Ip, Port, ProxyType, Location)  ' \
                 'values (%s, %s, %s, %s) '
    ip_info_list = [(ip.ip, ip.port, ip.proxy_type, ip.ip_location) for ip in ip_list]
    (index, connection_dict) = get_connection()
    connection = connection_dict['connection']
    try:
        cursor = connection.cursor()
        cursor.executemany(insert_sql, ip_info_list)
        connection.commit()
    finally:
        release_connection(index)