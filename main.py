from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from src.modules.scrape import Scrape

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Item(BaseModel):
    url: str


@app.get("/")
def index():
    return {'hello': 'world'}


@app.post("/items")
async def get_item(item: Item):
    scrape = Scrape()
    return await scrape.getData(item.url.split(','))
