# YahooFinanceSpider
## Intro.
日本の[ヤフーファイナンス](https://stocks.finance.yahoo.co.jp/)から株価データをスクレイピングするプログラム  
[jsm](https://pypi.org/project/jsm/)がメンテーナンスしていないため,新たなスクレイピングプログラムを作った  
jsmを参考した上で,lxmlとmultiprocessingを使って速度を改善した  
mutiprocessingパッケージ使ってスクレイピングを加速するので,python3.5以上が必要  
スクレイピングはヤフーのサーバに負荷をかけるので,悪意の使用はやめてください  
## Installation
```
pip3 install YahooFinanceSpider
```
## Useage
Crawlerインスタンス作成
```python
import YahooFinanceSpider as y
  c = y.Crawler()
```
このCrawlerインスタンスを使ってデータをダンロードする
### 銘柄情報の取得
```python
brand = c.get_brand_info(sector_code)
```
#### sector_codeは以下のまとめになる
```
'1050' # 鉱業
'2050' # 建設業
'3050' # 食料品
'0050' # 農林・水産業
'3150' # パルプ・紙
'3200' # 化学
'3250' # 医薬品
'3300' # 石油・石炭製品
'3350' # ゴム製品
'3400' # ガラス・土石製品
'3450' # 鉄鋼
'3100' # 繊維製品
'3500' # 非鉄金属
'3550' # 金属製品
'3600' # 機械
'3650' # 電気機器
'3700' # 輸送機器
'3750' # 精密機器
'3800' # その他製品
'4050' # 電気・ガス業
'5050' # 陸運業
'5100' # 海運業
'5150' # 空運業
'5200' # 倉庫・運輸関連業
'5250' # 情報・通信
'6050' # 卸売業
'6100' # 小売業
'7050' # 銀行業
'7100' # 証券業
'7150' # 保険業
'7200' # その他金融業
'8050' # 不動産業
'9050' # サービス業
```
### 株価データの取得
```python
# 日毎のデータを取得
price = c.get_price(code, start_time, end_time, y.DAILY) 

# 週間のデータを取得
price = c.get_price(code, start_time, end_time, y.WEEKLY)

# 月間のデータを取得
price = c.get_price(code, start_time, end_time, y.MONTHLY)
```
### 使用例
```python
# 農林水産業の銘柄情報を取得
brand = c.get_brand_info('0050')
# 全銘柄情報を取得
brand = c.get_brand_info()
# リストからインスタンスを取り出す
for i in brand:
  print(i.code) 
```
```python
from datetime import datetime
start_time = datetime(2018,1,1)
end_time = datetime(2018,8,8)

# 上記期間の銘柄コード1301会社の株価データを取得
# 全銘柄の銘柄コードはget_brand_info()で獲得できる
  price = c.get_price('1301', start_time, end_time, y.DAILY)
# リストからインスタンスを取り出す
  for i in price:
    print(i.close) 
```
## DataType
get_brand_info()の返すDataType
### Brand
```python
Brand.code      # 銘柄コード
Brand.market    # 市場
Brand.brand     # 銘柄名
Brand.intro     # 銘柄情報
```
get_price()の返すDataType
### Price
```python
Price.date      # 日時
Price.open      # 始値
Price.high      # 高値
Price.low       # 安値
Price.close     # 終値
Price.volume    # 出来高
Price.adj_close # 調整後終値
```
データが無いとき,Noneを返す
### TopixPrice
```python
TopixPrice.date      # 日時
TopixPrice.open      # 始値
TopixPrice.high      # 高値
TopixPrice.low       # 安値
TopixPrice.close     # 終値
```
データが無いとき,Noneを返す
