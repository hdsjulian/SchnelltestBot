#!/usr/bin/env python3
from time import sleep 
import random
import json
import re 
import datetime
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

messages_part1 = [
    "I'm having a breath",
    "I'm taking a breath",
    "I'm taking a moment to breathe"
]

messages_part2 = [
    "care to join?",
    "will you join me?",
    "want to join?"
]

while True: 
    now = datetime.datetime.now()
    if (now.hour > 22 or now.hour < 7):
        print("It's night time, sleeping for 1 hour")
        sleep(3600)
        continue
    number = random.randint(args.min_sleep, args.max_sleep)
    print(f"Sleeping for {number} seconds")
    sleep(number)
    message = f"{random.choice(messages_part1)}, {random.choice(messages_part2)}"
    print(f"Sending message: {message}")

    #bot.sendMessage(chatId, message)



