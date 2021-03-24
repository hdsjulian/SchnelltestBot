import json
import urllib3
import re 
import time


class Scraper: 
    def __init__(self):
        self.http = urllib3.PoolManager()
        self.sources = {
            'rossmann': {"name": "Rossmann", "url": "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141", "productURL": "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141", "function": self.rossmann, "status": False},
            'dm': {"name": "dm", "url": "https://products.dm.de/product/de/products/gtins/6921963712141?view=details", "productURL": "https://www.dm.de/boson-corona-schnelltest-selbsttest-p6921963712141.html", "function": self.dm, "status": False},
            'lidl': {"name": "Lidl", "url":"https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797", "productURL": "https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797","function": self.lidl,  "status": False},
            'tedi': {"name": "Tedi", "url":"https://tedi.de/LYHER-Covid-19-Antigen-Schnelltest-Nasal-Einzelverpackung", "productURL":"https://tedi.de/LYHER-Covid-19-Antigen-Schnelltest-Nasal-Einzelverpackung'", "function": self.tedi, "status": False},
            'mueller' : {"name": "Mueller", "url":"https://www.mueller.de/p/hotgen-covid-19-antigen-nasal-schnelltest-2718500/", "productURL":"https://www.mueller.de/p/hotgen-covid-19-antigen-nasal-schnelltest-2718500/", "function": self.mueller, "status": False},
            'mueller2' : {"name": "Mueller", "url":"https://www.mueller.de/p/hotgen-covid-19-antigen-nasal-selbsttest-2721685/", "productURL":"https://www.mueller.de/p/hotgen-covid-19-antigen-nasal-selbsttest-2721685/", "function": self.mueller, "status": False},
            'rossmannHotgen': {"name": "Rossmann", "url": "https://www.rossmann.de/de/gesundheit-hotgen-coronavirus2019-ncov-antigentest/p/6970297534073", "productURL": "https://www.rossmann.de/de/gesundheit-hotgen-coronavirus2019-ncov-antigentest/p/6970297534073", "function": self.rossmann, "status": False}, 
            'rossmannLyher': {"name": "Rossmann", "url": "https://www.rossmann.de/de/gesundheit-lyher-antigen-testkit/p/6972412610280", "productURL": "https://www.rossmann.de/de/gesundheit-lyher-antigen-testkit/p/6972412610280", "function": self.rossmann, "status": False}, 
            'dmLyher': {"name": "dm", "url": "https://products.dm.de/product/de/products/gtins/6972412610280?view=details", "productURL": "https://www.dm.de/lyher-corona-schnelltest-selbsttest-p6972412610280.html", "function": self.dm, "status": False  },
            'dmHotgen': {"name": "dm", "url": "https://products.dm.de/product/de/products/gtins/6970297534073?view=details", "productURL": "https://www.dm.de/hotgen-corona-schnelltest-selbsttest-p6970297534073.html", "function": self.dm, "status": False  },
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
        newStatus = self.sources[market]["function"](market)
        if (self.sources[market]["status"] != newStatus): 
            self.sources[market]["status"] = newStatus
            self.sources[market]["changed"] = True
            f = open("stati.txt", "w")
            stati = {}
            for k, v in self.sources.items():
                stati[k] = v["status"]
            f.write(json.dumps(stati))
            f.close()
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

    def mueller(self, market="mueller", counter= 0):
        infile = self.http.request('GET', self.sources[market]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status !=200):
            if (counter <3):
                counter += 1
                time.sleep(10)
                if self.mueller(market, counter) == True:
                    return True
            return False
        else:
            return True            

    def rossmann(self, market = "rossmann"):
        infile = self.http.request('GET', self.sources[market]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status == 200): 
            match = re.findall("(Aktuell nicht)", infile.data.decode('utf-8'))
            if (len(match) > 0): 
                return False
            return True
        if (infile.status == 301):
            return False

    def dm(self, market="dm"): 
        infile = self.http.request('GET', self.sources[market]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        foo = json.loads(infile.data.decode('utf-8'))
        if (foo[0]["purchasable"] == True):
            return True
        if (foo[0]["purchasable"] == False):
            return False

    def lidl(self, market="lidl"):
        infile = self.http.request('GET', self.sources[market]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status != 200):
            return False
        match = re.findall("isOnlineOrderable.* ([a-z]*)", infile.data.decode('utf-8'))
        if match[0] == "false":
            return False
        if match[0] == "true":
            return True

    def tedi(self, market="tedi"):
        infile = self.http.request('GET', self.sources[market]["url"], redirect=False, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        })
        if (infile.status != 200):
            return False
        match = re.findall("(OutOfStock)", infile.data.decode('utf-8'))
        if len(match) > 0: 
            return False
        else: 
            return True

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

