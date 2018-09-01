# -*- coding: utf-8 -*-
# @Author: S-W-K

from datetime import datetime


def _isNone(obj):
    if obj is None:
        obj = ''
    return obj.strip()


def _str(obj):
    obj = obj.replace(',', '')
    try:
        obj = int(obj)
    except:
        obj = float(obj)
    return str(obj)


class Brand:
    def __init__(self, code, market, brand, intro):
        self.code = code
        self.market = _isNone(market)
        self.brand = brand
        self.intro = _isNone(intro)


class Price:
    def __init__(self, data):
        try:
            date = datetime.strptime(data[0], '%Y年%m月%d日')
        except:
            date = datetime.strptime(data[0], '%Y年%m月')
            date = datetime.strftime(date, '%Y-%m')
        else:
            date = datetime.strftime(date, '%Y-%m-%d')
        self.date = str(date)
        self.open = _str(data[1])
        self.high = _str(data[2])
        self.low = _str(data[3])
        self.close = _str(data[4])
        self.volume = _str(data[5])
        self.adj_close = _str(data[6])
