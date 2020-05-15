import requests
from bs4 import BeautifulSoup
import lxml
import datetime
import psycopg2

url = 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PS4CAT/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
con = psycopg2.connect(
        database="Psn_game_base",
        user="postgres",
        password="va041062",
        host="127.0.0.1",
        port="5432"
    )
cur = con.cursor()
cur.execute('''CREATE TABLE psn_games
     (id SERIAL PRIMARY KEY NOT NULL,
     game_id TEXT NOT NULL,
      game_title TEXT NOT NULL,
      price FLOAT NOT NULL,
     value TEXT NOT NULL,
      req_date DATE NOT NULL);''')
con.commit()
con.close()

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
            game_price = (game.find('h3', {'class':game.find('h3').get('class')}).text).split('\xa0')
            actual_date = str(datetime.datetime.now().date())
            games_info.append({'game_id': game_id,
                                'game_title': game_title,
                               'game_price': float(game_price[1]),
                               'price_value': game_price[0],
                               'actual_date': actual_date})
        except: TypeError
    return games_info

pages = int(get_pages_count(url, headers))

con = psycopg2.connect(
        database="Psn_game_base",
        user="postgres",
        password="va041062",
        host="127.0.0.1",
        port="5432"
    )
cur = con.cursor()

for page in range(pages):
    page_info = get_game_data(url, headers, page)
    for i in range(len(page_info)):
        cur.execute(
            "INSERT INTO PSN_GAMES (GAME_ID, GAME_TITLE, PRICE, VALUE, REQ_DATE) VALUES (%s, %s, %s, %s, %s)",
            (page_info[i]['game_id'], page_info[i]['game_title'], page_info[i]['game_price'], page_info[i]['price_value'], page_info[i]['actual_date']
        ))
        con.commit()

con.close()

