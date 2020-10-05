#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 小区信息的数据结构


class XiaoQu(object):
    def __init__(self, district, area,coord,name, price,builtYear,on_sale):
        self.district = district
        self.area = area
        self.coord = coord
        self.name = name
        self.price = price
        self.builtYear = builtYear
        self.on_sale = on_sale

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.coord + "," + \
                self.name + "," + \
                self.price + "," + \
                self.builtYear + "," + \
                self.on_sale
