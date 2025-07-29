import streamlit as st
import json
import os
from spotify_client import search_songs_by_mood

# File for storing favorites
FAV_FILE = "favorites.json"

# Load favorites from JSON
def load_favorites():
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r") as f:
            return json.load(f)
    return []

# Save favorites to JSON
def save_favorites(favorites):
    with open(FAV_FILE, "w") as f:
        json.dump(favorites, f)

# Set page configuration
st.set_page_config(page_title="AI Music Recommender", layout="centered")

# Initialize session state
if 'favorites' not in st.session_state:
    st.session_state['favorites'] = load_favorites()

# App Title
st.title("🎵 AI Music Recommendation System")
st.write("Enter your mood and get real-time song suggestions!")

# Mood Input
mood = st.text_input("Enter your mood (happy, sad, relaxed, energetic, etc.):")

# Fetch recommendations
if st.button("Get Recommendations"):
    if mood.strip():
        st.write(f"🎧 Fetching songs for mood: **{mood}**...")
        try:
            songs = search_songs_by_mood(mood)
            if songs:
                st.session_state['current_songs'] = songs
            else:
                st.error("No songs found! Try another mood.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a mood to get recommendations.")

# Show recommended songs
if 'current_songs' in st.session_state and st.session_state['current_songs']:
    st.subheader("Recommended Songs:")
    for index, s in enumerate(st.session_state['current_songs']):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{s['name']}** by *{s['artist']}* → [Listen]({s['url']})")
        with col2:
            if st.button("❤️", key=f"fav_{index}"):
                if s not in st.session_state['favorites']:
                    st.session_state['favorites'].append(s)
                    save_favorites(st.session_state['favorites'])  # Save to file
                    st.success(f"Added {s['name']} to favorites!")

# Favorites Section
st.markdown("---")
st.subheader("⭐ Your Favorite Songs")
if st.session_state['favorites']:
    for fav in st.session_state['favorites']:
        st.markdown(f"**{fav['name']}** by *{fav['artist']}* → [Listen]({fav['url']})")
else:
    st.write("No favorites yet. Add some by clicking ❤️.")
