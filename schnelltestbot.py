from time import sleep 
import json
from telegram import Bot
import urllib3
import re 
from botcode import botcode
http = urllib3.PoolManager()
chatId = -1001444936568
bot = Bot(botcode)

def rossmann():
    url = "https://www.rossmann.de/de/gesundheit-boson-rapid-sars-cov-2-antigen-test/p/6921963712141"
    infile = http.request('GET', url, redirect=False, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })
    if (infile.status == 200): 
        bot.sendMessage(chatId, "Rossmann hat Tests verfügbar! "+url)
        return True
    if (infile.status == 301):
        return False
def dm(): 
    url = "https://products.dm.de/product/de/products/gtins/6921963712141?view=details"
    productURL = "https://www.dm.de/boson-corona-schnelltest-selbsttest-p6921963712141.html"
    infile = http.request('GET', url, redirect=False, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })
    foo = json.loads(infile.data.decode('utf-8'))
    
    if (foo[0]["purchasable"] == True):
        bot.sendMessage(chatId, "DM hat Tests verfügbar! "+productURL)
        return True
    if (foo[0]["purchasable"] == False):
        return False
def lidl():
    url = "https://www.lidl.de/de/5er-set-corona-sars-cov-2-antigenschnelltest-boson/p374797"
    infile = http.request('GET', url, redirect=False, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    })
    match = re.findall("isOnlineOrderable.* ([a-z]*)", infile.data.decode('utf-8'))
    if match[0] == "false":
        return False
    if match[0] == "true":
        bot.sendMessage(chatId, "Lidl hat Tests verfügbar! "+url)
        return True


dispatch = {
    'rossman': rossmann,
    'dm': dm,
    'lidl': lidl
}

while True:     
    for v in dispatch.values():
        v()
    sleep(60)



