import json
import urllib3
import re 

class Scraper: 
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.sources = {
            'rossmann': {"name": "Rossmann", "url": "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141", "productURL": "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141", "function": self.rossmann, "status": False, },
            'dm': {"name": "dm", "url": "https://products.dm.de/product/de/products/gtins/6921963712141?view=details", "productURL": "https://www.dm.de/boson-corona-schnelltest-selbsttest-p6921963712141.html", "function": self.dm, "status": False},
            'lidl': {"name": "Lidl", "url":"https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797", "productURL": "https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797","function": self.lidl,  "status": False},
            'tedi': {"name": "Tedi", "url":"https://tedi.de/LYHER-Covid-19-Antigen-Schnelltest-Nasal-Einzelverpackung", "productURL":"https://tedi.de/LYHER-Covid-19-Antigen-Schnelltest-Nasal-Einzelverpackung'", "function": self.tedi, "status": False}
        }

    def rossmann(self):
        infile = self.http.request('GET', self.sources["rossmann"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status == 200): 
            self.sources["rossmann"]["status"] = True
            return True
        if (infile.status == 301):
            self.sources["rossmann"]["status"] = False
            return False
    def dm(self): 
        infile = self.http.request('GET', self.sources["dm"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        foo = json.loads(infile.data.decode('utf-8'))

        if (foo[0]["purchasable"] == True):
            self.sources["dm"]["status"] = True
            return True
        if (foo[0]["purchasable"] == False):
            self.sources["dm"]["status"] = False
            return False
    def lidl(self):
        infile = self.http.request('GET', self.sources["lidl"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status != 200):
            self.sources["lidl"]["status"] = False
            return False
        match = re.findall("isOnlineOrderable.* ([a-z]*)", infile.data.decode('utf-8'))
        if match[0] == "false":
            self.sources["lidl"]["status"] = False
            return False
        if match[0] == "true":
            self.sources["lidl"]["status"] = True
            return True
    def tedi(self):
        infile = self.http.request('GET', self.sources["tedi"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status != 200):
            self.sources["tedi"]["status"] = False
            return False
        match = re.findall("(OutOfStock)", infile.data.decode('utf-8'))
        if len(match) > 0: 
            self.sources["tedi"]["status"] = False
            return False
        else: 
            self.sources["tedi"]["status"] = True
            return False
    def all(self): 
        for k, v in self.sources.items():
            print (v)
            v["function"]()
    def getResults(self):
        returnDict = {}
        for k, v in self.sources.items():
            returnDict[k] = {"name": v["name"], "url":v["url"], "productURL": v["productURL"], "status": str(v["status"])}
        return returnDict
