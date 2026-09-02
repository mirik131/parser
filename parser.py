import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://books.toscrape.com/"
PAGES = 3

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

data = []

print(f"парсинг")

for page in range(1, PAGES + 1):
    if page == 1:
        url = BASE_URL
    else:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        r.encoding = "utf-8"
    except Exception as e:
        print(f"Ошибка")
        continue

    soup = BeautifulSoup(r.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    if not books:
        print("книг нет")
        continue

    for b in books:
        try:
            title = b.h3.a["title"]
            price = b.find("p", class_="price_color").text.strip()
            price = price.replace("Â£", "£").replace("Â", "")
            link = b.h3.a["href"]

            link = link.replace("../../../", "")
            if not link.startswith("http"):
                if not link.startswith("catalogue/"):
                    link = "catalogue/" + link
                link = BASE_URL + link

            data.append([title, price, link, "", ""])
        except:
            continue

    time.sleep(1)

with open("output.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["title", "price", "link", "date", "location"])
    w.writerows(data)

print(f"готово")
