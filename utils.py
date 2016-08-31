# coding:utf-8
""" 封装了一些常用的操作

1: 请求频率限制
2: 线程池的装饰器
3: 时间保留两位小数的格式化

"""

import time
import threading

# 频率控制锁
incr_req_times_lock = threading.RLock()
# 请求滑动窗
req_slide_window = []


def rate_limit(max_req_times, time_value, time_unit):
    """请求频率限制

    :param max_req_times: 最大请求频率
    :param time_value:  单位时间值
    :param time_unit: 时间单位; 小时->'H'
    :return
    """

    global req_slide_window

    current_time = time.time()  # 当前时间以秒为单位
    req_slide_window.append(current_time)
    with incr_req_times_lock:
        if len(req_slide_window) == 0:
            return False
        else:
            # 以小时为单位
            if time_unit == 'H':
                interval = time_value * 3600
            else:  # 以分钟为单位
                interval = time_value * 60
            # 过滤出过去一段时间的list， 判断大小
            req_in_last_interval = [x for x in req_slide_window if x >= (current_time - interval)]
            req_slide_window = req_in_last_interval
            length = len(req_in_last_interval)
            if length > max_req_times:
                req_slide_window = req_in_last_interval[length - max_req_times:length]
                req_slide_window.remove(current_time)  # 超过最大值得请求不能算作
                return True
            else:
                return False


def format_time(time_in_seconds):
    """将秒转成毫秒， 并且保留两位小数

    :param time_in_seconds: 比如time.time() 的调用结果
    :return 保留两位小数的浮点数表示
    """

    milliseconds = time_in_seconds * 1000
    return float('%0.2f' % milliseconds)


def thread_pool(thread_num):
    """无返回的线程池的装饰器

    :param thread_num: 自定义的线程数
    :return
    """

    def _outer_func(target_func):
        def __inner_func(*args, **kwargs):
            threads = []
            for i in range(thread_num):
                thread = threading.Thread(target=target_func, args=args, kwargs=kwargs)
                threads.append(thread)
            for thread in threads:
                thread.start()
                # for thread in threads:
                #     thread.join()

        return __inner_func

    return _outer_func
