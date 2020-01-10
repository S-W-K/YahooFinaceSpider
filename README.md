# YahooFinanceSpider
日本語バージョンは[こちら](https://github.com/S-W-K/YahooFinanceSpider/blob/master/README_JPN.md)  
## Intro.
The multiprocessing web crawler	that downloads historical stock data from [YahooFinance(Japan)](https://stocks.finance.yahoo.co.jp/).  
Because [jsm](https://pypi.org/project/jsm/) is no longer being maintained, 
I rewrote the crawler with lxml, added the mechanism that prevents the crawler from getting banned, 
and used multiprocessing to accelerate.  
Python3.5 or above is needed for multiprocessing libarary.  
Crawling will increase the burden on yahoo's server, so unnecessary use should be avoided.

## Installation
```
pip3 install YahooFinanceSpider
```

## Usage
Create a Crawler instance.
```python
import YahooFinanceSpider as y
c = y.Crawler()
```

### Getting the brand information
```python
brand = c.get_brand_info(sector_code)
```

#### Sector_code is listed below
```
'1050' # mining industry
'2050' # construction industry
'3050' # food industry
'0050' # agricultural forestry industries and fishers
'3150' # pulp and paper
'3200' # chemistry
'3250' # medicine
'3300' # oil・coal products
'3350' # rubber products
'3400' # glass・stone and clay products
'3450' # steel industry
'3100' # textile products
'3500' # nonferrous metal
'3550' # metal products
'3600' # machine
'3650' # electrical machine
'3700' # transportation equipment
'3750' # precision instrument
'3800' # other products
'4050' # electricity・gas industry
'5050' # land transport
'5100' # ocean transport
'5150' # air transport
'5200' # warehouse・transportation-related
'5250' # information communication
'6050' # wholesale
'6100' # retailing
'7050' # banks 
'7100' # security business
'7150' # insurance business
'7200' # other financial business 
'8050' # real estate industry
'9050' # service industry
```
### Getting the price data
```python
# getting the daily data
price = c.get_price(code, start_time, end_time, y.DAILY) 

# getting the weekly data
price = c.get_price(code, start_time, end_time, y.WEEKLY)

# getting the monthly data
price = c.get_price(code, start_time, end_time, y.MONTHLY)
```
### Examples
```python
# getting the brand information for agricultural forestry industries and fishers
brand = c.get_brand_info('0050')
# getting all brands information
brand = c.get_brand_info()
# getting code information from the list
for i in brand:
	print(i.code) 
```
```python
from datetime import datetime
start_time = datetime(2018,1,1)
end_time = datetime(2018,8,8)

# getting the stock price data of brand 1301 during the dates noted above
price = c.get_price('1301', start_time, end_time, y.DAILY)
# getting code information from the list
for i in price:
	print(i.close) 
```
## DataType
DataType that get_brand_info() returns
### Brand
```python
Brand.code      # brand code
Brand.market    # market
Brand.brand     # brand name
Brand.intro     # brand introduction
```

DataType that get_price() returns
### Price
```python
Price.date      # date
Price.open      # opening price
Price.high      # high price
Price.low       # low price
Price.close     # closing price
Price.volume    # volume
Price.adj_close # latest price
```
### TopixPrice
```python
TopixPrice.date      # date
TopixPrice.open      # opening price
TopixPrice.high      # high price
TopixPrice.low       # low price
TopixPrice.close     # closing price
```
**Return *None* if there is no data**
