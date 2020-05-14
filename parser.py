import requests
from bs4 import BeautifulSoup
from lxml import html
import datetime
import psycopg2

url = 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PS4CAT/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
def get_pages_count(url, headers):
    store_page = requests.get(url,  headers = headers)
    soup = BeautifulSoup(store_page.text, 'lxml')
    pages_info = soup.find('div', {'class': 'grid-footer-controls'})\
        .find('a', {'class': 'paginator-control__end paginator-control__arrow-navigation internal-app-link ember-view'})\
        .get('href').split('/')
    pages_qty = int(pages_info[-1])
    return pages_qty
def get_game_data(url, headers, page):
    games_info = []
    current_url = url + str(page+1)
    store_page = requests.get(current_url, headers=headers)
    soup = BeautifulSoup(store_page.text, 'lxml')
    games_titles = soup.find_all('div', {'class': 'grid-cell__body'})
    for game in games_titles:
        try:
            game_id = game.find('a', {'class': 'internal-app-link ember-view'}).get('href').split('/')[3]
            game_title = game.find('div', {'class': 'grid-cell__title'}).find('span').text
            game_price = (game.find('h3', {'class':
                                           game.find('h3').get('class')}).text).split('\xa0')
            actual_date = str(datetime.datetime.now().date())
            games_info.append({'game_id' : game_id,
                                'game_title': game_title,
                               'game_price': game_price[1],
                               'price_value': game_price[0],
                               'actual_date': actual_date})
        except: TypeError
    return games_info

pages = int(get_pages_count(url, headers))
#for page in range(pages):
    #print(get_game_data(url, headers, page))

con = psycopg2.connect(
  database="Psn_game_base",
  user="postgres",
  password="va041062",
  host="127.0.0.1",
  port="5432"
)

cur = con.cursor()
cur.execute('''CREATE TABLE PSN_GAMES  
     (ID INT PRIMARY KEY NOT NULL,
      GAME_ID TEXT NOT NULL, 
      GAME_TITLE TEXT NOT NULL, 
      PRICE INT NOT NULL, 
      VALUE TEXT NOT NULL, 
      REQ_DATE DATE NOT NULL);''')
con.commit()
con.close()