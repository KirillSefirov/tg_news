import time

import requests
import sqlite3
from database import save_summary_and_priority_for_article_url
def get_article_sum_and_priority(article_text):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": "Summarize the article. At the end, add a single digit (0–9) "
                      "showing its global importance—0 = none, 9 = major impact. "
                      "Consider only technological impact for tech news."
                      "Be objective and strict. "
                      "Be short: Output only the summary and the digit. Be short: Do not add anything."
                      "Be short: No intro or extra text. Article starts after the dot: " + article_text,
            "stream": False
        }
    )
    return response.json()["response"]

connection = sqlite3.connect("news_info.db")
cursor = connection.cursor()

cursor.execute("SELECT article_url, article_body FROM articles")
article_texts = cursor.fetchall()
for i in range(len(article_texts)):
    response = get_article_sum_and_priority(article_texts[i][1])
    article_summary = response[:-1]
    article_priority = response[-1]
    save_summary_and_priority_for_article_url(article_url=article_texts[i][0], article_summary=article_summary, article_priority=article_priority)
    time.sleep(1)
connection.close()