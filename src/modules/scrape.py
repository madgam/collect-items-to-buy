import asyncio
import csv
import datetime
from typing import List

from requests_html import AsyncHTMLSession


class Scrape():

    def __init__(self):
        None

    def getData(self, spamreader):
        dt_now = datetime.datetime.now()
        formated_dt_now = dt_now.strftime('%Y%m%d%H%M%S')
        f = open('csv/out/out_{}.csv'.format(formated_dt_now), 'w')
        writer = csv.writer(f)
        data = []
        COLUMNS = ['URL', '素材', 'カラー',
                   '商品型番', 'コレクション', '価格', '最小サイズ', '最大サイズ']
        for c in COLUMNS:
            data.append(c)
        writer.writerow(data)
        assesion = AsyncHTMLSession()

        async def process(uri):
            r = await assesion.get(uri)
            await r.html.arender(wait=5, sleep=5)
            return r

        for row in spamreader:
            uri = row[0]
            data = []
            data.append(uri)
            loop = asyncio.get_event_loop()
            r = loop.run_until_complete(process(uri))

            # 商品データ
            itemInfo = r.html.find('.product-info-main')
            itemTable = itemInfo[0].find('.additional-attributes-wrapper')

            itemDetail = itemTable[0].find('p')
            # 素材
            data.append(itemDetail[0].text.split(':')[1].strip())
            # カラー
            data.append(itemDetail[1].text.split(':')[1].strip())
            # 商品型番
            data.append(itemDetail[2].text.split(':')[1].strip())
            # コレクション
            data.append(itemDetail[3].text.split(':')[1].strip())

            # 商品価格
            priceInfo = itemInfo[0].find('.product-info-price')
            justPrice = priceInfo[0].find('.price')
            data.append(justPrice[0].text)

            # サイズ一覧
            itemSizes = itemInfo[0].find('.product-options-wrapper')
            itemSizeList: List[str] = [
                fr.text for fr in itemSizes[0].find('.in-stock')]
            minimumSize = '-' if not itemSizeList else itemSizeList[0]
            data.append(minimumSize)
            maxSize = '-' if not itemSizeList else itemSizeList[-1]
            data.append(maxSize)
            writer.writerow(data)

        f.close()
