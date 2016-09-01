# coding:utf-8
"""抓取代理线程组
"""

from Queue import Empty
from Queue import Queue
import requests
from bs4 import BeautifulSoup
from configs.extractor_config import *
from configs.logger_config import *
from configs.user_agent_config import get_user_agent
from items.ProxyItem import ProxyItem
from proxy_item_dao import batch_insert_proxy
from utils import *
from duplicate_remover import hashset_duplicate_remover

logger = get_logger(__name__)  # 日志配置
extractor_config = init_extractor_conf()  # 全局的对应网站的抓取ip配置信息
task_queue = Queue(maxsize=100 * 10000)  # 抓取队列, 支持最大100万任务


@thread_pool(thread_num=5)
def fetch():
    """抓取
    """

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
            user_agent = get_user_agent()
            res = requests.get(url=url, headers={'User-Agent'
                                                 : user_agent})
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
                                         proxy_type=ip_type.upper(),
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
                if not hashset_duplicate_remover(url=url):
                    tmp_crawl_task_item = CrawlTaskItem(site=site,
                                                        url=url)
                    task_queue.put(tmp_crawl_task_item)


def init():
    """从配置中初始化抓取任务
    """

    init_crawl_task_items = init_crawl_task()
    for crawl_task_item in init_crawl_task_items:
        task_queue.put(crawl_task_item)


if __name__ == '__main__':
    init()
    fetch()
