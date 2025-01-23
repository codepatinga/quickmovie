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

         # Find the image tag with the class "image"
        image_tag = soup.find('img', class_='image')
        if image_tag:
            image_url = image_tag.get('src')
            if image_url:
                # Make sure the URL is absolute (some websites may use relative paths)
                if not image_url.startswith('http'):
                    image_url = f"https:{image_url}"

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
