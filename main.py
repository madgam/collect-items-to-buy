import json

from fastapi import FastAPI
from pydantic import BaseModel

from src.modules.scrape import Scrape

app = FastAPI()


class Item(BaseModel):
    url: str


@app.get("/")
def index():
    return {'hello': 'world'}


@app.post("/items")
def get_item(item: Item):
    print(item.url)
    # return {"hello": 'post'}

    scrape = Scrape()
    scrape.getData([item.url.split(',')])
    # csv_files = glob.glob('csv/in/*.csv')
    # for csv_file in csv_files:
    #     with open(csv_file, newline='', encoding="utf-8-sig") as csvfile:
    #         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #         scrape.getData(spamreader)
    return ''
