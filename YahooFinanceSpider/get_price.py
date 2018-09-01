# -*- coding: utf-8 -*-
# @Author: S-W-K

from lxml import etree
import requests
import math
import re
from fake_useragent import UserAgent
from multiprocessing import Pool
from .data_type import Price

DAILY = 1
MONTHLY = 2
WEEKLY = 3


class GetPrice:
    def __init__(self, code, start_date, end_date):
        self.base_url = 'https://info.finance.yahoo.co.jp/history/'
        self.daily_params = {'code': code+'.T',
                             'sy': str(start_date.year),
                             'sm': str(start_date.month),
                             'sd': str(start_date.day),
                             'ey': str(end_date.year),
                             'em': str(end_date.month),
                             'ed': str(end_date.day),
                             'tm': 'd', }
        self.weekly_params = {'code': code+'.T',
                              'sy': str(start_date.year),
                              'sm': str(start_date.month),
                              'sd': str(start_date.day),
                              'ey': str(end_date.year),
                              'em': str(end_date.month),
                              'ed': str(end_date.day),
                              'tm': 'w', }
        self.monthly_params = {'code': code+'.T',
                               'sy': str(start_date.year),
                               'sm': str(start_date.month),
                               'ey': str(end_date.year),
                               'em': str(end_date.month),
                               'tm': 'm', }

    def _getBrandPage(self, search_type):
        headers = {'user-agent': UserAgent().random}
        if search_type == DAILY:
            params = self.daily_params
        elif search_type == WEEKLY:
            params = self.weekly_params
        else:
            params = self.monthly_params
        response = requests.get(self.base_url, headers=headers, params=params)
        html = etree.HTML(response.content.decode('utf-8'))
        try:
            num = html.xpath(
                '// *[@id="main"]//span[@class="stocksHistoryPageing yjS"]')[0].text
        except:
            print('Couldn\'t finad this brand data')
            brand_page = None
        else:
            num = re.search(r'/(\d+)件', num).group(1)
            brand_page = math.ceil(int(num)/20)
        return brand_page

    def _getData(self, html):
        tag_trs = html.xpath('//*[@id="main"]/div[5]/table//tr')
        results = []
        for tr in tag_trs[1:]:
            data = tr.xpath('./td/text()')
            if len(data) == 7:
                results.append(Price(data))
        return results

    def _multiprc(self, function, arg):
        pool = Pool()
        results = pool.map_async(function, arg)
        pool.close()
        pool.join()
        final_result = []
        for result in results.get():
            final_result += result
        return final_result

    def _getDailyPrice(self, page):
        headers = {'user-agent': UserAgent().random}
        params = self.daily_params
        params['p'] = str(page)
        response = requests.get(
            self.base_url, headers=headers, params=params)
        html = etree.HTML(response.content.decode('utf-8'))
        result = self._getData(html)
        return result

    def getDailyPrice(self):
        page_num = self._getBrandPage(DAILY)
        if page_num is not None:
            pages = [i+1 for i in range(page_num)]
            result = self._multiprc(self._getDailyPrice, pages)
        else:
            result = None
        return result

    def _getWeeklyPrice(self, page):
        headers = {'user-agent': UserAgent().random}
        params = self.weekly_params
        params['p'] = str(page)
        response = requests.get(
            self.base_url, headers=headers, params=params)
        html = etree.HTML(response.content.decode('utf-8'))
        result = self._getData(html)
        return result

    def getWeeklyPrice(self):
        page_num = self._getBrandPage(WEEKLY)
        if page_num is not None:
            pages = [i+1 for i in range(page_num)]
            result = self._multiprc(self._getWeeklyPrice, pages)
        else:
            result = None
        return result

    def _getMonthlyPrice(self, page):
        headers = {'user-agent': UserAgent().random}
        params = self.monthly_params
        params['p'] = str(page)
        response = requests.get(
            self.base_url, headers=headers, params=params)
        html = etree.HTML(response.content.decode('utf-8'))
        result = self._getData(html)
        return result

    def getMonthlyPrice(self):
        page_num = self._getBrandPage(MONTHLY)
        if page_num is not None:
            pages = [i+1 for i in range(page_num)]
            result = self._multiprc(self._getMonthlyPrice, pages)
        else:
            result = None
        return result
