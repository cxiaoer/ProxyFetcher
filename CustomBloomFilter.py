# coding=utf-8
"""
自定义的基于BKDR Hash 算法的BloomFilter
"""

from bitarray import bitarray


class CustomBloomFilter(object):
    """docstring for CustomBloomFilter"""

    # 选取9个质数作为hash 种子
    seeds = [3, 5, 7, 11, 13, 17, 19, 23, 29]

    # 9个hash函数
    hash_num = 9

    # 选取接近10亿的bit位，减少冲撞效率
    bit_num = 1 << 30

    # 标记位
    # bits = [0] * bit_num # 太占内存
    bits = bitarray(bit_num)

    def __init__(self):
        super(CustomBloomFilter, self).__init__()
        self.bits.setall(False)

    def might_contain(self, element):
        """
        如果该元素曾经被插入过， 返回True 否则返回False
        :param element:
        """
        for seed in self.seeds:
            if not self.bits[self.__hash(seed, element)]:
                return False
        return True

    def add(self, element):
        """
        插入一个元素
        :param element:
        """
        for seed in self.seeds:
            self.bits[self.__hash(seed, element)] = 1

    def __hash(self, seed, element):
        if element is None or not isinstance(element, str):
            raise ValueError
        result = 0
        for ele in element:
            result = seed * result + ord(ele)
        return (self.bit_num - 1) & result


if __name__ == '__main__':
    bloom_filter = CustomBloomFilter()
    print(bloom_filter.might_contain('hello,world'))
    bloom_filter.add('hello,world')
    print(bloom_filter.might_contain('hello,world'))
    print(bloom_filter.might_contain('hello,world'))
    print(bloom_filter.might_contain('world'))
    bloom_filter.add('world')
    print(bloom_filter.might_contain('world'))
    print(bloom_filter.might_contain('world'))
