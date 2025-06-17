import json
from scraper import Scraper
import urllib3
http = urllib3.PoolManager()

infile = http.request('GET', "https://www.lidl.de/de/5er-set-mp-rapid-sars-cov-2-antigen-schnelltest/p376622?fromRecommendation=true&scenario=personalized", redirect=False, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
print (infile.status)
myScraper = Scraper()
print(myScraper.statusCheck("lidlMP"))
