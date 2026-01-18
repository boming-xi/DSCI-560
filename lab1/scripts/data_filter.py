import os
import requests
from bs4 import BeautifulSoup
import csv

base_dir = os.path.dirname(os.path.abspath(__file__))

html_path = os.path.join(base_dir, "../data/raw_data/web_data.html")
market_csv_path = os.path.join(base_dir, "../data/processed_data/market_data.csv")
news_csv_path = os.path.join(base_dir, "../data/processed_data/news_data.csv")

with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")

print("Filtering Market Data Fields...")
market_data = []

cards = soup.select("a.MarketCard-container")
print("cards found:", len(cards))

for card in cards:
    sym = card.select_one("span.MarketCard-symbol")
    pos = card.select_one("span.MarketCard-stockPosition")
    chg = card.select_one("span.MarketCard-changesPct")

    market_data.append([
        sym.get_text(strip=True) if sym else "N/A",
        pos.get_text(strip=True) if pos else "N/A",
        chg.get_text(strip=True) if chg else "N/A",
    ])

print(f"Storing Market data to {market_csv_path}...")
with open(market_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["marketCard_symbol", "marketCard_stockPosition", "marketCard_changePct"])
    writer.writerows(market_data)
print("Market CSV created")

print("Filtering Latest News Fields...")
news_data = []

news_items = soup.select("li.LatestNews-item")
print("news items found:", len(news_items))

for item in news_items:
    time_tag = item.select_one("time.LatestNews-timestamp")
    timestamp = time_tag.get_text(strip=True) if time_tag else "N/A"

    title_tag = item.select_one("a.LatestNews-headline")
    title = title_tag.get_text(strip=True) if title_tag else "N/A"
    link = title_tag.get("href") if title_tag else "N/A"

    if link and link.startswith("/"):
        link = "https://www.cnbc.com" + link

    news_data.append([timestamp, title, link])

print(f"Storing News data to {news_csv_path}...")
with open(news_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["LatestNews-timestamp", "title", "link"])
    writer.writerows(news_data)
print("News CSV created")