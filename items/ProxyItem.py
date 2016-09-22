# coding:utf-8
"""
代理对象的类表示
"""

from sqlalchemy import Column, BigInteger, Integer, String, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import sessionmaker
from configs import db_config

# 对象的基类
Base = declarative_base()
# 初始化数据库连接
mysql_str_format = 'mysql+pymysql://{username}:{password}@{host}:3306/{db}'
engine = create_engine(mysql_str_format.format(username=db_config.db_username,
                                               password=db_config.db_password,
                                               host=db_config.db_host,
                                               db=db_config.db))


# 会话
DBSession = sessionmaker(bind=engine)


class ProxyItem(Base):
    """抓取任务的抽象"""

    # 连接对应的表名
    __tablename__ = 'T_IP_Proxies'

    record_id = Column('RecordId', BigInteger, primary_key=True)
    ip = Column('Ip', String)
    port = Column('Port', String)
    proxy_type = Column('ProxyType', String)
    location = Column('Location', String, nullable=True)
    status = Column('Status', Integer, server_default=text('0'))
    success_test_times = Column(
        'SuccessedTestTimes', Integer, server_default=text('0'))
    failed_test_times = Column(
        'FailedTestTimes', Integer, server_default=text('0'))
    next_test_time = Column('NextTestTime', DateTime,
                            server_default=text('now()'))
    last_modify_time = Column(
        'LastModifyTime', DateTime, server_default=text('now()'))
    create_time = Column('CreateTime', DateTime,
                         server_default=text('now()'))


if __name__ == '__main__':
    session = DBSession()
    proxy_items = session.query(ProxyItem).filter(
        ProxyItem.ip == '1.0.247.171').all()
    print(type(proxy_items))
    # print(proxy_item.ip)
    for item in proxy_items:
        print(type(item))
        print(item.ip)
    session.close()
