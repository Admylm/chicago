import requests
import time
import os
from telegram import Bot

# Environment variable kullanımı
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Render'de ekle
CHAT_ID = int(os.environ.get("CHAT_ID", "7456009735"))  # Render'de ekle veya direkt integer

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

# Deploy sonrası mesaj gönderme
try:
    bot.send_message(chat_id=CHAT_ID, text="✅ Bot başarıyla çalışıyor!")
except Exception as e:
    print(f"Mesaj gönderilemedi: {e}")

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
        except Exception as e:
            print(f"Hata: {e}")

if __name__ == "__main__":
    while True:
        check_requests()
        time.sleep(300)
