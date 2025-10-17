from flask import Flask, request, jsonify
import base64
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import serpapi

load_dotenv()

IMAGE_DATA_URI = None
MAX_DATA_URI_LENGTH = 8 * 1024 * 1024  # 8 MB

app = Flask(__name__)


@app.route('/search/', methods=['POST'])
def post_image():
    data = request.get_json(silent=True)
    if not data or 'data_uri' not in data:
        return jsonify({'error': 'No data_uri provided', 'status': 'failed'}), 400

    data_uri = data.get('data_uri')
    if not isinstance(data_uri, str) or len(data_uri) == 0:
        return jsonify({'error': 'data_uri must be a non-empty string'}), 400

    if len(data_uri) > MAX_DATA_URI_LENGTH:
        return jsonify({'error': 'data_uri too large'}), 413

    global IMAGE_DATA_URI
    IMAGE_DATA_URI = data_uri

    return jsonify({'status': 'ok', 'stored_length': len(data_uri)})

@app.route('/search/', methods=['GET'])
def getProducts():
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=os.getenv("HG_KEY"),
    )


    if IMAGE_DATA_URI is None:
        return jsonify({'error': 'No data_uri is available', 'status': 'failed'}), 400

    completion = client.chat.completions.create(
        model="meta-llama/Llama-4-Scout-17B-16E-Instruct:groq",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the product shown in this image in just 10 words or less"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": IMAGE_DATA_URI}
                    }
                ]
            }
        ],
    )

    desc = completion.choices[0].message.content

    # serpAPI 
    params = {
        "q": desc,
        "location": "Menlo Park, California, United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": os.getenv("SERP_KEY")
        }

    search = serpapi.search(params)

    items = search.get("immersive_products")
    products = []

    if not items:
        return jsonify({'error': 'No products found', 'status': 'failed'}), 404
    
    for item in items:
        products.append(
            {
                "seller": item.get("source", None),
                "product_name": item.get("title", None),
                "image": item.get("thumbnail", None),
                "price": item.get("extracted_price", None),
                "rating": item.get("rating", None),
                "location": item.get("location", None)
            }
        )

    return jsonify({'status' : 'ok', 'items' : products})



#data:image/jpeg;base64,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
        