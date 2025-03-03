from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load scraped data
df = pd.read_csv('medium_articles.csv')

# Homepage route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Web Scraping API! Use /search?keyword=your_query to search articles."})

@app.route('/search', methods=['GET'])
def search_articles():
    keyword = request.args.get('keyword', '').lower()

    if not keyword:
        return jsonify({"error": "Please provide a keyword"}), 400

    # Filter data
    results = df[df['Title'].str.contains(keyword, case=False, na=False)]

    if results.empty:
        return jsonify({"message": "No articles found"}), 404

    return jsonify(results.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
