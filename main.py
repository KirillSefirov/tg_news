import time

import requests
from bs4 import BeautifulSoup
from datetime import datetime

from telegram_sender import send_telegram

news_ws = "https://techcrunch.com/"

headers = {
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
latest_news_page = BeautifulSoup(requests.get(url=news_ws + "latest/").text, "html.parser")


articles = latest_news_page.find_all('div', class_="loop-card__content")

def get_article_general_data_from_html(article_full_html):
    art_data = article_full_html.find("a", class_="loop-card__title-link")
    art_url = art_data.get_attribute_list("href").pop().strip()
    art_title = art_data.text
    try:
        art_datetime = datetime.fromisoformat(article_full_html.find("time").get_attribute_list("datetime").pop()).date()
    except AttributeError:
        art_datetime = None
    return {"article_url": art_url, "article_title": art_title, "article_date": art_datetime}

parsed_art_data = [get_article_general_data_from_html(art) for art in articles]

def get_article_body_by_url(art_url):
    article_html = BeautifulSoup(requests.get(art_url).text, "html.parser")
    all_paragraphs_html = article_html.find_all("p", class_="wp-block-paragraph")
    parsed_pars = []
    for par in all_paragraphs_html:
        parsed_pars.append(par.text)
    return parsed_pars

for i in range(len(parsed_art_data)):
    parsed_art_data[i]["article_body"] = get_article_body_by_url(parsed_art_data[i]["article_url"])
    time.sleep(0.1)


# send_telegram("alalal")

