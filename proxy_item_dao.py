# coding:utf-8

from configs import logger_config
from SimpleConnectionPool import SimpleConnectionPool
from configs import db_config
from ProxyItem import ProxyItem
import MySQLdb

logger = logger_config.get_logger(__name__)  # 日志配置
# 数据库连接池
connection_pool = SimpleConnectionPool(host=db_config.db_host,
                                       db=db_config.db,
                                       username=db_config.db_username,
                                       password=db_config.db_password,
                                       max_connection_size=db_config.max_connection_size)


# 批量插入ip 列表, 直接ignore掉duplication记录
def batch_insert_proxy(ip_list):
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


# 读取检测任务
def get_need_test_proxy(num):
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


# 检测完更新每个ip状态；包括状态以及下次检测时间，成功或失败次数
def update_proxy_status(is_success, ip_info_list):
    connection = connection_pool.get_connection(timeout=5)  # 获取连接,超时5秒钟
    try:
        cursor = connection.cursor()
        for ip_info in ip_info_list:
            if is_success:
                update_sql = "update T_IP_Proxies set Status = %s, " \
                             "NextTestTime = '%s' , SuccessedTestTimes = " \
                             "SuccessedTestTimes +1 " \
                             "where Ip = '%s' and Port = '%s' " % (ip_info.status,
                                                                   ip_info.next_test_time, ip_info.ip,
                                                                   ip_info.port)
            else:
                update_sql = "update T_IP_Proxies set Status = %s, " \
                             "NextTestTime = '%s' , FailedTestTimes = " \
                             "FailedTestTimes +1 " \
                             "where Ip = '%s' and Port = '%s' " % (ip_info.status,
                                                                   ip_info.next_test_time, ip_info.ip,
                                                                   ip_info.port)
            print update_sql
            cursor.execute(update_sql)
            connection.commit()
    except MySQLdb.Error as error:
        print error
        logger.exception('[读取检测任务] 抛异常')
    finally:
        connection_pool.free_connection(connection=connection)
