from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from urllib.parse import urlparse
from models import db, URL
from utils import is_valid_url, generate_short_code
import os

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# @app.route('/')
# def home():
#     return "Home"

@app.before_request
def create_tables():
    db.create_all()

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    custom_alias = data.get('custom_alias')

    if not original_url or not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    if custom_alias:
        print (f"Custom alias is {custom_alias}")
        if URL.query.filter_by(short_code=custom_alias).first():
            return jsonify({'error': 'Custom alias already exists'}), 409
        short_code = custom_alias + "-" + generate_short_code()
    else:
        short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()

    response = {
        "short_url": f"http://localhost:5000/{short_code}",
        "original_url": original_url,
        "short_code": short_code,
        "created_at": new_url.created_at.isoformat() + 'Z'
    }
    return jsonify(response), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if url_entry:
        url_entry.click_count += 1
        db.session.commit()
        return redirect(url_entry.original_url)
    return jsonify({'error': 'Short URL not found'}), 404

@app.route('/stats/<short_code>', methods=['GET'])
def url_stats(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()
    if not url_entry:
        return jsonify({'error': 'Short URL not found'}), 404

    response = {
        "short_code": short_code,
        "original_url": url_entry.original_url,
        "click_count": url_entry.click_count,
        "created_at": url_entry.created_at.isoformat() + 'Z'
    }
    return jsonify(response), 200

@app.route('/urls', methods=['GET'])
def list_urls():
    urls = URL.query.all()
    response = {
        "urls": [
            {
                "short_code": url.short_code,
                "original_url": url.original_url,
                "click_count": url.click_count,
                "created_at": url.created_at.isoformat() + 'Z'
            } for url in urls
        ]
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
