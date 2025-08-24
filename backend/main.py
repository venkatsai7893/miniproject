from flask import Flask, request, jsonify, send_file
from detection import DetectionofCopyMoveForgery, getFmeasure
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'backend/sample_images'
OUTPUT_IMAGE = 'backend/static/result.png'

@app.route('/detect', methods=['POST'])
def detect_forgery():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    img = cv2.imread(filepath, 0)
    height, width = img.shape

    # Run detection
    forgery_detector = DetectionofCopyMoveForgery(img.copy(), height, width, 8, 3.5, 8, 100, 5)
    forgery_detector.detection_forgery()

    # Save result
    cv2.imwrite(OUTPUT_IMAGE, forgery_detector.img)
    return send_file(OUTPUT_IMAGE, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
