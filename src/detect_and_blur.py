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
    detections = DeepFace.extract_faces(image, detector_backend='yolov8', enforce_detection=False, align=False)
    for detection in detections:
        if detection['confidence'] > 0:
            roi = detection['facial_area']
            x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']
            face = image[y:y+h, x:x+w]
            face = cv2.GaussianBlur(face, (65, 65), 20)
            image[y:y+h, x:x+w] = face

    cv2.imwrite(output_path, image)

def process_directory(directory):
    image_paths = []
    created = False
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))
                
    for image_path in tqdm(image_paths,  desc='Processing images'):         
        #output_path = image_path
        if not created:
            created = True
        output_path = os.path.join(os.path.dirname(image_path), os.path.basename(image_path))
        blur_faces(image_path, output_path)

if __name__ == '__main__':
    import sys
    
    directory = sys.argv[-1]
    print("BLURRING FACES...")
    process_directory(directory)
    print("FACES BLURRED!")
