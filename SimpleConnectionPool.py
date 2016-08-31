# coding:utf-8
"""
自定义简单连接池管理
1: 获取连接
2: 释放连接
"""

import MySQLdb
import time
from threading import RLock
from configs.logger_config import get_logger

logger = get_logger(__name__)  # 日志配置
available_connection_pool = []  # 用list数据结构来存放空闲连接
active_num = 0  # 正在使用中的连接数目
connection_lock = RLock()  # 可重入连接锁


class ConnectionWrapper(object):
    """数据连接的包装, 增加一些其他属性"""

    def __init__(self, connection, last_free_time):
        self.connection = connection
        self.last_free_time = last_free_time


class SimpleConnectionPool(object):
    """连接池对象"""

    def __init__(self, host, db, username, password, max_connection_size):
        self.host = host
        self.db = db
        self.username = username
        self.password = password
        self.max_connection_size = max_connection_size

    # 初始化一个连接
    def __new_connection(self):
        connection = MySQLdb.connect(host=self.host,
                                     user=self.username,
                                     passwd=self.password,
                                     db=self.db)
        logger.info('[连接池] 新建一个连接')
        return connection

    # 获取一个连接
    def __get_connection(self):
        global active_num
        # 有空闲的连接,直接取出来使用
        if len(available_connection_pool) > 0:
            logger.info('[连接池] 获取到一个空闲连接')
            connection_wrapper = available_connection_pool.pop()
        # 当没有空闲的连接时, 正在使用中的连接数目小于最大连接数时, 直接新建一个
        elif active_num < self.max_connection_size:
            connection_wrapper = ConnectionWrapper(self.__new_connection(),
                                                   time.time())
        else:
            connection_wrapper = None
        if connection_wrapper.connection is not None:
            active_num += 1
        return connection_wrapper.connection

    def get_connection(self, timeout):
        """
        同步获取连接,一段时间没有获取到连接,直接失败
        :param timeout:  获取连接超时时间
        :return:
        """

        current_time = time.time()
        with connection_lock:
            while True:
                interval = time.time() - current_time
                if interval > timeout:
                    logger.error('[连接池] 获取连接超时')
                    raise Exception
                connection = self.__get_connection()
                if connection is None:
                    logger.error('[连接池] 暂时没有可用连接')
                    continue
                return connection

    def free_connection(self, connection):
        """
        释放连接
        :param connection:  数据库连接对象
        :return:
        """
        global active_num
        with connection_lock:
            available_connection_pool.append(ConnectionWrapper(connection,
                                                               time.time()))
            active_num -= 1
            logger.info('[连接池] 释放一个可用连接')
