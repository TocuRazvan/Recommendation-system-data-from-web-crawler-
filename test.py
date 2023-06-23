import requests                 # Simpler HTTP requests 
from bs4 import BeautifulSoup   # Python package for pulling data out of HTML and XML files
import pandas as pd             # Python package for data manipulation and analysis
import re                       # regular expressions
import json                     # Python package used to work with JSON data
from tqdm import tqdm           # python for displaying progressbar 
from datetime import datetime   # python package to retireve DateTime


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

url = 'https://www.imdb.com/chart/top'              # IMDb Top 250 list link
url_text = requests.get(url, headers=headers).text                    # Get the session text for the link
url_soup = BeautifulSoup(url_text, 'html.parser')   # Get data from the HTML

template = 'https://www.imdb.com%s'

# Get the title links for all the pages
title_links = [template % a.attrs.get('href') for a in url_soup.select('td.titleColumn a')]

imdb_movie_list = []
# Getting the various fields and creating a list of objects with details
#   - ranking | movie_name | url | year | rating | vote_count | summary | production | director | writer_1 | writer_2
#   - genre_1 | genre_2 | genre_3 | genre_4 | release date | censor_rating | movie_length | country | language
#   - budget | gross_worldwide |

    #for i in tqdm(range(0, len(title_links)), desc="Movies processed", ncols=100):
for i in tqdm(range(5), desc="Movies processed", ncols=100):
    page_url = title_links[i]
    page_text = requests.get(page_url, headers=headers).text
    page_soup = BeautifulSoup(page_text, 'html.parser')
    
    # ------------------------------------------------------------------------------------------
    # Getting data about the movie name ,year,rating,vote,stars,driectors,writers
    movie_name = (page_soup.find("span",{"class":"sc-afe43def-1"}).get_text(strip=True).split('|')[0]).split('(')[0]
    
    #print('Titlu',movie_name)
    header_container = page_soup.find('div', {"class": "sc-52d569c6-0"})
    year_time_container = header_container.find('ul', {"class": "sc-afe43def-4"});
    li_element = year_time_container.find('li')
    first_anchor_tag = li_element.find('a')
    year = first_anchor_tag.get_text(strip=True)
    #print('Year:', year)
    
    rating = page_soup.find('span', {"class": "sc-bde20123-1"}).get_text(strip=True)
    #print(rating)
    
    vote_count = page_soup.find('div', {"class": "sc-bde20123-3"}).get_text(strip=True)
    #print(vote_count)
    
    summary_element = page_soup.find('span', {'data-testid': 'plot-l'})
    if summary_element:
        summary = summary_element.get_text(strip=True)
        #print('summary', summary)
    else:
        summary = None
        print('No summary')


    
    stars_writer_director_container = page_soup.find('div', {"class": "sc-52d569c6-3"}).find('div').find('ul')
    s_w_d_items = stars_writer_director_container.findAll("li")
    director_comp_arr = s_w_d_items[0].find("div").find('ul')
    directors = [w.get_text() for w in director_comp_arr]
    #print('directors', directors)
    
    writers_comp_arr =  s_w_d_items[1 + len(directors)].find('div').find('ul')
    if writers_comp_arr :
        writers_comp_arr = writers_comp_arr.findAll('li')
        writers = [w.get_text() for w in writers_comp_arr]
        #print('writers', writers)
    else :
        writers = []
        print('No writers found')
 
    
    stars_comp_arr = s_w_d_items[2 + len(directors) + len(writers)].find('div').find('ul').findAll('li')
    stars = [s.get_text() for s in stars_comp_arr]
    #print('stars', stars)
    
