import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import base64
import logging
from app.models.colorizer import ImageColorizer
from app.utils.metrics import calculate_metrics

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the colorizer
colorizer = ImageColorizer()

@app.route('/colorize', methods=['POST'])
def colorize():
    try:
        if 'grayscale_image' not in request.files or 'colored_image' not in request.files:
            return jsonify({'error': 'Both grayscale and colored images are required'}), 400
        
        grayscale_file = request.files['grayscale_image']
        colored_file = request.files['colored_image']
        
        if not grayscale_file or not colored_file:
            return jsonify({'error': 'Empty file(s)'}), 400

        # Read grayscale image
        grayscale_bytes = np.frombuffer(grayscale_file.read(), np.uint8)
        grayscale_image = cv2.imdecode(grayscale_bytes, cv2.IMREAD_COLOR)
        if grayscale_image is None:
            return jsonify({'error': 'Invalid grayscale image file'}), 400

        # Read colored image for comparison
        colored_bytes = np.frombuffer(colored_file.read(), np.uint8)
        colored_image = cv2.imdecode(colored_bytes, cv2.IMREAD_COLOR)
        if colored_image is None:
            return jsonify({'error': 'Invalid colored image file'}), 400

        # Colorize the grayscale image
        colorized = colorizer.colorize_image(grayscale_image)

        # Calculate metrics between original colored and colorized images
        metrics = calculate_metrics(colored_image, colorized)

        # Encode colorized image to PNG for response
        success, buf = cv2.imencode('.png', colorized)
        if not success:
            return jsonify({'error': 'Failed to encode colorized image'}), 500

        # Convert to base64
        image_b64 = base64.b64encode(buf).decode('utf-8')
        
        # Prepare response
        response = {
            'metrics': metrics,
            'colorized_image': image_b64
        }
        
        logger.debug(f"Response metrics: {metrics}")
        logger.debug(f"Colorized image data length: {len(image_b64)}")
        
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in colorize endpoint: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/')
def index():
    return 'Colorize Portraits API is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
