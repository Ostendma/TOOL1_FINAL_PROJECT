from bs4 import BeautifulSoup as bsoup
import requests
import numpy as np
import pandas as pd
import csv
import time

def get_bom_data():
    """Goes to box office mojo and grabs opening weekend box office revenue and number of theaters.
    Creates 3 csvs. One with a list of TT ID's that are not valid and cannot get to the website.
    A csv of TT ID's where there is no second link to get number of theaters.
    Final csv with valid data
    """
    baseurl_BOM_title = "https://www.boxofficemojo.com/title/"
    baseurl_BOM = "https://www.boxofficemojo.com"
    extension = "/?ref_=bo_se_r_1"
    
    bad_ttid = []
    df_list = []
    no_data = []
    valid_tt = []

    #Get all TT IDs
    ttdf = open_final_tt_file()
    file_len = len(ttdf['imdbId'])
    tt_count = 1
    
    for index, row in ttdf.iterrows():
        tt = str(row[1])
        tmdbid = str(row[2])
        weburl = baseurl_BOM_title + tt + extension
        try:
            response = requests.get(weburl).text
            soup = bsoup(response, 'html.parser')
            TT_class = soup.find_all('div', {"class":"a-section a-spacing-none"})
            for i in TT_class:
                if i.find('a') != None:
                    if i.find('a').get('href').find('release') == 1:
                        new_url = baseurl_BOM + i.find('a').get('href')
                        opening_rev = i.find('a').text 
                        num_theaters = get_theaters(new_url)
                        df_list += [[tt, weburl, opening_rev, new_url, num_theaters, tmdbid]]
                        valid_tt += [tt]
            
            if tt not in valid_tt:
                    no_data += [[tt, weburl]]        
        except:
               bad_ttid += [[tt, weburl]] 

        #Shows how far the file is in processing
        if tt_count % (file_len // 50) == 0:
            print(f"{tt_count / file_len * 100:.0f}% of the loop completed.")
        tt_count += 1

    df = pd.DataFrame(df_list,columns=['imdbID', 'TT URL', 'Opening Revenue', 'RL URL', 'Number of Theaters', 'tmdbID'])
    df_bad_tt = pd.DataFrame(bad_ttid, columns=['imdbID', 'TT URL'])
    df_no_data = pd.DataFrame(no_data, columns=['imdbID', 'TT URL'])
    
    df.to_csv('BOM Data.csv', index=False)
    df_bad_tt.to_csv('Bad TT File.csv', index=False)
    df_no_data.to_csv('No Data File.csv', index=False)


def get_theaters(rlurl):
    """Takes in the second url that is scraped from the table from box office mojo
    finds the number of theaters and returns it

    Args:
        rlurl (string): website link scraped from box office mojo to get number of theaters

    Returns:
        string: The number of theaters a movie was released in for opening weekend
    """
    rlresponse = requests.get(rlurl).text
    rlsoup = bsoup(rlresponse, 'html.parser')
    RL_class = rlsoup.find_all('br')
    for x in RL_class:
        if x.next_sibling.find('theater') != None and x.next_sibling.find('theater') >0:
            return x.next_sibling.split()[0]
    return np.Nan     
 

def open_final_tt_file():
    """Opens file with all the TT ID's in it

    Returns:
        List: List of TT ID's to try and pull information for
    """
    ttid_list = []
    TT_filename = r'C:\Matt Grad School\Comp 4447\Final Project\Matt Links Small.csv'
    ttdf = pd.read_csv(TT_filename)
    ttdf.fillna(0, inplace=True)
    ttdf['tmdbId'] = ttdf['tmdbId'].astype(int)
    
    return ttdf


if __name__ == '__main__':
    start_time = time.time()
    get_bom_data()
    print("--- %s seconds ---" % (time.time() - start_time))
    #open_final_tt_file()
