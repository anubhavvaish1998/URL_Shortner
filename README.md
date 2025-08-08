# URL_Shortner

## Setup
1. Create virtual environment and install requirements

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


2. Run the app

## API Endpoints

### POST /shorten
{
"url": "https://example.com",
"custom_alias": "alias"
}


### GET /<short_code>
Redirects to original URL.

### GET /stats/<short_code>
Returns stats like click count.

### GET /urls
Returns all shortened URLs.