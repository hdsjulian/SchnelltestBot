from fastapi import FastAPI
from scraper import Scraper
app = FastAPI()
scraper = Scraper()
scraper.all()

@app.get("/")
async def root():
    return scraper.getResults()

@app.get("/dm")
async def dm():
    return scraper.getResults()["dm"]
@app.get("/rossmann")
async def rossmann():
    return scraper.getResults()["rossmann"]
@app.get("/lidl")
async def lidl():
    return scraper.getResults()["lidl"]
@app.get("/tedi")
async def tedi():
    return scraper.getResults()["tedi"]