import streamlit as st
import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image

# Function to get movie poster from Letterboxd URL
def get_movie_poster_from_letterboxd(letterboxd_url):
    try:
        # Fetch the Letterboxd page content
        response = requests.get(letterboxd_url)
        response.raise_for_status()  # Ensure the request was successful

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the poster image by looking for the <meta> tag for the movie poster
        meta_image_tag = soup.find('meta', property='og:image')
        if meta_image_tag:
            image_url = meta_image_tag.get('content')
            if image_url:
                # Download the image
                img_response = requests.get(image_url)
                img = Image.open(BytesIO(img_response.content))
                return img
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Letterboxd page: {e}")
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

    # Get movie poster from Letterboxd URL
    poster_image = get_movie_poster_from_letterboxd(letterboxd_url)

    # Display movie info
    st.title("Quick Movie Recommendation System")
    st.header(f"Title: {movie_title}")
    st.subheader(f"Year: {movie['year']}")
    
    if poster_image:
        st.image(poster_image, use_container_width=True)
    else:
        st.write("Poster not found.")

    st.markdown(f"[View on Letterboxd]({letterboxd_url})")

if __name__ == "__main__":
    show_random_movie()
