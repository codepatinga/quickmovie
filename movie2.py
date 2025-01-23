import streamlit as st
import requests
import random
from bs4 import BeautifulSoup
import urllib.parse

# Function to get a random movie from a Letterboxd list
def get_random_movie_from_letterboxd_list(list_url):
    # Send a GET request to the Letterboxd list page
    response = requests.get(list_url)
    if response.status_code != 200:
        return None
    
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract movie titles from the list page
    movies = []
    for item in soup.find_all('div', class_='poster-container'):
        title_tag = item.find('a', class_='poster-link')
        if title_tag:
            movie_title = title_tag['title']
            movies.append(movie_title)

    if not movies:
        return None

    # Choose a random movie from the list
    random_movie = random.choice(movies)

    # Construct the URL for the movie on Letterboxd
    movie_url = f"https://letterboxd.com{urllib.parse.quote(random_movie.replace(' ', '-'))}/"

    return {
        'title': random_movie,
        'url': movie_url
    }

# Streamlit interface
st.image("https://github.com/codepatinga/quickmovie/blob/main/logo.png?raw=true", width=300)
st.title('Quick Movie Recommendation System (From Letterboxd List)')

# Text input to enter Letterboxd list URL
list_url = st.text_input("Enter a Letterboxd List URL", "https://letterboxd.com/films/by/ranking/")  # Example list URL

# Button to fetch movie recommendation
if st.button('Get Movie Recommendation'):
    movie_data = get_random_movie_from_letterboxd_list(list_url)
    
    if movie_data:
        st.write(f"### {movie_data['title']}")
        st.markdown(f"[More Info on Letterboxd]({movie_data['url']})", unsafe_allow_html=True)
    else:
        st.write("No movie found or failed to fetch data from the list.")
