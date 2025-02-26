# app/main.py
from flask import Flask, request, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối MongoDB
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.get_database()

# show result in mongodb to web

@app.route('/')
def home():
    return "Welcome to Sentiment Analysis API!"

# @app.route('/show_data' , methods=['GET'])
# def show_data():
#     collection = db['raw_news']
#     data = collection.find()
#     result = []
#     for item in data:
#         item.pop('_id')
#         result.append(item)
#     return jsonify(result)

# @app.route('/clean_data' , methods=['GET'])
# def clean_data():
#     collection = db['clean_news']
#     data = collection.find()
#     result = []
#     for item in data:
#         item.pop('_id')
#         result.append(item)
#     return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)