from accessKeys import API_KEY
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import time

def get_articles_json(month, year, api_key=API_KEY):
    print('Getting articles for {}/{}'.format(month,year))
    url = 'https://api.nytimes.com/svc/archive/v1/{}/{}.json'.format(year, month)
    params = {'api-key': api_key}
    response = requests.get(url, params=params)
    print('status code: {}'.format(response.status_code))
    while response.status_code != 200:
        print('trying again...')
        time.sleep(15)
        response = requests.get(url, params=params)
        print('status code: {}'.format(response.status_code))
    data = json.loads(response.text)
    try:
        data['response']['docs']
        print('Get articles success')
        return data['response']['docs']
    except Exception as e:
        print('ERROR:, {}'.format(e))
        return {}

def get_year(x):
    return x['pub_date'].split('T')[0].split('-')[0]

def get_month(x):
    return x['pub_date'].split('T')[0].split('-')[1]

def clean_df(df_raw):
    temp_df = df_raw[df_raw['type_of_material'] == 'News'].reset_index()
    temp_df['year'] = temp_df.apply(get_year, axis=1)
    temp_df['month'] = temp_df.apply(get_month, axis=1)
    temp_df = temp_df[['year', 'month', '_id', 'web_url', 'word_count']]
    return temp_df

def parse_url(url, retry=False):
    time.sleep(0.8)
    response_text = requests.get(url)    
    soup = BeautifulSoup(response_text.content, 'html.parser')
    all_text = soup.find_all(attrs={'class':'story-body-text'})
    if len(all_text) == 0 and not retry:
        joined_text = parse_url(url, retry=True)
    else:
        joined_text = ' '.join([x.text for x in all_text])
    return joined_text

def get_write_article(year, month, start_point=0):
    raw_df = pd.DataFrame(get_articles_json(month,year))
    cleaned_df = clean_df(raw_df)
    print('number of articles: {}'.format(len(cleaned_df)))
    n = 50  #chunk row size
    # Split dataframe into chunks so we can parse and write to csv in chunks
    start_point = start_point * n
    temp_dfs = [cleaned_df[i:i+n].copy() for i in range(start_point,cleaned_df.shape[0],n)]
    no_chunks = len(temp_dfs)
    print('number of chunks: {}'.format(no_chunks))
    
    with open('{}_{}.csv'.format(year, month), 'a') as f:
        for idx, df_chunk in enumerate(temp_dfs):
            df_chunk['article'] = df_chunk['web_url'].apply(parse_url)
            df_chunk.to_csv(f, header=False, encoding='utf-8')
            print('done writing {} of {}'.format((idx + 1), no_chunks))
#             if idx >= 100:
#                 return
            time.sleep(15)


for i in range(1,13):
    get_write_article(2014,i)
#     time.sleep(60)
