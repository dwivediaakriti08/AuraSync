import requests
from base64 import b64encode

# --- Spotify API credentials ---
SPOTIFY_CLIENT_ID = "444e3617af0847eaad07f46883ba0796"
SPOTIFY_CLIENT_SECRET = "5b0d13e33ff042e0bfa9d574e075d205"

# --- Mood → Genre mapping (expanded with Spotify-supported seeds) ---
MOOD_TO_GENRE = {
    "happy": "pop",
    "sad": "acoustic",
    "angry": "metal",
    "fear": "ambient",
    "neutral": "chill",
    "surprise": "dance",
    "disgust": "punk",
    # More moods → Spotify-supported genres
    "love": "romance",
    "chill": "chill",
    "study": "study",
    "party": "dance",
    "workout": "work-out",
    "focus": "focus",
    "relax": "sleep",
    "travel": "road-trip",
    "classical": "classical",
    "jazz": "jazz",
    "indie": "indie",
    "rap": "hip-hop",
    "sadness": "blues",
    "celebration": "party",
    "energized": "edm",
    "calm": "ambient",
    "nostalgic": "singer-songwriter",
}


def get_spotify_token():
    """Authenticate with Spotify API and return access token."""
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + b64encode(
            f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()
        ).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f"Failed to authenticate: {response.text}")

    return response.json()["access_token"]


def get_valid_genres():
    """Fetch valid Spotify genre seeds. Returns fallback on failure."""
    token = get_spotify_token()
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("genres", [])

    # If Spotify fails, return safe defaults
    print(f"⚠️ Could not fetch valid genres. Falling back to defaults. Error: {response.status_code}")
    return ["pop", "rock", "hip-hop", "jazz"]


def get_recommendations(mood, limit=10):
    """
    Get Spotify track recommendations based on detected mood.
    Uses Search API with genre filtering for reliability.
    """
    token = get_spotify_token()
    genre = MOOD_TO_GENRE.get(mood.lower(), "pop")

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": f"genre:{genre}",
        "type": "track",
        "limit": limit
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Spotify API error {response.status_code}: {response.text}")

    data = response.json()
    tracks = []
    for item in data.get("tracks", {}).get("items", []):
        tracks.append({
            "name": item["name"],
            "artist": item["artists"][0]["name"],
            "url": item["external_urls"]["spotify"]
        })

    return tracks
