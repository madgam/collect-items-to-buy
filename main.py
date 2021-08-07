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
async def get_item(item: Item):
    scrape = Scrape()
    await scrape.getData(item.url.split(','))
    return ''
