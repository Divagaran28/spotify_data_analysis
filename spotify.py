from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re
import os

# ==============================
# Spotify API Authentication
# ==============================
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='Replace with your Client ID',   # Replace with env variables in production
    client_secret='Replace with your Client ID'
))

# ==============================
# Read track URLs from file
# ==============================
file_path = "spotify_data_analysis/track_urls.txt"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File '{file_path}' not found.")

with open(file_path, 'r') as file:
    track_urls = [url.strip() for url in file.readlines() if url.strip()]

if not track_urls:
    raise ValueError("No track URLs found in the file.")

# ==============================
# Process each URL
# ==============================
all_tracks = []

for track_url in track_urls:
    # Extract track ID safely using regex
    match = re.search(r'track/([a-zA-Z0-9]+)', track_url)
    if not match:
        print(f"Invalid URL format: {track_url}")
        continue

    track_id = match.group(1)

    try:
        # Fetch track details
        track = sp.track(track_id)

        # Extract metadata
        track_data = {
            'Track Name': track['name'],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration (minutes)': track['duration_ms'] / 60000
        }

        all_tracks.append(track_data)

    except Exception as e:
        print(f"Error processing URL: {track_url}, Error: {e}")

# ==============================
# Save and Display Results
# ==============================
if not all_tracks:
    raise ValueError("No valid track data retrieved.")

# Convert to DataFrame
df = pd.DataFrame(all_tracks)

# Print DataFrame
print("\nTrack Data:")
print(df)

# Save to CSV
df.to_csv('spotify_track_data.csv', index=False)
print("\nData saved to 'spotify_track_data.csv'")

# ==============================
# Visualization
# ==============================
plt.figure(figsize=(7, 5))

# Plot popularity
plt.bar(df['Track Name'], df['Popularity'], color='green', edgecolor='black', label='Popularity')

# Plot duration (optional: as second y-axis)
# plt.plot(df['Track Name'], df['Duration (minutes)'], color='red', marker='o', label='Duration (min)')

plt.title("Spotify Track Metadata")
plt.xticks(rotation=45, ha='right')
plt.ylabel('Value')
plt.legend()
plt.tight_layout()
plt.show()