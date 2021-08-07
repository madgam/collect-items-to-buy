import asyncio
import io
from typing import List

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup
from fastapi.responses import StreamingResponse


class Scrape():

    def __init__(self):
        None

    async def getData(self, uriList: List[str]):
        COLUMNS = ['URL', '商品名', '説明文', '素材', 'カラー',
                   '商品型番', 'コレクション', '価格', '最小サイズ', '最大サイズ']
        df = pd.DataFrame(columns=COLUMNS)

        async def aprocess(url, session):
            async with session.get(url) as response:
                html = await response.text()
                bs = BeautifulSoup(html, "html.parser")
                return bs

        row_count = len(uriList)

        for i, uri in enumerate(uriList):
            print('[INFO] データ取得処理中 ... {}/{}'.format(i + 1, row_count))
            try:
                data = []
                data.append(uri)
                async with aiohttp.ClientSession() as session:
                    bs = await asyncio.gather(aprocess(uri, session))

                # 商品名
                productTitle = bs[0].find_all(class_='breadcrumbs')[0].\
                    select('.product')[0].text.strip()
                data.append(productTitle)
                # 商品データ
                itemInfo = bs[0].find_all(class_='product-info-main')

                # 説明文
                description = itemInfo[0].select('.overview')[0].text.strip()
                data.append(description)

                itemDetail = itemInfo[0].\
                    select('.additional-attributes-wrapper > p')
                # 素材
                data.append(itemDetail[0].text.split(':')[1].strip())
                # カラー
                data.append(itemDetail[1].text.split(':')[1].strip())
                # 商品型番
                data.append(itemDetail[2].text.split(':')[1].strip())
                # コレクション
                data.append(itemDetail[3].text.split(':')[1].strip())

                # 商品価格
                priceInfo = itemInfo[0].select('.product-info-price')
                justPrice = priceInfo[0].select('.price')
                data.append(justPrice[0].text.strip())

                # サイズ一覧
                itemSizes = itemInfo[0].select('.product-options-wrapper')
                itemSizeList: List[str] = [
                    fr.text.strip() for fr in itemSizes[0].select('.super-attribute-select > li')]
                minimumSize = '-' if not itemSizeList else itemSizeList[0]
                data.append(minimumSize)
                maxSize = '-' if not itemSizeList else itemSizeList[-1]
                data.append(maxSize)

                df.loc[i] = data
                # print('[ERROR] データ取得処理成功 ... {}'.format(count))

            except Exception as e:
                print('[ERROR] データ取得処理失敗 ... {}:[{}]'.format(i + 1, e))
                continue

        stream = io.StringIO()
        df.to_csv(stream, index=False)
        # stream.getvalue()によってデータを取り出し
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type="text/csv")

        response.headers["Content-Disposition"] = "attachment; filename=export.csv"

        return response
