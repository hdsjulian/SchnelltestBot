import json
import urllib3
import re 

class scraper: 
    http = urllib3.PoolManager()
    sources = {
        'rossmann': {"url": "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141", "productURL": "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141", "function": scraper.rossmann, "status": False, },
        'dm': {"url": "https://products.dm.de/product/de/products/gtins/6921963712141?view=details", "productURL": "https://www.dm.de/boson-corona-schnelltest-selbsttest-p6921963712141.html", "function": scraper.dm, "status": False},
        'lidl': {"url":"https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797", "productURL": "https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797","function": scraper.lidl,  "status": False}
    }
    def rossmann(self):
        infile = this.http.request('GET', sources["rossmann"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status == 200): 
            self.sources["rossmann"]["status"] = True
            return True
        if (infile.status == 301):
            self.sources["rossmann"]["status"] = False
            return False
    def dm(self): 
        url = "https://products.dm.de/product/de/products/gtins/6921963712141?view=details"
        productURL = "https://www.dm.de/boson-corona-schnelltest-selbsttest-p6921963712141.html"
        infile = this.http.request('GET', sources["dm"]["url"], redirect=False, headers={
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
        url = "https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797"
        infile = this.http.request('GET', source["lidl"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        match = re.findall("isOnlineOrderable.* ([a-z]*)", infile.data.decode('utf-8'))
        if match[0] == "false":
            self.sources["lidl"]["status"] = False
            return False
        if match[0] == "true":
            self.sources["lidl"]["status"] = True
            return True
    def all(): 
        for k, v in self.sources.items():
            v["function"]()
        print(self.sources)