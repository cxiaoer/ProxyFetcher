# coding:utf-8
"""
自动管理sqlachemy session
"""
from __future__ import with_statement

import contextlib
import functools


@contextlib.contextmanager
def temp_session(session_factory, **kwargs):
    """对于查等操作，不需要事务
    :param session_factory: sqlachemy session 工厂
    """
    session = session_factory(**kwargs)
    yield session


@contextlib.contextmanager
def transactional_session(session_factory, nested=True, **kwargs):
    """
     增删改用这个with语句
    :param session_factory: sqlachemy session 工厂
    :param nested: 是否开启savepoint transaction
    :param kwargs:
    :return:
    """
    session = session_factory(**kwargs)
    # session.begin(nested=True)
    try:
        yield session
        # 正常的话直接提交
        session.commit()
    except:
        # 抛出异常，回退
        session.rollback()
        raise
    finally:
        session.close()


def in_transaction(**session_kwargs):
    """
    增删改支持装饰器实现session管理
    :param session_kwargs:
    :return:
    """

    def outer_wrapper(func):
        """

        :param func:
        :return:
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """

            :param args:
            :param kwargs:
            :return:
            """
            with transactional_session(**session_kwargs):
                return func(*args, **kwargs)

        return wrapper

    return outer_wrapper
