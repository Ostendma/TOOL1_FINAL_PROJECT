# Comp4447-Final-Project
Data Science Tools 1 Final Project

The Final Project.ipynb is the jupyter notebook that loads the appropriate csv files, cleans data, conducts exploratory data analysis and runs the models
To run this model one needs the following csv files:
- OMDB API Data.csv
- CPI Data.csv
- NLP Data.csv

Source Data:
- This includes the data we used from https://grouplens.org/datasets/movielens/25m/
- The full data set from grouplens included data we did not use for our analysis
- We ended up using links.csv and movies.csv to obtain a movie's title, imdbID and tmdbID to do our webscraping and API pulls.

Initial Data Scraping & Collection
- BOM_Data_Pull.py - this is the python script we used to get opening weekend revenue and number of theaters
- OMDB API.py - this is the python script we used to get other descriptive data from the OMDB API
- TMDB API.py - this is the python script we used to connect to the TMDB API to get budget, overview, production company and collections data
- OMDB API Data.csv - this is the resulting csv file from all of the API pulls and web scrapes
- CPI Data.csv - this is CPI data
- Links File Full.csv - files that includes the imdbID and tmdbID used for the web scrape and API puls

NLP Data Scraping & Analysis
- Movie_Review_Scrape_Script.py - this is the python script that took a movie's tmdbID and pulled the featured review
- NLP.ipynb - jupyter notebook that does the NLP sentiment analysis
- Featured_Reviews_with_tmdbid.csv - the data set that was ran through the NLP models
- NLP.csv - the output from the NLP model
- links_final.csv - used in the Movie_Review_Scrape_Script.py
- movies_final.csv - used in the Movie_Review_Scrape_Script.py
- No_Review_Found.csv - a resulting csv file from the Movie_Review_Scrape_Script.py
