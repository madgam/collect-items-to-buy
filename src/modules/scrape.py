import csv
import datetime

import requests
from bs4 import BeautifulSoup


class Scrape():

    def __init__(self):
        None

    def getData(self, spamreader):
        dt_now = datetime.datetime.now()
        formated_dt_now = dt_now.strftime('%Y%m%d%H%M%S')
        f = open('csv/out/out_{}.csv'.format(formated_dt_now), 'w')
        writer = csv.writer(f)
        data = []
        COLUMNS = ['URL', '商品型番', '価格']
        for c in COLUMNS:
            data.append(c)
        writer.writerow(data)
        for row in spamreader:
            uri = row[0]

            data = []
            data.append(uri)
            res = requests.get(uri)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            itemInfo = soup.select('.product-info-main')
            itemTable = itemInfo[0].find(
                class_='additional-attributes-wrapper')
            itemDetail = itemTable.find_all('p')
            data.append(itemDetail[2].text.split(':')[1].strip())
            priceInfo = itemInfo[0].find(class_='product-info-price')
            justPrice = priceInfo.find(class_='price')
            data.append(justPrice.text)
            writer.writerow(data)
        f.close()
