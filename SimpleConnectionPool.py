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
import uuid

logger = get_logger(__name__)  # 日志配置


class ConnectionWrapper(object):
    """数据连接的包装, 增加一些其他属性"""

    def __init__(self, connection, last_free_time):
        self.connection = connection
        self.last_free_time = last_free_time
        self.connection_id = str(uuid.uuid1())  # 生成唯一连接标识


class SimpleConnectionPool(object):
    """连接池对象"""

    available_connection_pool = []  # 用list数据结构来存放空闲连接
    active_num = 0  # 正在使用中的连接数目
    connection_lock = RLock()  # 可重入连接锁

    MAX_IDLE_TIME = 3600  # 一个连接最大闲置时间

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
        return connection

    # 获取一个连接
    def __get_connection(self):
        # 有空闲的连接,直接取出来使用
        if len(self.available_connection_pool) > 0:
            connection_wrapper = self.available_connection_pool.pop()
            logger.info('[连接池] 获取到一个空闲连接; connection_id:%s',
                        connection_wrapper.connection_id)
            last_free_time = connection_wrapper.last_free_time
            # 如果一个connection 1小时内没有被使用, 关闭并且丢弃这个连接
            if time.time() - last_free_time > self.MAX_IDLE_TIME:
                logger.warn('连接超时未使用, 主动关闭,并且重新获取; connection_id:%s',
                            connection_wrapper.connection_id)
                connection_wrapper.connection.close()
                self.__get_connection()
        # 当没有空闲的连接时, 正在使用中的连接数目小于最大连接数时, 直接新建一个
        elif self.active_num < self.max_connection_size:
            connection_wrapper = ConnectionWrapper(self.__new_connection(),
                                                   time.time())
            logger.info('[连接池] 新建一个连接; connection_id:%s',
                        connection_wrapper.connection_id)
        else:
            connection_wrapper = None
        if connection_wrapper.connection is not None:
            self.active_num += 1
        return connection_wrapper

    def get_connection(self, timeout):
        """
        同步获取连接,一段时间没有获取到连接,直接失败
        :param timeout:  获取连接超时时间
        :return:
        """

        current_time = time.time()
        with self.connection_lock:
            while True:
                interval = time.time() - current_time
                if interval > timeout:
                    logger.error('[连接池] 获取连接超时')
                    raise Exception
                connection_wrapper = self.__get_connection()
                if connection_wrapper is None:
                    logger.error('[连接池] 暂时没有可用连接')
                    continue
                return connection_wrapper

    def free_connection(self, connection_wrapper):
        """
        释放连接
        :param connection_wrapper:  数据库连接对象
        :return:
        """
        with self.connection_lock:
            connection_wrapper.last_free_time = time.time()
            self.available_connection_pool.append(connection_wrapper)
            self.active_num -= 1
            logger.info('[连接池] 释放一个可用连接; connection_id:%s',
                        connection_wrapper.connection_id)
