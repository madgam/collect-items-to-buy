import asyncio
from typing import List

import aiohttp
from bs4 import BeautifulSoup


class Scrape():

    def __init__(self):
        None

    async def getData(self, uriList: List[str]):
        COLUMNS = ['url', 'item_name', 'description', 'material', 'color',
                   'item_no', 'collection', 'price', 'size_minimum', 'size_max']

        async def aprocess(url, session):
            async with session.get(url) as response:
                html = await response.text()
                bs = BeautifulSoup(html, "html.parser")
                return bs

        row_count = len(uriList)
        jsonInnerData = []

        for i, uri in enumerate(uriList):
            print('[INFO] データ取得処理中 ... {}/{}'.format(i + 1, row_count))
            try:
                data = {}
                data[COLUMNS[0]] = uri
                async with aiohttp.ClientSession() as session:
                    bs = await asyncio.gather(aprocess(uri, session))

                # 商品名
                productTitle = bs[0].find_all(class_='breadcrumbs')[0].\
                    select('.product')[0].text.strip()
                data[COLUMNS[1]] = productTitle
                # 商品データ
                itemInfo = bs[0].find_all(class_='product-info-main')

                # 説明文
                description = itemInfo[0].select('.overview')[0].text.strip()
                data[COLUMNS[2]] = description

                itemDetail = itemInfo[0].\
                    select('.additional-attributes-wrapper > p')
                # 素材
                data[COLUMNS[3]] = itemDetail[0].text.split(':')[1].strip()
                # カラー
                data[COLUMNS[4]] = itemDetail[1].text.split(':')[1].strip()
                # 商品型番
                data[COLUMNS[5]] = itemDetail[2].text.split(':')[1].strip()
                # コレクション
                data[COLUMNS[6]] = itemDetail[3].text.split(':')[1].strip()

                # 商品価格
                priceInfo = itemInfo[0].select('.product-info-price')
                justPrice = priceInfo[0].select('.price')
                data[COLUMNS[7]] = justPrice[0].text.strip()

                # サイズ一覧
                itemSizes = itemInfo[0].select('.product-options-wrapper')
                itemSizeList: List[str] = [
                    fr.text.strip() for fr in itemSizes[0].select('.super-attribute-select > li')]
                minimumSize = '-' if not itemSizeList else itemSizeList[0]
                data[COLUMNS[8]] = minimumSize
                maxSize = '-' if not itemSizeList else itemSizeList[-1]
                data[COLUMNS[9]] = maxSize

                jsonInnerData.append(data)
                # print('[ERROR] データ取得処理成功 ... {}'.format(count))

            except Exception as e:
                print('[ERROR] データ取得処理失敗 ... {}:[{}]'.format(i + 1, e))
                continue

        return jsonInnerData
