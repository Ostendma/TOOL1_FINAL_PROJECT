from bs4 import BeautifulSoup as bsoup
import requests
import re
import numpy as np
import pandas as pd
import csv
import time
from typing import Tuple
import os

links_df = pd.read_csv('links_final.csv')
movies_df = pd.read_csv('movies_final.csv')

# print(links_df.head())
# print(movies_df.head())

def clean_title(title: str) -> Tuple[str, str]:
    """
    Clean and transform the movie title based on specified rules, handling special characters and extra content.

    Parameters:
    title (str): The original title.

    Returns:
    str: The cleaned and transformed title.
    str: The year extracted from the title.
    """

    # Extract the year and save it for later use
    year_match = re.search(r'\((\d{4})\)', title)
    year = year_match.group(1) if year_match else ''

    # Remove the year and any content in parentheses from the title
    title = re.sub(r'\([^)]*\)', '', title).strip()

    # Rule for cases like "Title, The" to transform into "the-title"
    if ',' in title:
        parts = [part.strip() for part in title.split(',')]
        if parts[-1].lower() == 'the':
            parts = [parts[-1]] + parts[:-1]  # Rearranging the order
            title = ' '.join(parts)

    # Lowercase the title
    title = title.lower()

    # Remove punctuation and special characters
    title = re.sub(r'[^\w\s-]', '', title)  # Keeping hyphens, removing other punctuation

    # Replace spaces and remaining punctuation with hyphens
    title = re.sub(r'[\s]+', '-', title).strip('-')

    # Handle non-ASCII characters by trying to represent them in the closest ASCII form
    title = title.encode("ascii", errors="ignore").decode()  # This removes non-ASCII characters

    return title, year

# Apply the cleaning function to the 'title' column
movies_df['cleaned_title'], movies_df['year'] = zip(*movies_df['title'].map(clean_title))

# Merge the two dataframes on 'movieId'
merged_df = pd.merge(movies_df, links_df, on='movieId')

# Create the "lookup ID" which is a combination of 'tmdbId' and 'cleaned_title'
merged_df['lookup_id'] = merged_df['tmdbId'].astype(str) + '-' + merged_df['cleaned_title']

# Display the first few rows of the merged dataframe to verify the results
print(merged_df.head())




def scrape_reviews():
    """"Scrapes 'featured review' from the movie page"""

    base_url = "https://www.themoviedb.org/movie/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    no_review_list = []  # Movies with no featured review
    bad_id_list = []  # IDs leading to a bad or non-existent page
    review_list = []  # Successfully scraped reviews
    valid_ids = []  # IDs that have been successfully scraped

    id_df = merged_df  
    total_movies = len(id_df)

    for index, row in id_df.iterrows():
        lookup_id = row['lookup_id']
        movie_url = base_url + lookup_id

        try:
            response = requests.get(movie_url, headers=headers).text
            soup = bsoup(response, 'html.parser')

            review_div = soup.find('div', {"class":"teaser"})

            if review_div is not None: 
                review_paragraph = review_div.find('p')
                if review_paragraph and review_paragraph.text:
                    review_text = review_paragraph.get_text(strip=True)
                    review_list.append([lookup_id, movie_url, review_text])
                    valid_ids.append(lookup_id)
                else:
                    no_review_list.append([lookup_id, movie_url, 'No review paragraph found'])
            else:
                no_review_list.append([lookup_id, movie_url, 'No review div found'])

        except Exception as e:
            print(f"Error with {lookup_id}: {str(e)}")
            bad_id_list.append([lookup_id, movie_url, 'Error occurred'])

    # Convert lists to DataFrames
    review_df = pd.DataFrame(review_list, columns=['Lookup ID', 'URL', 'Featured Review'])
    no_review_df = pd.DataFrame(no_review_list, columns=['Lookup ID', 'URL', 'Status'])
    bad_id_df = pd.DataFrame(bad_id_list, columns=['Lookup ID', 'URL', 'Status'])

    # Save to CSV
    review_df.to_csv('Featured_Reviews.csv', index=False)
    no_review_df.to_csv('No_Review_Found.csv', index=False)
    bad_id_df.to_csv('Bad_IDs.csv', index=False)

scrape_reviews()