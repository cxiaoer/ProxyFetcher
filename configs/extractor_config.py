# coding:utf-8
"""
抓取配置的读取和解析
"""

from configparser import ConfigParser
import re

from items.CrawlTaskItem import CrawlTaskItem

config = ConfigParser()
config.read('extractor.conf', encoding='utf-8')


def init_extractor_conf():
    """
    初始化所有的提取配置,尤其是正则配置
    :return:
    """

    d = {}
    for section_name in config.sections():
        # ip 信息提取配置
        ip_info_reg = config.get(section_name, 'ip_info_reg')
        # css select 不用预编译
        ip_info_list = config.get(section_name, 'ip_info_list')

        # 翻页信息提取
        nav_page_format = config.get(section_name, "nav_page_format")
        # css select 不用预编译
        nav_area_css = config.get(section_name, "nav_area_css")
        page_num_reg = config.get(section_name, "page_num_reg")
        d[section_name] = PageExtractConfig(ip_info_list=ip_info_list,
                                            ip_info_reg=re.compile(ip_info_reg),
                                            nav_area_css=None if nav_area_css == 'None'
                                            else nav_area_css,
                                            nav_page_format=None if nav_page_format == 'None'
                                            else nav_page_format,
                                            page_num_reg=None if page_num_reg == 'None'
                                            else re.compile(page_num_reg)
                                            )
    return d


def init_crawl_task():
    """
    从conf中初始化抓取任务
    :return:
    """
    init_crawl_task_items = []
    for section_name in config.sections():
        tmp_crawl_task_item = CrawlTaskItem(site=section_name,
                                            url=config.get(section_name,
                                                           'index_url'))
        init_crawl_task_items.append(tmp_crawl_task_item)
    return init_crawl_task_items


class PageExtractConfig(object):
    """单页面的提取规则"""

    def __init__(self, **kwargs):
        super(PageExtractConfig, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

# 一load就去加载配置
init_extractor_conf()


if __name__ == '__main__':
    # test_reg = re.compile('\d{0,8}.*[\s\S]')
    # if test_reg.search('abc'):
    #     print True
    # if re.compile(config.get('kuaidaili', 'test_reg')).search('abc'):
    #     print True
    # else:
    #     print False
    init_extractor_conf()
    for section in config.sections():
        print(config.items(section))
