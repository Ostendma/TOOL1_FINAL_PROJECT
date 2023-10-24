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
    df_list = []
    header = ['Title','Year','Rated','Released','Runtime','Genre','Director','Writer','Actors'
              ,'Plot','Language','Country','Awards','Poster',"All Ratings",'Internet Movie Database'
              ,'Rotten Tomatoes','Metacritic','Metascore','imdbRating','imdbVotes','imdbID'
              ,'Type','DVD','BoxOffice','Production','Website','Response']
    
    #Read in list of valid tt id's
    ttid_list = TT_file_read()

    #loop through all tt id's and pull data from the api
    for i in ttid_list:
       weburl = baseurl + i + extension + apikey
       response = requests.get(weburl)
       soup = str(bsoup(response.text , 'html.parser'))
       soup = soup.strip('[]')
       soup = soup.replace('\\"', '"')
        
       data_list = json.loads(soup)
       title = data_list.get("Title")
       year = data_list.get('Year')
       Rated = data_list.get("Rated")
       Released = data_list.get("Released")
       Runtime = data_list.get("Runtime")
       Genre = data_list.get("Genre")
       Director = data_list.get("Director")
       Writer = data_list.get("Writer")
       Actors = data_list.get("Actors")
       Plot = data_list.get("Plot")
       Language = data_list.get("Language")
       Country = data_list.get("Country")
       Awards = data_list.get("Awards")
       Poster = data_list.get("Poster")
       Ratings = data_list.get("Ratings")
       Metascore = data_list.get("Metascore")
       imdbRating = data_list.get("imdbRating")
       imdbVotes = data_list.get("imdbVotes")
       imdbID = data_list.get("imdbID")
       Type = data_list.get("Type")
       DVD = data_list.get("DVD")
       BoxOffice = data_list.get("BoxOffice")
       Production = data_list.get("Production")
       Website = data_list.get("Website")
       Response = data_list.get("Response")
       
       Ratings_IMDB = np.nan 
       Ratings_Rotten = np.nan
       Ratings_Metacritic = np.nan
        
       #Loop through rating column to extract the specific data. Set to NA if no data is found 
       for i in range(0,len(Ratings)):
           if Ratings[i].get("Source") == "Internet Movie Database":
               Ratings_IMDB = Ratings[i].get("Value")
           if  Ratings[i].get("Source") == "Rotten Tomatoes":
               Ratings_Rotten = Ratings[i].get("Value")  
           if  Ratings[i].get("Source") == "Metacritic":
               Ratings_Metacritic = Ratings[i].get("Value")  
       
       df_list += [[title,year,Rated, Released, Runtime, Genre, Director, Writer, Actors, Plot, Language
                     , Country, Awards, Poster, Ratings, Ratings_IMDB, Ratings_Rotten, Ratings_Metacritic
                     , Metascore, imdbRating, imdbVotes, imdbID, Type, DVD, BoxOffice, Production, Website, Response]] 

    df = pd.DataFrame(df_list, columns=header)            
    
    #Output data to csv
    df.to_csv("OMDB API Data.csv", index=False)

def TT_file_read():
    """Read in valid TT's to pull data using API

    Returns:
        Dataframe: One column of pandas dataframe which has the valid tt values in it
    """
    df = pd.read_csv('BOM Data.csv')
    return df['TT Value']

if __name__ == '__main__':
    scrape_omdb_site()
    #TT_file_read()