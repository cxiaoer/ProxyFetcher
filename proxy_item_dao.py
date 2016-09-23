# coding:utf-8
""" 代理的db操作

批量查询; 更新状态
"""

from configs.logger_config import get_logger
from items.ProxyItem import ProxyItem, session_factory
from db_utils import transactional_session
import datetime

logger = get_logger(__name__)  # 日志配置


def batch_insert_proxy(ip_list):
    """批量插入ip 列表, 直接ignore掉duplication记录

    :param ip_list: :class:`ProxyItem` object list
    :return
    """

    pass


def get_need_test_proxy(num):
    """读取检测任务

    :param num: 每次读取多少数量的代理信息
    :return :return: :class:`ProxyItem` object list
    """

    results = []
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
                results.append(item)
    return results


def get_need_reset_proxy(num, timeout):
    """获取需要重置的代理列表

    :param num: 每次读取多少数量的需要重置的代理信息
    :param timeout: 任务超时时间; 一旦超时,重置任务
    :return: :class:`ProxyItem` object list
    """
    pass
    # need_reset_proxy_list = []
    # select_sql = 'select Ip as ip, Port as port, SuccessedTestTimes as success_test_times,' \
    #              'FailedTestTimes as fail_test_times,' \
    #              'ProxyType as proxy_type, LastModifyTime as last_modify_time ' \
    #              'from T_IP_Proxies ' \
    #              'where NextTestTime < now() + %s and Status = 2 ' \
    #              'order by LastModifyTime asc ' \
    #              'limit %s'
    # # 获取连接,超时5秒钟
    # connection_wrapper = connection_pool.get_connection(timeout=5)
    # connection = connection_wrapper.connection
    # try:
    #     cursor = connection.cursor()
    #     cursor.execute(select_sql, (timeout, num))
    #     columns = cursor.description
    #     need_reset_proxy_list = [{columns[index][0]: column for index, column in enumerate(value)}
    #                              for value in cursor.fetchall()]
    # except Error as error:
    #     logger.exception('[重置代理] 抛异常', error)
    # finally:
    #     connection_pool.free_connection(connection_wrapper=connection_wrapper)
    # return need_reset_proxy_list


def update_proxy_status(ip_info_list):
    """检测完更新每个ip状态；包括状态以及下次检测时间，成功或失败次数

    :param ip_info_list: :class:`ProxyItem` object list
    :return
    """

    pass
    # 获取连接,超时5秒钟
    # connection_wrapper = connection_pool.get_connection(timeout=5)
    # connection = connection_wrapper.connection
    # try:
    #     cursor = connection.cursor()
    #     for ip_info in ip_info_list:
    #         update_sql = "update T_IP_Proxies set "
    #         if not isinstance(ip_info, ProxyItem):
    #             raise Exception
    #         if ip_info.status is not None:
    #             update_sql += "Status = {0}, ".format(ip_info.status)
    #         if ip_info.next_test_time is not None:
    #             update_sql += "NextTestTime = '{0}', ".format(ip_info.
    #                                                           next_test_time)
    #         if ip_info.success_test_times is not None:
    #             update_sql += "SuccessedTestTimes={0},".format(ip_info.
    #                                                            success_test_times)
    #         if ip_info.fail_test_times is not None:
    #             update_sql += "FailedTestTimes ={0}, ".format(ip_info.
    #                                                           fail_test_times)
    #         update_sql += "LastModifyTime = NOW() where Ip='{0}' " \
    #                       'and Port = {1}'.format(ip_info.ip,
    #                                               ip_info.port)
    #         print(update_sql)
    #         cursor.execute(update_sql)
    #         connection.commit()
    # except Error as error:
    #     print(error)
    #     logger.exception('[更新任务状态] 抛异常')
    # finally:
    #     connection_pool.free_connection(connection_wrapper=connection_wrapper)


if __name__ == '__main__':
    res = get_need_test_proxy(1)
    print(res)
