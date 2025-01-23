import streamlit as st
import pandas as pd
import random
import wikipedia-api as wikipedia
import requests
from io import BytesIO
from PIL import Image

# Function to get a movie's poster from Wikipedia
def get_movie_poster(movie_title):
    try:
        # Search for the movie on Wikipedia
        search_result = wikipedia.search(movie_title)
        if search_result:
            # Get the first result (most likely to be the correct article)
            page = wikipedia.page(search_result[0])
            # Look for the image in the page content
            image_url = None
            for img in page.images:
                if img.endswith('.jpg') or img.endswith('.png'):
                    image_url = img
                    break
            if image_url:
                # Download the image
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                return img
        return None
    except wikipedia.exceptions.DisambiguationError as e:
        st.error(f"Ambiguous search result: {e.options}")
    except Exception as e:
        st.error(f"Error fetching poster: {e}")

# Streamlit app to show random movie
def show_random_movie():
    # Load the CSV file containing movie data
    df = pd.read_csv("movies.csv")

    # Choose a random movie
    movie = df.sample().iloc[0]
    movie_title = movie['title']
    letterboxd_url = movie['letterboxd_url']

    # Get movie poster from Wikipedia
    poster_image = get_movie_poster(movie_title)

    # Display movie info
    st.title("Random Movie Picker")
    st.header(f"Title: {movie_title}")
    st.subheader(f"Year: {movie['year']}")
    
    if poster_image:
        st.image(poster_image, caption=f"{movie_title} Poster", use_column_width=True)
    else:
        st.write("Poster not found.")

    st.markdown(f"[View on Letterboxd]({letterboxd_url})")

if __name__ == "__main__":
    show_random_movie()
