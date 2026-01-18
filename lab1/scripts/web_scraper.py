import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

URL = "https://www.cnbc.com/world/?region=world"

base_dir = os.path.dirname(os.path.abspath(__file__))
raw_dir = os.path.join(base_dir, "..", "data", "raw_data")
os.makedirs(raw_dir, exist_ok=True)

out_path = os.path.join(raw_dir, "web_data.html")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    )
    page = context.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=120000)
    page.mouse.wheel(0, 1200)
    page.wait_for_selector("span.MarketCard-symbol", timeout=120000)

    html = page.content()
    browser.close()


with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved rendered HTML to:", os.path.abspath(out_path))

soup = BeautifulSoup(html, "html.parser")
pretty_html = soup.prettify()
with open(out_path, "w", encoding="utf-8") as f:
    f.write(pretty_html)

print("Saved HTML to:", os.path.abspath(out_path))

print("\nFirst 10 lines of web_data.html:")
with open(out_path, "r", encoding="utf-8", errors="ignore") as f:
    for _ in range(10):
        line = f.readline()
        if not line:
            break
        print(line.rstrip("\n"))