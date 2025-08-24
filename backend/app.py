
from flask import Flask, request, send_file
from flask_cors import CORS
import cv2
import numpy as np
import os
from detection import DetectionofCopyMoveForgery

app = Flask(__name__)
CORS(app)  # Enables CORS for all domains (for frontend connection)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/detect', methods=['POST'])
def detect_forgery():
    # Check if an image was uploaded
    if 'image' not in request.files:
        return "No image provided", 400

    image_file = request.files['image']
    if image_file.filename == '':
        return "Empty filename", 400

    # Save uploaded image
    filepath = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(filepath)

    # Read image as grayscale
    img = cv2.imread(filepath, 0)
    if img is None:
        return "Failed to load image", 500

    height, width = img.shape

    # Run detection
    detector = DetectionofCopyMoveForgery(
        img, height, width,
        blocksize=8,
        oklid_threshold=3.5,
        correlation_threshold=8,
        vec_len_threshold=100,
        num_ofvector_threshold=5
    )
    detector.detection_forgery()

    # Save output result
    result_path = os.path.join(UPLOAD_FOLDER, 'result.png')
    cv2.imwrite(result_path, img)

    # Return the result image to frontend
    return send_file(result_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
