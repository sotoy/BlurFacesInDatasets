import os
import cv2
import numpy as np
from deepface import DeepFace

def blur_faces(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        return

    # Detect faces using RetinaFace
    detections = DeepFace.extract_faces(image, detector_backend='retinaface', enforce_detection=False, align=False)
    for detection in detections:
        roi = detection['facial_area']
        x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']
        face = image[y:y+h, x:x+w]
        face = cv2.GaussianBlur(face, (21, 21), 20)
        image[y:y+h, x:x+w] = face

    cv2.imwrite(output_path, image)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                output_path = image_path
                #output_path = os.path.join(root, 'blurred_' + file)
                blur_faces(image_path, output_path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python detect_and_blur.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    process_directory(directory)

