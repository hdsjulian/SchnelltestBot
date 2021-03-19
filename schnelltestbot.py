from time import sleep 
import json
import urllib3
import re 
from telegram import Bot
from botcode import botcode
from scraper import Scraper
scraper = Scraper()
#debug id
chatId = -1001397128869
#real id
#chatId = -1001450910076
bot = Bot(botcode)

while True: 
    scraper.all()    
    results = scraper.getResults()
    for k,v in results.items():
        if v["status"] == "True":
            bot.sendMessage(chatId, "Test Verfuegbar bei "+v["name"]+"! "+v["productURL"])
    sleep(60)



