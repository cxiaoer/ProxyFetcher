# coding:utf-8

from configs.extractor_config import *
from configs.logger_config import *
from Queue import Empty
from Queue import Queue
import requests
from bs4 import BeautifulSoup
import hashlib
from ProxyItem import ProxyItem
from proxy_item_dao import batch_insert_proxy
from utils import *

# 简单的agent 还是要用的,防止被封
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/51.0.2704.106 Safari/537.36'
}
# 日志配置
logger = get_logger(__name__)

# 全局的对应网站的抓取ip配置信息
extractor_config = init_extractor_conf()

# 抓取队列, 支持最大100万任务
task_queue = Queue(maxsize=100 * 10000)

# 检查url是否重复的锁
check_url_duplicate_lock = threading.RLock()
# 已经抓取过的url集合
url_md5_set = set()


@thread_pool(thread_num=5)
def fetch():
    while True:
        try:
            # 10秒木有任务说明做完了,直接退出
            crawl_task_item = task_queue.get(block=True, timeout=60)
        except Empty:
            logger.warn('[fetch] 木有抓取任务, 线程退出')
            break
        site = crawl_task_item.site
        url = crawl_task_item.url
        logger.info('[fetch] [%s] 开始抓取网页:%s', site, url)
        try:
            res = requests.get(url=url, headers=HEADERS)
        except requests.exceptions.RequestException as e:
            logger.exception('[fetch] [%s] 抓取网页:%s 出现异常', site, url, e)
        status_code = res.status_code
        content = res.content
        if not status_code == 200:
            logger.error('[fetch] [%s] 抓取网页:%s 状态码[%s]', site, url,
                         status_code)
            continue
        # ip信息提取
        conf = extractor_config[site]
        soup = BeautifulSoup(content, 'html.parser')
        ip_list = []
        for tag in soup.select(conf.ip_info_list):
            # ip_info_matcher = conf.ip_info_reg.finditer(str(tag))
            # ip_info_matcher = test_reg.search(str(tag))
            ip_info_matcher = conf.ip_info_reg.search(str(tag))
            if ip_info_matcher:
                ip = ip_info_matcher.group('ip')
                port = ip_info_matcher.group('port')
                ip_type = ip_info_matcher.group('ip_type')
                ip_location = ip_info_matcher.group('ip_location')
                logger.info('[fetch][%s] 在页面[%s]中抓取到ip:%s, 端口:%s, '
                            '类型:%s,位置:%s', site, url, ip, port, ip_type,
                            ip_location)
                ip_list.append(ProxyItem(ip=ip,
                                         port=port,
                                         proxy_type=ip_type,
                                         ip_location=ip_location))
        batch_insert_proxy(ip_list=ip_list)
        logger.info('[fetch][%s] 批量保存成功', site)
        # 没有分页
        if conf.nav_area_css is None:
            continue
        for nav_area in soup.select(conf.nav_area_css):
            nav_area_matcher = conf.page_num_reg.finditer(str(nav_area))
            for nav_area_match in nav_area_matcher:
                page_num = nav_area_match.group('page_num')
                # 构造分页url
                url = conf.nav_page_format.format(page_num)
                print url
                if not check_url_duplicate(url=url):
                    tmp_crawl_task_item = CrawlTaskItem(site=site,
                                                        url=url)
                    task_queue.put(tmp_crawl_task_item)


# url 去重
def check_url_duplicate(url):
    hash_type = hashlib.md5()
    hash_type.update(url)
    url_md5 = hash_type.hexdigest()
    logger.info('[fetch] 开始检查%s 是否已经抓取过;md5:%s', url, url_md5)
    check_result = False
    with check_url_duplicate_lock:
        if url_md5 in url_md5_set:
            logger.warn('[fetch] url: %s [已经]抓取过;md5:%s', url, url_md5)
            check_result = True
        else:
            url_md5_set.add(url_md5)
    return check_result


def init():
    init_crawl_task_items = init_crawl_task()
    for crawl_task_item in init_crawl_task_items:
        task_queue.put(crawl_task_item)


if __name__ == '__main__':
    init()
    fetch()
