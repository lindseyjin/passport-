from flask import jsonify
from app import app
import webscrape


@app.route('/')
def test():
    return "testing testing, hello world"


@app.route('/exchanges', methods=['GET'])
def scraped_data():
    return jsonify(webscrape.scrape())
