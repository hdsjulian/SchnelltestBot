from time import sleep 
import random
import json
import urllib3
import re 
from telegram import Bot
from botcode import botcode

#debug id
chatId = -1002868327646
#real id
#chatId = -1001450910076
bot = Bot(botcode)

while True: 
    number = random.randint(900, 3600)
    print(f"Sleeping for {number} seconds")
    sleep(number)
    bot.sendMessage(chatId, "I'm taking a breath. Will you join me?")
    sleep(60)



