from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    url = data.get('url')
    custom_alias = data.get('customAlias')
    is_expirable = data.get('isExpirable')
    expire_datetime = data.get('expireDateTime')

    return jsonify({
        'short_url': url,
        'orginal_url': url,
        'short_code': is_expirable,
        'created_at': expire_datetime,
        "expire_datetime" : expire_datetime
    }), 200

if __name__ == '__main__':
    app.run(debug=True)