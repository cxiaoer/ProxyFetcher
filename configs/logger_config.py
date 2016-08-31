# coding:utf-8
"""
日志配置
"""

import logging

# 日志的配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(threadName)s %(name)s %(levelname)s'
                           '%(message)s')


def get_logger(name):
    """
    全局日志打印工具
    :param name:  当前文件名
    :return:
    """
    return logging.getLogger(name)
