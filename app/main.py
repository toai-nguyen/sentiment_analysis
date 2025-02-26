# app/main.py
from flask import Flask, render_template, request, jsonify
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
    collection = db['pred_news']
    
    # Get the page number from the query string, default to 1
    page = int(request.args.get('page', 1))
    per_page = 20  # Number of items per page
    skips = per_page * (page - 1)
    
    # Retrieve the data with pagination
    data = list(collection.find({}, {'_id': 0}).skip(skips).limit(per_page))
    
    # Get the total number of documents for pagination
    total_count = collection.count_documents({})
    total_pages = (total_count + per_page - 1) // per_page  # Calculate total pages
    
    return render_template('index.html', predictions=data, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
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