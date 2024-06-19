import os
import cv2
import numpy as np
from deepface import DeepFace
from tqdm import tqdm

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
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))
                
    for image_path in tqdm(image_paths,  desc='Processing images'):         
        #output_path = image_path
        output_path = os.path.join(os.path.dirname(image_path), 'blurred_' + os.path.basename(image_path))
        blur_faces(image_path, output_path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python detect_and_blur.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    process_directory(directory)
