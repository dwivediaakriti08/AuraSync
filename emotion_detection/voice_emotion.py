# emotion_detection/voice_emotion.py

import librosa
import numpy as np
import joblib
import tempfile

# Load a pre-trained voice emotion model (must be trained & saved separately)
try:
    model = joblib.load("voice_emotion_model.pkl")
except:
    model = None

def analyze_voice_emotion(audio_file):
    """
    Extracts features from audio and predicts emotion using a trained model.
    Works with both file paths and Streamlit's UploadedFile objects.
    """
    if model is None:
        raise RuntimeError("Voice emotion model not found. Please train and save it first.")

    # Handle Streamlit uploaded file (BytesIO-like)
    if hasattr(audio_file, "read"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        file_path = tmp_path
    else:
        # Already a file path
        file_path = audio_file

    # Load audio
    y, sr = librosa.load(file_path, sr=None)

    # Extract MFCC features
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    features = np.mean(mfccs.T, axis=0).reshape(1, -1)

    # Predict emotion
    prediction = model.predict(features)[0]
    return prediction
