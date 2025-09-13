# app.py

import streamlit as st
from spotify.spotify_client import get_recommendations, MOOD_TO_GENRE, get_valid_genres
from emotion_detection.face_emotion import analyze_face_emotion
from emotion_detection.voice_emotion import analyze_voice_emotion

# Page setup
st.set_page_config(page_title="AuraSync - AI Music Recommender", layout="wide")
st.title("🎵 AuraSync - AI Music Recommender")
st.write("Welcome! Detect your mood via **Face** or **Voice** and get personalized Spotify recommendations.")

# Sidebar for options
st.sidebar.title("🎭 Choose Emotion Detection Mode")
mode = st.sidebar.radio("Select detection method:", ["Face (Webcam)", "Voice (Audio File)"])

detected_mood = None

# --- Face Detection Mode ---
if mode == "Face (Webcam)":
    img_file = st.camera_input("Take a picture to detect your mood")
    if img_file is not None:
        if st.button("Analyze Face Emotion"):
            with st.spinner("Analyzing your facial expression..."):
                detected_mood = analyze_face_emotion(img_file)
            st.success(f"Detected Mood: **{detected_mood}**")

# --- Voice Detection Mode ---
elif mode == "Voice (Audio File)":
    uploaded_file = st.file_uploader("Upload an audio file (WAV/MP3)", type=["wav", "mp3"])
    if uploaded_file is not None:
        if st.button("Analyze Voice"):
            with st.spinner("Analyzing your voice tone..."):
                detected_mood = analyze_voice_emotion(uploaded_file)
            st.success(f"Detected Mood: **{detected_mood}**")

# --- Spotify Recommendations ---
if detected_mood:
    st.subheader(f"🎧 Recommended Tracks for Mood: {detected_mood.capitalize()}")
    try:
        # Get valid Spotify genres
        valid_genres = get_valid_genres()
        mapped_genre = MOOD_TO_GENRE.get(detected_mood.lower(), "pop")

        # Validate against Spotify's official seeds
        if mapped_genre not in valid_genres:
            st.warning(f"⚠️ Genre '{mapped_genre}' not supported by Spotify. Falling back to 'pop'.")
            mapped_genre = "pop"

        st.info(f"Using Spotify Genre Seed: **{mapped_genre}**")

        # Fetch recommendations
        tracks = get_recommendations(detected_mood)
        if not tracks:
            st.warning("No recommendations found. Try another mood!")
        else:
            for idx, track in enumerate(tracks, start=1):
                st.write(f"{idx}. [{track['name']} - {track['artist']}]({track['url']})")
    except Exception as e:
        st.error(f"Error fetching recommendations: {e}")


        
