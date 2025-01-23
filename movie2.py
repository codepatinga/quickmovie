import streamlit as st
import requests
import random
import urllib.parse
import os

# Fetch API key from environment variable for better security
api_key = os.getenv('OMDB_API_KEY', '66d5d104')  # Replace with your OMDb API key

# Function to get a random movie from a specific decade
def get_random_movie_from_decade(decade):
    start_year = decade
    end_year = decade + 9
    url = f"http://www.omdbapi.com/?apikey={api_key}&type=movie&y={start_year}&y2={end_year}&plot=short"
    
    response = requests.get(url).json()
    
    if response.get('Response') == 'True':
        movies = response.get('Search', [])
        if movies:
            movie = random.choice(movies)
            movie_title = movie['Title']
            release_year = movie['Year']
            imdb_rating = movie.get('imdbRating', 'N/A')
            poster_url = get_wikipedia_poster(movie_title)
            return {
                'title': movie_title,
                'year': release_year,
                'rating': imdb_rating,
                'poster': poster_url,
                'url': f"https://www.imdb.com/find?q={urllib.parse.quote(movie_title)}"
            }
    return None

# Function to get movie poster from Wikipedia
def get_wikipedia_poster(movie_title):
    # Search for the movie on Wikipedia
    search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(movie_title)}&limit=1&format=json"
    search_response = requests.get(search_url).json()
    
    if search_response[1]:  # Check if we found any results
        # Fetch the Wikipedia page URL
        movie_page_url = search_response[3][0]
        
        # Fetch the page content from Wikipedia
        page_response = requests.get(f"https://en.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(movie_page_url)}&format=json").json()
        
        # Try to extract the image URL from the infobox (common place for posters)
        page_content = page_response.get('parse', {}).get('text', {}).get('*', '')
        
        # Look for the first image URL from the infobox, typically the movie poster
        start_index = page_content.find('infobox')  # Looking for the infobox
        if start_index != -1:
            # Extract image URL (this is a simplified way to scrape the infobox for the first image)
            img_start = page_content.find('src="', start_index)
            if img_start != -1:
                img_start += 5  # Skip 'src="'
                img_end = page_content.find('"', img_start)
                if img_end != -1:
                    poster_url = "https:" + page_content[img_start:img_end]
                    return poster_url
    return None

# Function to get movie recommendations from the last 7 decades (1960s to 2020s)
def get_movie_recommendations():
    decades = [1960, 1970, 1980, 1990, 2000, 2010, 2020]  # Updated to include 1960s and remove 2030s
    recommendations = []
    
    for decade in decades:
        movie_data = get_random_movie_from_decade(decade)
        if movie_data:
            recommendations.append(movie_data)
    
    return recommendations

# Streamlit interface
st.image("https://github.com/codepatinga/quickmovie/blob/main/logo.png?raw=true", width=300)
st.title('Quick Movie Recommendation System (Random Movies from Last 7 Decades)')

if st.button('Get Movie Recommendations'):
    recommendations = get_movie_recommendations()
    
    for idx, movie in enumerate(recommendations):
        if movie:
            st.write(f"### {movie['title']} ({movie['year']}) - IMDb Rating: {movie['rating']}")
            if movie['poster'] and movie['poster'] != 'N/A':
                st.image(movie['poster'], caption=movie['title'])
            st.markdown(f"[More Info on IMDb]({movie['url']})", unsafe_allow_html=True)
