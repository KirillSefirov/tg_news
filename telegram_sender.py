import os

import requests

tg_url =  "https://api.telegram.org/bot"

def send_telegram(text: str):
    full_url = tg_url + os.environ["TG_TOKEN"] + "/sendMessage"
    r = requests.post(full_url, data={
         "chat_id": os.environ["TG_CHANNEL_ID"],
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")

