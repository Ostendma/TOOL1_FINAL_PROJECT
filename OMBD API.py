import json
import numpy as np
from bs4 import BeautifulSoup as bsoup
import requests
import pandas as pd

def scrape_omdb_site():
    """Goes to omdbi api and returns all the values into a csv. Splits out ratings into seperate columns 
    """
    apikey = 'a8e7ab1f'
    baseurl = 'https://www.omdbapi.com/?i='
    extension = "&apikey="

    #Read in list of valid tt id's
    df = TT_file_read()
    
    #loop through all tt id's and pull data from the api
    for index, row in df.iterrows():
       ttid = row['imdbID']
       weburl = baseurl + ttid + extension + apikey
       response = requests.get(weburl)
       soup = str(bsoup(response.text , 'html.parser'))
       soup = soup.strip('[]')
       
        
       data_list = json.loads(soup)
       df.at[index,'omdb title'] = data_list.get("Title")
       df.at[index,'year'] = data_list.get('Year')
       df.at[index,'Rated'] = data_list.get("Rated")
       df.at[index,'Released'] = data_list.get("Released")
       df.at[index,'Runtime'] = data_list.get("Runtime")
       df.at[index,'Genre'] = data_list.get("Genre")
       df.at[index,'Director'] = data_list.get("Director")
       df.at[index,'Writer'] = data_list.get("Writer")
       df.at[index,'Actors'] = data_list.get("Actors")
       df.at[index,'Plot'] = data_list.get("Plot")
       df.at[index,'Language'] = data_list.get("Language")
       df.at[index,'Country'] = data_list.get("Country")
       df.at[index,'Awards'] = data_list.get("Awards")
       df.at[index,'Poster'] = data_list.get("Poster")
       Ratings = data_list.get("Ratings")
    
       
       df.at[index,'Ratings_IMDB'] = np.nan 
       df.at[index,'Ratings_Rotten'] = np.nan
       df.at[index,'Ratings_Metacritic'] = np.nan
        

       #Loop through rating column to extract the specific data. Set to NA if no data is found 
       for i in range(0,len(Ratings)):
           if Ratings[i].get("Source") == "Internet Movie Database":
               df.at[index,'Ratings_IMDB'] = Ratings[i].get("Value")
           if  Ratings[i].get("Source") == "Rotten Tomatoes":
               df.at[index,'Ratings_Rotten'] = Ratings[i].get("Value")  
           if  Ratings[i].get("Source") == "Metacritic":
               df.at[index,'Ratings_Metacritic'] = Ratings[i].get("Value")  
       
       df.at[index,'Metascore'] = data_list.get("Metascore")
       df.at[index,'imdbRating'] = data_list.get("imdbRating")
       df.at[index,'imdbVotes'] = data_list.get("imdbVotes")
       df.at[index,'imdbID'] = data_list.get("imdbID")
       df.at[index,'Type'] = data_list.get("Type")
       df.at[index,'DVD'] = data_list.get("DVD")
       df.at[index,'BoxOffice'] = data_list.get("BoxOffice")
       df.at[index,'Production'] = data_list.get("Production")
       df.at[index,'Website'] = data_list.get("Website")
       df.at[index,'Response'] = data_list.get("Response")           
                 
    
    #Output data to csv
    df.to_csv("OMDB API Data.csv", index=False)

def TT_file_read():
    """Read in valid TT's to pull data using API

    Returns:
        Dataframe: One column of pandas dataframe which has the valid tt values in it
    """
    df = pd.read_csv('TMDB API Data Small.csv')
    return df

if __name__ == '__main__':
    scrape_omdb_site()
    #TT_file_read()