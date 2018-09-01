# -*- coding: utf-8 -*-
# @Author: S-W-K

from .get_brand_info import GetBrandInfo
from .get_price import GetPrice

DAILY = 1
MONTHLY = 2
WEEKLY = 3


class Crawler:
    def get_brand_info(self, sector_code=None):
        return GetBrandInfo(sector_code).getBrandInfo()

    def get_price(self, brand_code, start_date, end_date, search_type):
        if search_type == DAILY:
            result = GetPrice(brand_code, start_date, end_date).getDailyPrice()
        elif search_type == WEEKLY:
            result = GetPrice(brand_code, start_date,
                              end_date).getWeeklyPrice()
        else:
            result = GetPrice(brand_code, start_date,
                              end_date).getMonthlyPrice()
        return result
