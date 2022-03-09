import re
import random
import requests
import numpy as np
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup

headers = {'Accept-Language': 'en-US, en:q=0.5'}

rows = []
j = 1
for i in range(1, 1001, 50):
  res = requests.get('https://www.imdb.com/search/title/?groups=top_1000&start=' + str(i) +
        '&ref_=adv_nxt',
        headers=headers)
  soup = BeautifulSoup(res.text, 'html.parser')
  movies = soup.find_all('div', class_='lister-item mode-advanced')
  
  for movie in movies:
    row = []
        
    title = movie.h3.a.text
    row.append(title)
    
    year = movie.h3.find('span', class_ = 'lister-item-year').text
    row.append(year)
    
    certificate = movie.p.find('span', class_ = 'certificate')
    if certificate:
      certificate = certificate.text
    else:
      certificate = np.nan
    row.append(certificate)
  
    runtime = movie.p.find('span', class_ = 'runtime')
    if runtime:
      runtime = runtime.text
    else:
      runtime = np.nan
    row.append(runtime)
  
    genres = movie.p.find('span', class_ = 'genre')
    if genres:
      genres = genres.text
    else:
      genres = np.nan
    row.append(genres)
  
    rating = movie.strong.text
    row.append(rating)
      
    metascore = movie.find('span', class_ = 'metascore')
    if metascore:
      metascore = metascore.text
    else:
      metascore = np.nan
    row.append(metascore)

    director = movie.find_all('p')[2].a.text
    row.append(director)
      
    extras = movie.find('p', class_ = 'sort-num_votes-visible')
    labels = [span.text for span in extras.find_all('span', 'text-muted')]
    values = [span.text for span in extras.find_all('span', attrs = {'name': 'nv'})]
  
    possible_labels = ['Votes:', 'Gross:', 'Top 250:']
    for possible_label in possible_labels:
        if possible_label in labels:
            i = labels.index(possible_label)
            row.append(values[i])
        else:
            row.append(np.nan)
          
    rows.append(row)
    print(j, title)
    j += 1
  sleep(random.randint(1,5))

df = pd.DataFrame(rows, columns = ['Title', 'Release Year', 'MPA Film Rating', 
                                   'Runtime', 'Genres', 'User Rating', 'Metascore',
                                   'Director', 'Number of Votes', 'U.S. Box Office', 
                                   'Top 250 Ranking'])

df['Release Year'] = df['Release Year'].str.extract('(\d{4})')
df['Runtime'] = df['Runtime'].str.extract('(\d*)')
df['Genres'] = df['Genres'].str.strip().str.split(', ')
df['User Rating'] = df['User Rating'].astype(float)
df['Metascore'] = df['Metascore'].astype(float)
df['Number of Votes'] = df['Number of Votes'].str.replace(',', '').astype(int)
df['U.S. Box Office'] = df['U.S. Box Office'].str.extract('(\d*\.\d*)').astype(float)
df['Top 250 Ranking'] = df['Top 250 Ranking'].str.extract('#(\d*)')

df.to_csv('movies.csv')