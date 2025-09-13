# emotion_detection/face_emotion.py

import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
import tempfile

def analyze_face_emotion(image_file):
    """
    Detects the dominant emotion from an uploaded/captured image.
    Works with Streamlit's st.camera_input() or file_uploader().
    """
    try:
        # Convert Streamlit UploadedFile / CameraInput to OpenCV format
        image = Image.open(image_file).convert("RGB")
        frame = np.array(image)  # PIL → NumPy (RGB)

        # Convert RGB → BGR (OpenCV format expected by DeepFace)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Analyze emotion using DeepFace
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)

        # DeepFace may return a list depending on version
        if isinstance(result, list):
            result = result[0]

        return result.get("dominant_emotion", "neutral")

    except Exception as e:
        raise RuntimeError(f"Face emotion analysis failed: {e}")
