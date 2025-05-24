from flask import Blueprint, request, jsonify, Response
import numpy as np
import cv2
import base64
from app.models.colorizer import ImageColorizer
from app.utils.metrics import calculate_metrics
import json

main_bp = Blueprint('main', __name__)
colorizer = ImageColorizer()

@main_bp.route('/')
def index():
    return 'Colorize Portraits API is running!'

@main_bp.route('/colorize', methods=['POST'])
def colorize():
    if 'colored_image' not in request.files or 'grayscale_image' not in request.files:
        missing = []
        if 'colored_image' not in request.files:
            missing.append('colored_image')
        if 'grayscale_image' not in request.files:
            missing.append('grayscale_image')
        error_msg = f'Missing required files: {", ".join(missing)}'
        return jsonify({'error': error_msg}), 400
    
    colored_file = request.files['colored_image']
    grayscale_file = request.files['grayscale_image']
    
    if not colored_file or not grayscale_file:
        return jsonify({'error': 'Empty file(s)'}), 400

    try:
        # Read colored image
        colored_bytes = np.frombuffer(colored_file.read(), np.uint8)
        colored_image = cv2.imdecode(colored_bytes, cv2.IMREAD_COLOR)
        if colored_image is None:
            return jsonify({'error': 'Invalid colored image file'}), 400

        # Read grayscale image
        grayscale_bytes = np.frombuffer(grayscale_file.read(), np.uint8)
        grayscale_image = cv2.imdecode(grayscale_bytes, cv2.IMREAD_COLOR)
        if grayscale_image is None:
            return jsonify({'error': 'Invalid grayscale image file'}), 400

        # Colorize grayscale image
        colorized = colorizer.colorize_image(grayscale_image)

        # Calculate metrics between original colored and colorized images
        metrics = calculate_metrics(colored_image, colorized)

        # Encode colorized result to PNG with maximum quality
        encode_params = [cv2.IMWRITE_PNG_COMPRESSION, 0]
        success, buf = cv2.imencode('.png', colorized, encode_params)
        if not success:
            return jsonify({'error': 'Failed to encode image'}), 500

        # Prepare response data
        response_data = {
            'metrics': metrics,
            'colorized_image': base64.b64encode(buf).decode('utf-8')
        }
        
        # Return response with increased max content length
        return Response(
            json.dumps(response_data),
            mimetype='application/json',
            headers={
                'Content-Length': str(len(json.dumps(response_data)))
            }
        )
        
    except Exception as e:
        return jsonify({'error': f'Error processing images: {str(e)}'}), 500 