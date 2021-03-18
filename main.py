from fastapi import FastAPI
from scraper import Scraper
app = FastAPI()
scraper = Scraper()
scraper.all()

@app.get("/")
async def root():
    return scraper.getResults()
@app.get("/markets/{marketname}")
async def markets(marketname):
    return scraper.getResults()[marketname]
