import os
from deepface import DeepFace
import cv2
import numpy as np


def get_image_folder():
  """
  Prompts the user for the folder path containing images.

  Returns:
      str: Path to the image folder provided by the user.
  """
  folder_path = input("Enter the path to the folder containing images: ")
  return folder_path
  
  
  
def blur_faces(folder_path):
  """
  Blurs faces in all images within a specified folder.

  Args:
      folder_path (str): Path to the folder containing images.
  """
  for filename in os.listdir(folder_path):
    if filename.endswith((".jpg", ".jpeg", ".png", ".JPEG")):
      print(filename)
      image_path = os.path.join(folder_path, filename)
      # Detect faces
      result = DeepFace.extract_faces(img_path=image_path, enforce_detection=False, detector_backend='retinaface')
      # Check for detected faces
      
      if len(result):
        img = cv2.imread(image_path)
        print(img.shape)
        for face in result:
          # Extract face ROI coordinates
          roi = face['facial_area']
          x, y, w, h = roi['x'], roi['y'], roi['w'], roi['h']
          x = 0 if x<0 else x
          y = 0 if y<0 else y
          print("x, y, w, h", x, y, w, h)
          face_roi = img[x:x+w, y:y+h]
          print(np.isnan(face_roi).any())
          print(face_roi.shape)
          # Apply blurring effect on the ROI
          blurred_roi = apply_blur(face_roi)
          # Replace ROI in the original image
          img[x:x+w, y:y+h] = blurred_roi
        # Save the modified image
        save_path = os.path.join(folder_path, filename)
        cv2.imwrite(save_path, img)
      else:
        print(f"No faces detected in image: {image_path}")  # Handle no faces scenario  

# Function to apply blurring effect (replace with your preferred method)
def apply_blur(face_roi):
  # Example using Gaussian blur
  return cv2.GaussianBlur(face_roi, (5, 5), 0)

if __name__ == "__main__":
  folder_path = get_image_folder()
  blur_faces(folder_path)
  print(f"Finished blurring faces in {folder_path}")

