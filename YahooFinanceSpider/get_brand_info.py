# -*- coding: utf-8 -*-
# @Author: S-W-K

from lxml import etree
import requests
import math
from fake_useragent import UserAgent
from multiprocessing import Pool
from .data_type import Brand


class GetBrandInfo:
    def __init__(self, sector_code):
        self.base_url = 'https://stocks.finance.yahoo.co.jp/stocks/qi/'
        all_sectors_code = [
            '0050',  # 農林・水産業
            '1050',  # 鉱業
            '2050',  # 建設業
            '3050',  # 食料品
            '3100',  # 繊維製品
            '3150',  # パルプ・紙
            '3200',  # 化学
            '3250',  # 医薬品
            '3300',  # 石油・石炭製品
            '3350',  # ゴム製品
            '3400',  # ガラス・土石製品
            '3450',  # 鉄鋼
            '3500',  # 非鉄金属
            '3550',  # 金属製品
            '3600',  # 機械
            '3650',  # 電気機器
            '3700',  # 輸送機器
            '3750',  # 精密機器
            '3800',  # その他製品
            '4050',  # 電気・ガス業
            '5050',  # 陸運業
            '5100',  # 海運業
            '5150',  # 空運業
            '5200',  # 倉庫・運輸関連業
            '5250',  # 情報・通信
            '6050',  # 卸売業
            '6100',  # 小売業
            '7050',  # 銀行業
            '7100',  # 証券業
            '7150',  # 保険業
            '7200',  # その他金融業
            '8050',  # 不動産業
            '9050',  # サービス業
        ]
        if sector_code is None:
            self.sector_code = all_sectors_code
        else:
            self.sector_code = [sector_code]

    def _getSectorPage(self, sector_code):
        headers = {'user-agent': UserAgent().random, }
        params = {'ids': str(sector_code), }
        response = requests.get(self.base_url, headers=headers, params=params)
        html = etree.HTML(response.content.decode('utf-8'))
        try:
            sector_num = html.xpath(
                '//*[@id="listTable"]/div[1]/b[1]/text()')[0]
        except:
            print('Counldn\'t find this sector imformation')
            sector_page = None
        else:
            sector_page = math.ceil(int(sector_num)/20)
        return sector_page

    def _getBrandInfo(self, sector_code, sector_page):
        params = {'ids': sector_code, 'p': str(sector_page), }
        headers = {'user-agent': UserAgent().random, }
        response = requests.get(
            self.base_url, params=params, headers=headers)
        html = etree.HTML(response.content.decode('utf-8'))
        codes = html.xpath(
            '//*[@id="listTable"]/table/tr[@class="yjM"]/td[1]/a')
        markets = html.xpath(
            '//*[@id="listTable"]/table/tr[@class="yjM"]/td[2]')
        brands = html.xpath(
            '//*[@id="listTable"]/table/tr[@class="yjM"]/td[3]//a')
        intros = html.xpath(
            '//*[@id="listTable"]/table/tr[@class="yjM"]/td[3]/span')

        results = []
        for code, market, brand, intro in zip(codes, markets, brands, intros):
            results.append(Brand(code.text, market.text, brand.text,
                                 intro.text))
        return results

    def getBrandInfo(self):
        pool = Pool()
        final_result = []
        for sector_code in self.sector_code:
            page = self._getSectorPage(sector_code)
            if page is not None:
                code_page = [(sector_code, page_+1) for page_ in range(page)]
                results = pool.starmap_async(self._getBrandInfo, code_page)
                for result in results.get():
                    final_result += result
            else:
                final_result += None
        pool.close()
        pool.join()
        return final_result
