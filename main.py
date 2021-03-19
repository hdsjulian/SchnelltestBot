from fastapi import FastAPI
from scraper import Scraper
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title='SchnelltestBot',
    description='Returns information about availability od Covid-Antigentests in some online shops in Germany'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['filename']
)

scraper = Scraper()
scraper.all()

@app.get("/")
async def root():
    """
    test test test
    :return:
    :rtype:
    """
    return scraper.getResults()
@app.get("/markets/{marketname}")
async def markets(marketname):
    return scraper.getResults()[marketname]
