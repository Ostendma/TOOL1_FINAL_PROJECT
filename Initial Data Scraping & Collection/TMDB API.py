from bs4 import BeautifulSoup as bsoup
import requests
import pandas as pd
import json


def scrape_tmdb_api(df):

    apikey = '448fb8084e6c46cb8447cda0cd773e3a'
    extension = '?api_key='
    baseurl = 'https://api.themoviedb.org/3/movie/'
    
    for index, row in df.iterrows():
        weburl = baseurl + str(row['tmdbID']) + extension + apikey
        response = requests.get(weburl)
        soup = str(bsoup(response.text , 'html.parser'))
        data_list = json.loads(soup)
        
        df.at[index, 'url'] = weburl
        df.at[index, 'budget'] = data_list.get('budget')
        df.at[index, 'original_title'] = data_list.get('original_title')
        df.at[index,'title'] = data_list.get('title')
        df.at[index,'overview'] = data_list.get('overview')
        df.at[index, 'production_company'] = str(data_list.get('production_companies'))
        df.at[index,'belongs_to_collection'] = str(data_list.get('belongs_to_collection'))
        
    df.to_csv("TMDB API Data Part4.csv", index=False)


def tmbdID_file_read():
    """Read in valid TT's to pull data using API

    Returns:
        Dataframe: One column of pandas dataframe which has the valid tt values in it
    """
    df = pd.read_csv('BOM Data Final Part4.csv')
    
    return df

if __name__ == '__main__':
    scrape_tmdb_api(tmbdID_file_read())
    #tmbdID_file_read()
