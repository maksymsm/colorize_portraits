from flask import Blueprint, request, jsonify
import numpy as np
import cv2
import base64
from app.models.colorizer import ImageColorizer
from app.utils.metrics import calculate_metrics

main_bp = Blueprint('main', __name__)
colorizer = ImageColorizer()

@main_bp.route('/')
def index():
    return 'Colorize Portraits API is running!'

@main_bp.route('/colorize', methods=['POST'])
def colorize():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    if not file:
        return jsonify({'error': 'Empty file'}), 400

    # Read file stream to numpy array
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    if image is None:
        return jsonify({'error': 'Invalid image file'}), 400

    # Store original image for metrics calculation
    original_image = image.copy()

    # Colorize image
    colorized = colorizer.colorize_image(image)

    # Calculate metrics
    metrics = calculate_metrics(original_image, colorized)

    # Encode to PNG for response
    success, buf = cv2.imencode('.png', colorized)
    if not success:
        return jsonify({'error': 'Failed to encode image'}), 500

    # Return response
    response = {
        'metrics': metrics,
        'image': base64.b64encode(buf).decode('utf-8')
    }
    
    return jsonify(response) 