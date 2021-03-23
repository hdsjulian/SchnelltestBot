import json
import urllib3
import re 
import time


class Scraper: 
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.sources = {
            'rossmann': {"name": "Rossmann", "url": "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141", "productURL": "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141", "function": self.rossmann, "status": False, },
            'dm': {"name": "dm", "url": "https://products.dm.de/product/de/products/gtins/6921963712141?view=details", "productURL": "https://www.dm.de/boson-corona-schnelltest-selbsttest-p6921963712141.html", "function": self.dm, "status": False},
            'lidl': {"name": "Lidl", "url":"https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797", "productURL": "https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797","function": self.lidl,  "status": False},
            'tedi': {"name": "Tedi", "url":"https://tedi.de/LYHER-Covid-19-Antigen-Schnelltest-Nasal-Einzelverpackung", "productURL":"https://tedi.de/LYHER-Covid-19-Antigen-Schnelltest-Nasal-Einzelverpackung'", "function": self.tedi, "status": False},
            'mueller' : {"name": "Mueller", "url":"https://www.mueller.de/p/hotgen-covid-19-antigen-nasal-schnelltest-2718500/", "productURL":"https://www.mueller.de/p/hotgen-covid-19-antigen-nasal-schnelltest-2718500/", "function": self.mueller, "status": False}
            'mueller2' : {"name": "Mueller", "url":"https://www.mueller.de/p/hotgen-covid-19-antigen-nasal-selbsttest-2721685/", "productURL":"https://www.mueller.de/p/hotgen-covid-19-antigen-nasal-selbsttest-2721685/", "function": self.mueller, "status": False}
            #'doccheck': {
            #    'name': 'DocCheck',
            #    'url': 'https://www.doccheckshop.eu/laboratory/tests/rapid-coronavirus-tests/12076/roche-sars-cov-2-rapid-antigen-test',
            #    'productURL': 'https://www.doccheckshop.eu/laboratory/tests/rapid-coronavirus-tests/12076/roche-sars-cov-2-rapid-antigen-test',
            #    'function': self.doc_check,
            #    'status': False
            #}
        }
        f = open("stati.txt", "r")
        stati = json.loads(f.read())
        f.close()
        for k, v in self.sources.items():
            self.sources[k]["status"] = stati[k]
            self.sources[k]["changed"] = False
        
    def statusCheck(self, market):
        newStatus = self.sources[market]["function"]()
        if (self.sources[market]["status"] != newStatus): 
            self.sources[market]["status"] = newStatus
            self.sources[market]["changed"] = True
            return True
        else: 
            self.sources[market]["changed"] = False
            return False

    def doc_check(self):
        infile = self.http.request('GET', self.sources['doccheck']["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status !=200):
            return False
        if 'This item is not available' in infile.data.decode('utf-8'):
            return False
        else:
            return True

    def mueller(self, counter= 0):
        infile = self.http.request('GET', self.sources['mueller']["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status !=200):
            if (counter <3):
                counter += 1
                time.sleep(10)
                if self.mueller(counter) == True:
                    return True
            return False
        else:
            return True            

    def rossmann(self):
        infile = self.http.request('GET', self.sources["rossmann"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status == 200): 
            return True
        if (infile.status == 301):
            return False

    def dm(self): 
        infile = self.http.request('GET', self.sources["dm"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        foo = json.loads(infile.data.decode('utf-8'))

        if (foo[0]["purchasable"] == True):
            return True
        if (foo[0]["purchasable"] == False):
            return False

    def lidl(self):
        infile = self.http.request('GET', self.sources["lidl"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status != 200):
            return False
        match = re.findall("isOnlineOrderable.* ([a-z]*)", infile.data.decode('utf-8'))
        if match[0] == "false":
            return False
        if match[0] == "true":
            return True

    def tedi(self):
        infile = self.http.request('GET', self.sources["tedi"]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status != 200):
            return False
        match = re.findall("(OutOfStock)", infile.data.decode('utf-8'))
        if len(match) > 0: 
            return False
        else: 
            return False

    def all(self): 
        stati = {}
        for k, v in self.sources.items():
            self.statusCheck(k)
            stati[k] = self.sources[k]["status"]
        f = open("stati.txt", "w")
        f.write(json.dumps(stati))
        f.close()

            
    def getResults(self):
        returnDict = {}
        for k, v in self.sources.items():
            returnDict[k] = {"name": v["name"], "url":v["url"], "productURL": v["productURL"], "status": v["status"], "changed":v["changed"]}
        return returnDict

