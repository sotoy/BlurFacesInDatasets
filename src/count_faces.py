import os
import cv2
import numpy as np
from deepface import DeepFace
from tqdm import tqdm

def detect_faces(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return

    # Detect faces using RetinaFace
    detections = DeepFace.extract_faces(image, detector_backend='retinaface', enforce_detection=False, align=False)
    dets = [det for det in detections if det['confidence'] > 0.1]
    return len(dets)
        

def traverse_directory(directory, when):
    image_count = 0
    total_faces = 0
    image_paths = []
    found_in = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))
                
    for image_path in tqdm(image_paths, desc='Counting faces'):         
        image_count += 1
        num_faces = detect_faces(image_path)
        if num_faces > 1:
            found_in.append(image_path+"\t"+str(num_faces))
        total_faces += num_faces
                
    with open('/app/images/faces_'+when+'.txt', 'w') as f:
        s = "Number of images in Dataset: "+str(image_count)+'.\n'
        s += "Number of faces in Dataset "+when+" blurring: "+str(total_faces)+'.\n'
        s += "Face frequency in Dataset: "+str((total_faces*1.0)/image_count)+' faces per image.\n\n\n'
        s += "Faces found in the following images (filename-number_of_faces):\n"
        for i in found_in:
            s += '\t' + i + '\n'
        
        f.write(s)

if __name__ == '__main__':
    import sys
    directory = sys.argv[-2]
    when = sys.argv[-1]
    print("COUNTING FACES...")
    traverse_directory(directory, when)
    print("FACES COUNTED...")
