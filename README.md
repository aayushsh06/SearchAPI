# SearchAPI

An AI-powered visual product search API that identifies products from images and finds similar items available for purchase online.

## Overview

SearchAPI uses computer vision and AI to analyze product images, generate descriptive text, and search for similar products across the web. It combines the power of Meta's Llama vision model with SerpAPI's Google Shopping integration to deliver relevant product matches with pricing, ratings, and seller information.

## Features

- **🖼️ Image-Based Product Search**: Upload product images and automatically find similar items online
- **🤖 AI-Powered Description**: Uses Meta Llama-4-Scout vision model to generate concise product descriptions
- **🛍️ Real Shopping Results**: Integrates with Google Shopping via SerpAPI for actual product listings
- **📊 Rich Product Data**: Returns seller info, prices, ratings, thumbnails, and locations
- **🚀 Simple REST API**: Easy-to-use POST/GET endpoint structure
- **📦 Base64 Image Support**: Accepts images as data URIs for seamless integration

## Tech Stack

- **Backend**: Flask (Python)
- **AI Model**: Meta Llama-4-Scout-17B-16E-Instruct via Hugging Face Router
- **Search API**: SerpAPI for Google Shopping integration
- **Image Processing**: Base64 data URI handling

## Installation

```bash
# Clone the repository
git clone https://github.com/aayushsh06/SearchAPI.git
cd SearchAPI

# Install dependencies
pip install flask openai python-dotenv serpapi

# Create .env file with your API keys
cp .env.example .env
```

## Configuration

Create a `.env` file in the root directory with the following keys:

```env
HG_KEY=your_huggingface_api_key
SERP_KEY=your_serpapi_key
```

**Getting API Keys:**
- **Hugging Face**: Sign up at [huggingface.co](https://huggingface.co) and generate an API token
- **SerpAPI**: Sign up at [serpapi.com](https://serpapi.com) and get your API key

## Usage

### Starting the Server

```bash
python app.py
```

The API will start on `http://localhost:5000` (default Flask port).

### API Endpoints

#### 1. Upload Image (POST)

First, upload an image as a base64-encoded data URI:

```http
POST /search/
Content-Type: application/json

{
  "data_uri": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response:**
```json
{
  "status": "ok",
  "stored_length": 1234567
}
```

#### 2. Search Products (GET)

After uploading an image, retrieve matching products:

```http
GET /search/
```

**Response:**
```json
{
  "status": "ok",
  "items": [
    {
      "seller": "Amazon",
      "product_name": "Wireless Bluetooth Headphones",
      "image": "https://example.com/thumbnail.jpg",
      "price": 49.99,
      "rating": 4.5,
      "location": "Online"
    }
  ]
}
```

### Complete Example

#### Python

```python
import requests
import base64

# Read and encode image
with open('product.jpg', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')
    data_uri = f'data:image/jpeg;base64,{image_data}'

# Upload image
upload_response = requests.post('http://localhost:5000/search/', 
    json={'data_uri': data_uri})
print(upload_response.json())

# Search for products
search_response = requests.get('http://localhost:5000/search/')
products = search_response.json()['items']

for product in products:
    print(f"{product['product_name']} - ${product['price']}")
    print(f"Seller: {product['seller']}, Rating: {product['rating']}")
```

#### JavaScript/Node.js

```javascript
const axios = require('axios');
const fs = require('fs');

async function searchProduct(imagePath) {
  // Read and encode image
  const imageBuffer = fs.readFileSync(imagePath);
  const base64Image = imageBuffer.toString('base64');
  const dataUri = `data:image/jpeg;base64,${base64Image}`;
  
  // Upload image
  await axios.post('http://localhost:5000/search/', {
    data_uri: dataUri
  });
  
  // Get products
  const response = await axios.get('http://localhost:5000/search/');
  return response.data.items;
}

searchProduct('product.jpg')
  .then(products => console.log(products))
  .catch(error => console.error(error));
```

#### cURL

```bash
# Upload image
curl -X POST http://localhost:5000/search/ \
  -H "Content-Type: application/json" \
  -d '{"data_uri": "data:image/jpeg;base64,/9j/4AAQ..."}'

# Search products
curl http://localhost:5000/search/
```

## How It Works

1. **Image Upload**: Client sends a base64-encoded image as a data URI to the POST endpoint
2. **Image Analysis**: The stored image is sent to Meta's Llama-4-Scout vision model with a prompt to describe the product in 10 words or less
3. **Product Search**: The AI-generated description is used as a search query for SerpAPI's Google Shopping integration
4. **Results Processing**: Product listings are extracted, formatted, and returned with seller info, pricing, ratings, and images

## Limitations

- Maximum image size: 8 MB
- Images must be in data URI format (base64-encoded)
- Search results limited to Google Shopping's "immersive_products" results
- Requires active internet connection for AI model and search API
- Sequential workflow: must POST image before GET request

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Missing or invalid data_uri
- `404 Not Found`: No products found matching the image
- `413 Payload Too Large`: Image exceeds 8 MB limit

**Example Error Response:**
```json
{
  "error": "No products found",
  "status": "failed"
}
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `HG_KEY` | Hugging Face API key for Llama model access | Yes |
| `SERP_KEY` | SerpAPI key for Google Shopping searches | Yes |

## Project Structure

```
SearchAPI/
├── app.py              # Main Flask application
├── .env                # Environment variables (not in repo)
├── .env.example        # Example environment file
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

```txt
flask
openai
python-dotenv
serpapi
```

## License

This project is available for personal and commercial use.

## Acknowledgments

- **Meta AI** for the Llama-4-Scout vision model
- **Hugging Face** for model hosting and inference API
- **SerpAPI** for Google Shopping search integration

## Support

For issues, questions, or contributions, please open an issue on the [GitHub repository](https://github.com/aayushsh06/SearchAPI).
