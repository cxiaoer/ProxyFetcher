# coding:utf-8
"""
代理对象的类表示
"""

from peewee import *
from configs import db_config
import datetime

db = MySQLDatabase(db_config.db,
                   user=db_config.db_username,
                   host=db_config.db_host,
                   password=db_config.db_password)


class ProxyItem(Model):
    """抓取任务的抽象"""
    record_id = BigIntegerField(db_column='RecordId', primary_key=True)
    ip = CharField(db_column='Ip')
    port = CharField(db_column='Port')
    proxy_type = CharField(db_column='ProxyType')
    location = CharField(db_column='Location')
    status = IntegerField(db_column='Status')
    success_test_times = IntegerField(db_column='SuccessedTestTimes')
    failed_test_times = IntegerField(db_column='FailedTestTimes')
    next_test_time = DateTimeField(db_column='NextTestTime', default=datetime.datetime.now())
    last_modify_time = DateTimeField(db_column='LastModifyTime', default=datetime.datetime.now())
    create_time = DateTimeField(db_column='CreateTime', default=datetime.datetime.now())

    class Meta:
        """Meta"""
        database = db
        db_table = 'T_IP_Proxies'
        indexes = (
            # ip 和 port 的唯一索引
            (('ip', 'port'), True),
        )


if __name__ == '__main__':
    item = ProxyItem.select().where(ProxyItem.ip == '182.89.7.212' and ProxyItem.proxy_type == 'HTTP').get()
    print(item.ip)
    item1 = ProxyItem(ip='test', port='test')
    item2 = ProxyItem(ip='test', port='test')
    item1.save()
    item2.save()
