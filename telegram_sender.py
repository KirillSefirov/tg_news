import os
import sqlite3
import requests
from _datetime import datetime

tg_url =  "https://api.telegram.org/bot"

def get_articles_from_db():
    connection = sqlite3.connect('news_info.db')
    cursor = connection.cursor()

    cursor.execute('SELECT article_title, article_summary  FROM articles WHERE article_priority > 7 '
                   'AND article_date = ? ', (str(datetime.today().date()),))
    articles_info = cursor.fetchall()
    connection.close()
    return articles_info

def send_telegram(text: str):
    full_url = tg_url + os.environ["TG_TOKEN"] + "/sendMessage"
    r = requests.post(full_url, data={
         "chat_id": os.environ["TG_CHANNEL_ID"],
         "text": text,
         "parse_mode": "HTML"
          })

    if r.status_code != 200:
        raise Exception("post_text error")

articles = get_articles_from_db()

for i in range(len(get_articles_from_db())):
    article = '<b>' + articles[i][0] + '</b>' + '\n\n' + articles[i][1]
    send_telegram(article)
