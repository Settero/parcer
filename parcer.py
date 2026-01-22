import requests
from bs4 import BeautifulSoup
import sqlite3
import streamlit
import pandas

conn = sqlite3.connect('products.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL UNIQUE,
    price INT NOT NULL,
    DESCRIPTION TEXT NOT NULL,
    STARS INT NOT NULL,
    REVIEWS INT NOT NULL
)
""")

html = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
try:
    response = requests.get(html).text
except Exception as error:
    print(f'Произошла ошибка: {error}')

bs = BeautifulSoup(response, 'html.parser')
for card in bs.find_all('div', {'class': 'product-wrapper card-body'}):
    product = {
        'title': card.select_one('a.title')['title'],
        'price': card.select_one('h4.price span').get_text(strip=True),
        'description': card.select_one('p.description.card-text')
        .get_text(strip=True),
        'stars': int(card.select_one('p[data-rating]')['data-rating']),
        'reviews': int(card.select_one('p.review-count span').text)
        }
    cursor.execute("""
    INSERT OR IGNORE INTO products
    (title, price, description, stars, reviews)
    VALUES (?, ?, ?, ?, ?)
    """, (
        product['title'],
        product['price'],
        product['description'],
        product['stars'],
        product['reviews']
    ))

conn.commit()

df = pandas.read_sql("SELECT * FROM products", conn)
edited_df = streamlit.data_editor(df, num_rows="dynamic")
if streamlit.button("Сохранить изменения"):
    edited_df.to_sql("products", conn, if_exists="replace", index=False)
