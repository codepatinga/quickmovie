import streamlit as st
import requests
import random
import urllib.parse

def get_movie_recommendation(genre_name):
    api_key = '568e9a36cfaba6826530142303f5e74f'  # Replace 'YOUR_API_KEY' with your actual TMDB API key
    genres_response = requests.get(f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US").json()
    genre_id = next((genre["id"] for genre in genres_response["genres"] if genre["name"].lower() == genre_name.lower()), None)
    
    if genre_id:
        movies_response = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={api_key}&with_genres={genre_id}&vote_average.gte=6.5&language=en-US").json()
        if movies_response["results"]:
            movie = random.choice(movies_response["results"])
            release_year = movie['release_date'].split("-")[0] if 'release_date' in movie and movie['release_date'] else "Unknown release year"
            st.write(f"Recommended movie: {movie['title']} ({release_year}) with IMDb rating: {movie['vote_average']}")
            poster_path = movie['poster_path']
            if poster_path:
                st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", caption=movie['title'])
            # Create a link to search for the movie on JustWatch
            justwatch_search_url = f"https://www.justwatch.com/us/search?q={urllib.parse.quote(movie['title'])}"
            st.markdown(f"[Watch on JustWatch]({justwatch_search_url})", unsafe_allow_html=True)
        else:
            st.write("No movies found in this genre with the specified rating.")
    else:
        st.write("Invalid genre name.")

st.title('Movie Recommendation System')
genre_name = st.text_input("Enter a genre: ")
if st.button('Get Recommendation'):
    get_movie_recommendation(genre_name)
