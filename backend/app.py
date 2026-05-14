import os
# Suppress TensorFlow informational warnings and oneDNN messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import io
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image

# Import the model code
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from model.predict import load_recognition_model, predict_character

# Set frontend folder as static folder
frontend_folder = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app = Flask(__name__, static_folder=frontend_folder, static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

model = None

@app.before_request
def load_model_once():
    global model
    if model is None:
        try:
            print("Loading the model...")
            model = load_recognition_model()
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Did you run train.py first?"}), 500
        
    data = request.json
    if not data or 'image' not in data:
        return jsonify({"error": "No image provided"}), 400
        
    try:
        # Extract base64 image
        img_data = data['image'].split(',')[1]
        img_bytes = base64.b64decode(img_data)
        img = Image.open(io.BytesIO(img_bytes))
        
        # Transparent canvas usually is RGBA, Extract alpha to create black/white image
        # Because we draw white on black in frontend, alpha matters
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
            # We can use the alpha channel directly because drawing is fully opaque against transparent bg
            # Or convert to RGB
            img = Image.merge('RGB', (r, g, b))
            
        char, conf = predict_character(model, img)
        return jsonify({
            "prediction": char,
            "confidence": conf
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
