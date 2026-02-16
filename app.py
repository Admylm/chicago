import requests
import time
import os
from telegram import Bot

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

ADDRESSES = [
    "422 W ROSLYN PL",
    "160 W SCHILLER ST",
    "2935 N ASHLAND AVE",
    "2422 W TAYLOR ST",
    "2420 W TAYLOR ST",
    "2219 W ADAMS ST"
]

API_URL = "https://data.cityofchicago.org/resource/v6vf-nfxy.json"

bot = Bot(token=TELEGRAM_TOKEN)

seen_requests = set()

def check_requests():
    for address in ADDRESSES:
        params = {
            "$where": f"upper(street_address) like '%{address.upper()}%'",
            "$order": "creation_date DESC",
            "$limit": 5
        }
        try:
            response = requests.get(API_URL, params=params)
            data = response.json()
            for item in data:
                sr_number = item.get("service_request_number")
                if sr_number and sr_number not in seen_requests:
                    seen_requests.add(sr_number)
                    message = (
                        f"New 311 Request!\n"
                        f"Address: {item.get('street_address')}\n"
                        f"Service: {item.get('service_name')}\n"
                        f"Status: {item.get('status')}\n"
                        f"Date: {item.get('creation_date')}"
                    )
                    bot.send_message(chat_id=CHAT_ID, text=message)
        except:
            pass

if __name__ == "__main__":
    bot.send_message(chat_id=CHAT_ID, text="Bot is running!")
    while True:
        check_requests()
        time.sleep(300)
