import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'DeOldify'))
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import io
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import base64
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def calculate_metrics(original, colorized):
    try:
        # Convert to grayscale for comparison
        original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        colorized_gray = cv2.cvtColor(colorized, cv2.COLOR_BGR2GRAY)
        
        # Calculate PSNR
        psnr_value = psnr(original_gray, colorized_gray)
        
        # Calculate SSIM
        ssim_value = ssim(original_gray, colorized_gray)
        
        return {
            'psnr': float(psnr_value),
            'ssim': float(ssim_value)
        }
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        return {'psnr': 0.0, 'ssim': 0.0}

@app.route('/colorize', methods=['POST'])
def colorize():
    try:
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

        # Load models (consider caching in production)
        net = cv2.dnn.readNetFromCaffe('colorization_deploy_v2.prototxt', 'colorization_release_v2.caffemodel')
        pts = np.load('pts_in_hull.npy')
        class8 = net.getLayerId('class8_ab')
        conv8 = net.getLayerId('conv8_313_rh')
        pts = pts.transpose().reshape(2, 313, 1, 1)
        net.getLayer(class8).blobs = [pts.astype('float32')]
        net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype='float32')]

        scaled = image.astype('float32') / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)
        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50
        net.setInput(cv2.dnn.blobFromImage(L))
        ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
        ab = cv2.resize(ab, (image.shape[1], image.shape[0]))
        L_orig = cv2.split(lab)[0]
        colorized = np.concatenate((L_orig[:, :, np.newaxis], ab), axis=2)
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
        colorized = np.clip(colorized, 0, 1)
        colorized = (255 * colorized).astype('uint8')

        # Calculate metrics
        metrics = calculate_metrics(original_image, colorized)

        # Encode to PNG for response
        success, buf = cv2.imencode('.png', colorized)
        if not success:
            return jsonify({'error': 'Failed to encode image'}), 500

        # Convert to base64
        image_b64 = base64.b64encode(buf).decode('utf-8')
        
        # Prepare and validate response
        response = {
            'metrics': metrics,
            'image': image_b64
        }
        
        logger.debug(f"Response metrics: {metrics}")
        logger.debug(f"Image data length: {len(image_b64)}")
        
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in colorize endpoint: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/')
def index():
    return 'Colorize Portraits API is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
