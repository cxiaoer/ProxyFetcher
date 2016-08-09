# coding:utf-8


import logging

# 日志的配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(threadName)s %(name)s %(levelname)s'
                    '%(message)s')


# 全局日志打印工具
def get_logger(name):
    return logging.getLogger(name)
