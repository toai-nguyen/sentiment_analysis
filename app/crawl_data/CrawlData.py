import datetime
import time
import requests
from bs4 import BeautifulSoup
import pymongo
import os
from pymongo import MongoClient

mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db['raw_news']


url = "https://vnexpress.net/kinh-doanh/chung-khoan-p11"
headers = {
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    "User-Agent": ""
}
# headers=headers
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("h2", {"class": "title-news"})

for article in articles:
    title = article.text.strip()
    link = article.a["href"]
    

    # Gửi request lấy nội dung bài báo
    article_response = requests.get(link, headers=headers) #headers=headers
    article_soup = BeautifulSoup(article_response.text, "html.parser")

    # Tìm phần nội dung bài báo
    content = article_soup.find("article", {"class": "fck_detail"})

    if content:
        paragraphs = content.find_all("p")
        article_text = "\n".join(p.text for p in paragraphs)
    else:
        article_text = "Không thể lấy nội dung"
    
    article_data = {
        "title": title,
        "url": link,
        "content": article_text,
        "scraped_at": datetime.datetime.now()  # Thời gian lấy dữ liệu
    }
            # Kiểm tra nếu bài báo đã tồn tại thì không lưu trùng
    if not collection.find_one({"url": link}):
        collection.insert_one(article_data)
        print(f"Đã lưu: {title}")
    else:
        print(f"Đã tồn tại: {title}")

    time.sleep(2)

print("Kết thúc crawl dữ liệu")