import os
from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load scraped data
df = pd.read_csv('medium_articles.csv')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Web Scraping API! Use /search?keyword=your_query to search articles."})

@app.route('/search', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword', '').lower()
    if not keyword:
        return jsonify({"error": "Please provide a keyword"}), 400
    results = df[df['Title'].str.contains(keyword, case=False, na=False)]
    if results.empty:
        return jsonify({"message": "No articles found"}), 404
    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render assigns a port dynamically
    app.run(host='0.0.0.0', port=port)
