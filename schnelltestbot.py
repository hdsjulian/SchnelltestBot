#!/usr/bin/env python3
from time import sleep 
import random
import json
import urllib3
import re 
from telegram import Bot
from botcode import botcode
import argparse
parser = argparse.ArgumentParser(description='A bot that sends a message every 60 seconds after a random sleep.')
parser.add_argument('min_sleep', type=int, help='Minimum sleep time in seconds', default=900)
parser.add_argument('max_sleep', type=int, help='Maximum sleep time in seconds', default=3600)
args = parser.parse_args()
print(f"Minimum sleep time: {args.min_sleep} seconds")
print(f"Maximum sleep time: {args.max_sleep} seconds")  
#debug id
chatId = -1002868327646
#real id
#chatId = -1001450910076
bot = Bot(botcode)

while True: 

    number = random.randint(args.min_sleep, args.max_sleep)
    print(f"Sleeping for {number} seconds")
    sleep(number)
    bot.sendMessage(chatId, "I'm taking a breath. Will you join me?")



