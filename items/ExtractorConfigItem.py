"""解析配置对应的item
"""
# coding:utf-8

import attr


@attr.s
class ExtractorConifgItem(object):
    """解析配置描述bean"""

    config_id = attr.ib()
    website = attr.ib()
    content = attr.ib()
    parse_type = attr.ib(default='regex')
    is_need_escapse = attr.ib(default=True)
    parent_config_id = attr.ib(default=0)
    sort = attr.ib(default=0)
    match_type = attr.ib(default=0)


if __name__ == '__main__':
    config = ExtractorConifgItem(config_id=1, website='douban')
    print(config.parent_config_id)
