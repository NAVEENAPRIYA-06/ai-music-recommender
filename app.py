import streamlit as st
from spotify_client import search_songs_by_mood

# Set page configuration
st.set_page_config(page_title="AI Music Recommender", layout="centered")

# App Title
st.title("🎵 AI Music Recommendation System")
st.write("Enter your mood and get real-time Spotify song suggestions!")

# Mood Input
mood = st.text_input("Enter your mood (happy, sad, relaxed, energetic, etc.):")

# Button to fetch songs
if st.button("Get Recommendations"):
    if mood:
        st.write(f"🎧 Fetching songs for mood: **{mood}**...")
        try:
            songs = search_songs_by_mood(mood)
            if songs:
                st.subheader("Recommended Songs:")
                for s in songs:
                    st.markdown(f"**{s['name']}** by *{s['artist']}* → [Listen Here]({s['url']})")
            else:
                st.error("No songs found! Try another mood.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a mood to get recommendations.")
