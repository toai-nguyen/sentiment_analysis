import os
from pymongo import MongoClient

# Kết nối MongoDB
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.get_database()
collection = db["raw_news"]

# Lấy 10 bài báo chưa có nhãn
articles = collection.find({"sentiment": {"$exists": False}})

VALID_SENTIMENTS = ['positive', 'neutral', 'negative']

for article in articles:
    print("\nTiêu đề:", article["title"])
    print("Nội dung:", article["content"][:400])  # Hiển thị 500 ký tự đầu

    # Nhập nhãn và kiểm tra cho đến khi hợp lệ
    while True:
        sentiment = input("Nhập sentiment (positive/neutral/negative): ").strip().lower()
        if sentiment in VALID_SENTIMENTS:
            break
        print("Giá trị không hợp lệ! Vui lòng nhập lại (positive/neutral/negative)")

    # Cập nhật vào MongoDB
    collection.update_one({"_id": article["_id"]}, {"$set": {"sentiment": sentiment}})

print("Hoàn thành gắn nhãn!")
