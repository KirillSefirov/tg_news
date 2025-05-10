import sqlite3

def create_database():
    connection = sqlite3.connect('news_info.db')
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
    article_title TEXT NOT NULL,
    article_url TEXT NOT NULL,
    article_date TEXT NOT NULL,
    article_body TEXT NOT NULL,
    article_summary TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()

def add_index_by_url():
    connection = sqlite3.connect('news_info.db')
    cursor = connection.cursor()

    cursor.execute('CREATE INDEX idx_url ON articles (article_url)')

    connection.commit()
    connection.close()

def save_article(article_title, article_url, article_date="", article_body="", article_summary=""):
    connection = sqlite3.connect('news_info.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO articles '
                   '(article_title, article_url, article_date, article_body, article_summary) '
                   'VALUES (?, ?, ?, ?, ?)',
                   (article_title, article_url, article_date, article_body, article_summary))
    connection.commit()
    connection.close()