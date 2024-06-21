import os
import cv2
import numpy as np
from deepface import DeepFace
from tqdm import tqdm

def blur_faces(image_path, output_path):
    image = cv2.imread(image_path)
    if image is None:
        return
        
    faces_num = 0

    # Detect faces using RetinaFace
    detections = DeepFace.extract_faces(image, detector_backend='yolov8', enforce_detection=False, align=False)
    for detection in detections:
        if detection['confidence'] > 0:
            roi = detection['facial_area']
            x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']
            face = image[y:y+h, x:x+w]
            face = cv2.GaussianBlur(face, (65, 65), 20)
            image[y:y+h, x:x+w] = face
            
            faces_num += 1

    cv2.imwrite(output_path, image)
    return faces_num
    
def process_directory(directory):
    image_paths = []
    created = False
    found_in = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))
                
    for image_path in tqdm(image_paths,  desc='Processing images'):         
        #output_path = image_path
        if not created:
            created = True
        output_path = os.path.join(os.path.dirname(image_path), os.path.basename(image_path))
        faces_num = blur_faces(image_path, output_path)
        if faces_num: found_in.append(image_path+"\t"+str(faces_num))
    
    with open('/app/images/blurred_images.txt', 'w') as f:
        s = "Faces found in the following images (filename-number_of_faces):\n"
        for i in found_in:
            s += '\t' + i + '\n'    
        f.write(s)

if __name__ == '__main__':
    import sys
    
    directory = sys.argv[-1]
    print("BLURRING FACES...")
    process_directory(directory)
    print("FACES BLURRED!")
