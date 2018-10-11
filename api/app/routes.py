from flask import jsonify
from app import app
import web_scrape


@app.route('/')
def test():
    return "testing testing, hello world"


@app.route('/exchanges', methods=['GET', 'POST'])
def get_scraped_webpage():
    return jsonify(web_scrape.scrape_exchange_data())


@app.route('/exchanges/<pid>', methods=['GET'])
def get_program_data(pid):
    return pid