#   # Getting data about genres
#     _genres = page_soup.find('li', {'data-testid': 'storyline-genres'})
#     if _genres:
#         genres_div = _genres.find('div')
#         if genres_div:
#             genres_ul = genres_div.find('ul')
#             if genres_ul:
#                 genres_li = genres_ul.find_all('li')
#                 genres_list = [genre.find('a').get_text(strip=True) for genre in genres_li]
#                 print('Genres:', genres_list)
#     else:
#         genres_list = None
#         print('No genres information found.')


    # ---------------------------------------------------------------------------------
   # Getting data about release date
    _release_date = page_soup.find('li', {'data-testid': "title-details-releasedate"})
    if _release_date:
        release_date_div = _release_date.find('div')
        if release_date_div:
            release_date_ul = release_date_div.find('ul')
            if release_date_ul:
                release_date = release_date_ul.find('li').find('a').get_text(strip=True)
                #print('Release date:', release_date)
    else:
        release_date = None
        print('No release date')

# Getting data about country
    _country = page_soup.find('li', {'data-testid': "title-details-origin"})
    if _country:
        country_div = _country.find('div')
        if country_div:
            country_ul = country_div.find('ul')
            if country_ul:
                country_li = country_ul.findAll('li')
                country = [c.get_text() for c in country_li]
                #print('Country:', country)
    else:
        country = None
        print('No country')
    
    
    _sites = page_soup.find('li', {'data-testid': "details-officialsites"})
    if _sites:
        sites_div = _sites.find('div')
        if sites_div:
            sites_ul=sites_div.find('ul')
        if sites_ul:
            sites_li=sites_ul.findAll('li')
            sites = [s.find('a').get('href') for s in sites_li]
            #print('sites', sites)
    else:
        sites = None
        print('No sites')
         
        
    # Getting data about language
    _language = page_soup.find('li', {'data-testid': "title-details-languages"})
    if _language:
        language_div = _language.find('div')
        if language_div:
            language_ul = language_div.find('ul')
            if language_ul:
                language_li = language_ul.findAll('li')
                language = [l.get_text() for l in language_li]
                #print('Language:', language)
        else:
            language = None
            print('No language information found.')
     
    # Getting data about budget
    _budget = page_soup.find('li', {"data-testid": "title-boxoffice-budget"})
    if _budget:
        budget_div = _budget.find('div')
        if budget_div:
            budget_ul = budget_div.find('ul')
            if budget_ul:
                budget_li = budget_ul.findAll('li')
                if len(budget_li) > 0:
                    budget = budget_li[0].get_text(strip=True)
                    #print('Budget:', budget)
                else:
                    budget = None
                    print('No budget information found.')

    # Getting data about worldwide gross
    _gross_worldwide = page_soup.find('li', {"data-testid": "title-boxoffice-cumulativeworldwidegross"})
    if _gross_worldwide:
        gross_worldwide_div = _gross_worldwide.find('div')
        if gross_worldwide_div:
            gross_worldwide_ul = gross_worldwide_div.find('ul')
            if gross_worldwide_ul:
                gross_worldwide_li = gross_worldwide_ul.findAll('li')
                gross_worldwide = gross_worldwide_li[0].get_text(strip=True)
                #print('Gross Worldwide:', gross_worldwide)
        else:
            gross_worldwide = None
            print('No gross worldwide information found.')
    
    _run_time = page_soup.find('li', {"data-testid": "title-techspec_runtime"})
    run_time= [l.get_text() for l in _run_time]
    #print('Run time', run_time)
    
 
    movie_data = {
    'Ranking': i+1, 
    'Movie Name': movie_name, 
    'url': page_url, 
    'Year': year,
    'Rating': rating,
    'Vote Count': vote_count, 
    'Director': directors, 
    'Writers': writers, 
    'Stars': stars,
    #'Genres List' :genres_list, 
    'Summary': summary,
    'Site':sites,
    'Release Date': release_date,
    'Country': country,
    'Run Time': run_time, 
    'Language': language, 
    'Budget': budget, 
    'Gross Worldwide': gross_worldwide,
    }

    # add the dictionary to the list
    imdb_movie_list.append(movie_data)
timestamp =  datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
imdb_list = {
   "timestamp" : timestamp,
   "imdb_movies" : imdb_movie_list
}
with open('imdb_data.json', 'w') as file:
   json.dump(imdb_list, file)
