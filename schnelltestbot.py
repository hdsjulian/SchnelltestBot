from time import sleep 
import json
import urllib3
import re 
from telegram import Bot
from botcode import botcode
from scraper import Scraper
scraper = Scraper()
#debug id
#chatId = -1001397128869
#real id
chatId = -1001450910076
bot = Bot(botcode)

while True: 
    scraper.all()    
    results = scraper.getResults()
    for k,v in results.items():
        if v["changed"] == True: 
            if v["status"] == True:
                bot.sendMessage(chatId, "Test Verfügbar bei "+v["name"]+"! "+v["productURL"])
            elif v["status"] == False:
                bot.sendMessage(chatId, "Sieht nun aus als sei der Test bei "+v["name"]+" ausverkauft")
            v["changed"] == False
    sleep(60)



