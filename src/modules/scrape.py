import asyncio
from typing import List
import numpy as np
import pandas as pd

from requests_html import AsyncHTMLSession, HTMLSession


class Scrape():

    def __init__(self):
        None

    def getData(self, uriList: List[str]):
        COLUMNS = ['URL', '商品名', '説明文', '素材', 'カラー',
                   '商品型番', 'コレクション', '価格', '最小サイズ', '最大サイズ']
        assesion = AsyncHTMLSession()

        async def aprocess(uri: str):
            r = await assesion.get(uri)
            await r.html.arender(wait=10, sleep=10, timeout=20)
            return r

        print(uriList)
        row_count = len(uriList)

        for i, uri in enumerate(uriList):
            print('[INFO] データ取得処理中 ... {}/{}'.format(i + 1, row_count))
            try:
                data = []
                data.append(uri)
                loop = asyncio.get_event_loop()
                r = loop.run_until_complete(aprocess(uri))

                # 商品名
                productTitle = r.html.find('.breadcrumbs')[0].\
                    find('.product')[0].text
                data.append(productTitle)
                # 商品データ
                itemInfo = r.html.find('.product-info-main')

                # 説明文
                description = itemInfo[0].find('.overview')[0].text
                data.append(description)

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
                    fr.text for fr in itemSizes[0].find('.super-attribute-select')[0].find(('li'))]
                minimumSize = '-' if not itemSizeList else itemSizeList[0]
                data.append(minimumSize)
                maxSize = '-' if not itemSizeList else itemSizeList[-1]
                data.append(maxSize)

                # print('[ERROR] データ取得処理成功 ... {}'.format(count))

                print(data)

            except Exception as e:
                print('[ERROR] データ取得処理失敗 ... {}:[{}]'.format(i + 1, e))
                continue
