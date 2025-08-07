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
        'url': url,
        'customAlias': custom_alias,
        'isExpirable': is_expirable,
        'expireDateTime': expire_datetime
    }), 200

if __name__ == '_main_':
    app.run(debug=True)