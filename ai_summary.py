import time

import requests
import sqlite3
from database import save_summary_and_priority_for_article_url
def get_article_sum_and_priority(article_text):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.1",
            "prompt": "Summarize article, and at the end of the summary, "
                      "very last symbol should be it's global importance from 0 to 9. "
                      "Your response should consist of only the summary and priority. No extra text."
                      "No words here's the summary."
                      "Article text starts after dot. " + article_text,
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