# write the list to a JSON file
with open('imdb_data_TEST.json', 'w', encoding='utf-8') as f:
    json.dump(imdb_list, f, ensure_ascii=False, indent=4)
     
#     dataframe_columns = [ 'ranking', 'movie_name', 'url', 'year', 'rating', 'vote_count', 'summary', 'production_1', 'production_2', 'production_3', 'director', 'writer_1', 'writer_2', 'star_1', 'star_2', 'star_3', 'genre_1', 'genre_2', 'genre_3', 'genre_4','release_date', 'censor_rating', 'movie_length', 'country_1', 'country_2', 'country_3', 'country_4', 'language_1', 'language_2', 'language_3', 'language_4', 'language_5', 'budget', 'gross_worldwide']
#     dataframe = pd.DataFrame(columns=dataframe_columns)
# for i in range(0, len(imdb_movie_list)):
#     dataframe.at[i, 'ranking'] = imdb_movie_list[i]['ranking']
#     dataframe.at[i, 'movie_name'] = imdb_movie_list[i]['movie_name']
#     dataframe.at[i, 'url'] = imdb_movie_list[i]['url']
#     dataframe.at[i, 'year'] = imdb_movie_list[i]['year']
#     dataframe.at[i, 'rating'] = imdb_movie_list[i]['rating']
#     dataframe.at[i, 'vote_count'] = imdb_movie_list[i]['vote_count']
#     dataframe.at[i, 'summary'] = imdb_movie_list[i]['summary']
#     dataframe.at[i, 'director'] = imdb_movie_list[i]['director'][0]
#     dataframe.at[i, 'writer_1'] = imdb_movie_list[i]['writers'][0]
#     dataframe.at[i, 'writer_2'] = imdb_movie_list[i]['writers'][1]
#     dataframe.at[i, 'star_1'] = imdb_movie_list[i]['stars'][0]
#     dataframe.at[i, 'star_2'] = imdb_movie_list[i]['stars'][1]
#     dataframe.at[i, 'star_3'] = imdb_movie_list[i]['stars'][2]
#     # dataframe.at[i, 'genre_1'] = imdb_movie_list[i]['genres'][0]
#     # dataframe.at[i, 'genre_2'] = imdb_movie_list[i]['genres'][1]
#     # dataframe.at[i, 'genre_3'] = imdb_movie_list[i]['genres'][2]
#     # dataframe.at[i, 'genre_4'] = imdb_movie_list[i]['genres'][3]
#     dataframe.at[i, 'release_date'] = imdb_movie_list[i]['release_date']
#     # dataframe.at[i, 'censor_rating'] = imdb_movie_list[i]['censor_rating']
#     dataframe.at[i, 'run_time'] = imdb_movie_list[i]['run_time']
#     dataframe.at[i, 'country_1'] = imdb_movie_list[i]['country'][0]
#     dataframe.at[i, 'country_2'] = imdb_movie_list[i]['country'][1]
#     dataframe.at[i, 'country_3'] = imdb_movie_list[i]['country'][2]
#     dataframe.at[i, 'country_4'] = imdb_movie_list[i]['country'][3]
#     dataframe.at[i, 'language'] = imdb_movie_list[i]['language'][0]
#     dataframe.at[i, 'language_2'] = imdb_movie_list[i]['language'][1]
#     dataframe.at[i, 'language_3'] = imdb_movie_list[i]['language'][2]
#     dataframe.at[i, 'language_4'] = imdb_movie_list[i]['language'][3]
#     dataframe.at[i, 'language_5'] = imdb_movie_list[i]['language'][4]
#     dataframe.at[i, 'budget'] = imdb_movie_list[i]['budget']
#     dataframe.at[i, 'site'] = imdb_movie_list[i]['site']
#     dataframe.at[i, 'gross_worldwide'] = imdb_movie_list[i]['gross_worldwide']


# dataframe = dataframe.set_index(['ranking'], drop=False)
# dataframe.to_csv('./src/data/imdb_movies_data.csv')
# print("Successfully saved to CSV")